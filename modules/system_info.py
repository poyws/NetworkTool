"""
Sistema de Informações de Rede

Este módulo avançado coleta e exibe informações detalhadas sobre a configuração
de rede do sistema, incluindo endereços IP locais e públicos, endereço MAC,
interfaces de rede, velocidade de conexão e servidores DNS configurados.
Suporta diferentes sistemas operacionais (Windows, Linux, macOS).
"""

import socket
import uuid
import subprocess
import re
import os
import psutil
import requests
from colorama import Fore, Style
import platform
import time

class SystemInfo:
    """
    Classe responsável por coletar e fornecer informações de rede do sistema.
    
    Esta classe oferece métodos para obtenção de dados detalhados sobre
    a configuração de rede do sistema, desde endereços IP e MAC até
    informações de interfaces, velocidades e configurações DNS.
    Fornece suporte a múltiplos sistemas operacionais e formata os dados
    de maneira consistente para análise e diagnóstico.
    """
    
    def __init__(self):
        """
        Inicializa a classe SystemInfo.
        
        Coleta informações básicas sobre o sistema operacional durante
        a inicialização, que serão utilizadas posteriormente em outros métodos.
        """
        self.os_name = platform.system()  # Nome do sistema operacional
        self.hostname = socket.gethostname()  # Nome do host
        self.system_platform = platform.platform()  # Informações da plataforma
        self.python_version = platform.python_version()  # Versão do Python
    
    def get_local_ip(self):
        """
        Obtém os endereços IP locais do sistema (IPv4 e IPv6).
        
        Este método tenta criar conexões UDP com servidores DNS públicos
        para determinar os endereços IP locais utilizados para saída.
        Essa técnica garante que seja obtido o IP atual em uso, não apenas
        um IP listado nas interfaces de rede.
        
        Returns:
            dict: Dicionário contendo endereços IPv4 e IPv6
        """
        local_ips = {"IPv4": "Não disponível", "IPv6": "Não disponível"}
        
        # Tenta obter endereço IPv4
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 1))  # Servidor DNS do Google
            local_ips["IPv4"] = s.getsockname()[0]
            s.close()
        except Exception as e:
            local_ips["IPv4"] = f"Não disponível: {str(e)}"
        
        # Tenta obter endereço IPv6
        try:
            s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
            s.connect(('2001:4860:4860::8888', 1))  # DNS IPv6 do Google
            local_ips["IPv6"] = s.getsockname()[0]
            s.close()
        except Exception as e:
            local_ips["IPv6"] = "Não disponível"
            
        return local_ips
    
    def get_public_ip(self):
        """
        Determina o endereço IP público utilizado para acesso à Internet.
        
        Este método consulta vários serviços online confiáveis de verificação
        de IP, tentando cada um até conseguir uma resposta válida. Utiliza
        múltiplas fontes para garantir maior confiabilidade.
        
        Returns:
            str: Endereço IP público ou mensagem de erro
        """
        # Lista de serviços para verificar IP público com fallback
        ip_services = [
            ('https://api.ipify.org', 5),
            ('https://ipinfo.io/ip', 5),
            ('https://checkip.amazonaws.com', 5),
            ('https://ifconfig.me', 5)
        ]
        
        try:
            for service_url, timeout in ip_services:
                try:
                    response = requests.get(service_url, timeout=timeout)
                    if response.status_code == 200:
                        return response.text.strip()
                except:
                    continue
                    
            return "Não foi possível determinar o IP público"
        except Exception as e:
            return f"Erro ao obter o IP público: {str(e)}"
    
    def get_mac_address(self):
        """
        Obtém o endereço MAC da interface principal de rede.
        
        Utiliza a biblioteca uuid para obter o identificador
        universal único da máquina, convertendo-o para o formato
        padrão de endereço MAC (XX:XX:XX:XX:XX:XX).
        
        Returns:
            str: Endereço MAC formatado
        """
        # Obtem o número MAC como inteiro
        mac = uuid.getnode()
        
        # Converte para o formato XX:XX:XX:XX:XX:XX
        mac_formatted = ':'.join(['{:02x}'.format((mac >> elements) & 0xff) 
                                  for elements in range(0, 8 * 6, 8)][::-1])
        
        return mac_formatted
    
    def get_network_interfaces(self):
        """
        Obtém informações detalhadas sobre todas as interfaces de rede do sistema.
        
        Este método coleta dados sobre todas as interfaces de rede disponíveis,
        incluindo status (ativo/inativo), endereços IPv4 e IPv6 associados,
        e endereços MAC. Interfaces de loopback são ignoradas.
        
        Returns:
            list: Lista de strings com informações formatadas das interfaces
        """
        interfaces = []
        
        # Coleta informações sobre interfaces de rede usando psutil
        net_if_addrs = psutil.net_if_addrs()
        net_if_stats = psutil.net_if_stats()
        
        # Itera sobre todas as interfaces encontradas
        for interface_name, interface_addresses in net_if_addrs.items():
            # Ignora interfaces de loopback
            if interface_name.startswith('lo'):
                continue
            
            # Verifica se a interface está ativa
            status = "Ativo" if net_if_stats.get(interface_name) and getattr(net_if_stats.get(interface_name), 'isup', False) else "Inativo"
            
            addresses = []
            mac_address = None
            
            # Processa todos os endereços associados a esta interface
            for addr in interface_addresses:
                if addr.family == socket.AF_INET:
                    # Endereço IPv4
                    addresses.append(f"IPv4: {addr.address}")
                elif addr.family == socket.AF_INET6:
                    # Endereço IPv6 (ignora endereços link-local)
                    if not addr.address.startswith('fe80'):
                        addresses.append(f"IPv6: {addr.address}")
                elif addr.family == psutil.AF_LINK:
                    # Endereço MAC da interface
                    mac_address = addr.address
            
            # Formata as informações da interface
            interface_info = f"{interface_name} - {status}"
            if mac_address:
                interface_info += f" - MAC: {mac_address}"
            if addresses:
                interface_info += f" - {', '.join(addresses)}"
            
            interfaces.append(interface_info)
        
        # Caso não encontre nenhuma interface válida
        if not interfaces:
            interfaces.append("Nenhuma interface de rede detectada")
            
        return interfaces
    
    def get_network_speed(self):
        """
        Mede a velocidade atual de download e upload da rede.
        
        Este método monitora as interfaces de rede por um segundo,
        calculando a taxa de transferência com base na diferença entre
        os contadores de bytes enviados e recebidos. O resultado é
        convertido para Megabits por segundo (Mbps).
        
        Returns:
            dict: Velocidades medidas (download, upload) e totais acumulados
        """
        try:
            # Coleta estatísticas iniciais
            start_stats = psutil.net_io_counters()
            # Aguarda 1 segundo para medição
            time.sleep(1)
            # Coleta estatísticas finais
            end_stats = psutil.net_io_counters()
            
            # Calcula a diferença de bytes em 1 segundo e converte para Mbps
            # (bytes * 8 bits/byte) / (1_000_000 bits/Mbps)
            download = (end_stats.bytes_recv - start_stats.bytes_recv) * 8 / 1_000_000
            upload = (end_stats.bytes_sent - start_stats.bytes_sent) * 8 / 1_000_000
            
            # Estatísticas totais de dados enviados/recebidos (em MB)
            total_sent = end_stats.bytes_sent / (1024 * 1024)
            total_recv = end_stats.bytes_recv / (1024 * 1024)
            
            return {
                "download": f"{download:.2f}",  # Velocidade de download em Mbps
                "upload": f"{upload:.2f}",      # Velocidade de upload em Mbps
                "total_sent": f"{total_sent:.2f}",  # Total enviado em MB
                "total_recv": f"{total_recv:.2f}"   # Total recebido em MB
            }
        except Exception as e:
            return {
                "download": "0.00",
                "upload": "0.00",
                "error": f"Erro ao obter velocidade da rede: {str(e)}"
            }
    
    def get_dns_servers(self):
        """
        Obtém os servidores DNS configurados no sistema operacional.
        
        Este método utiliza diferentes técnicas conforme o sistema operacional
        para identificar os servidores DNS configurados. Em Windows, utiliza
        o comando ipconfig; em macOS, o comando scutil; e em Linux, lê o arquivo
        /etc/resolv.conf.
        
        Returns:
            list: Lista de servidores DNS encontrados
        """
        dns_servers = []
        
        try:
            # Detecção específica por sistema operacional
            if self.os_name == "Windows":
                # Extrai servidores DNS do output do ipconfig no Windows
                output = subprocess.check_output("ipconfig /all", shell=True).decode()
                dns_pattern = r"DNS Servers[^\n]+:[^\n]+((?:\n[^:]+[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)+)"
                dns_matches = re.findall(dns_pattern, output)
                
                for match in dns_matches:
                    servers = re.findall(r"([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)", match)
                    dns_servers.extend(servers)
                    
            elif self.os_name == "Darwin":
                # Extrai servidores DNS no macOS (Darwin)
                output = subprocess.check_output("scutil --dns", shell=True).decode()
                dns_servers = re.findall(r"nameserver\[0-9]*\s*:\s*([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)", output)
                
            else:
                # Para Linux e outros sistemas, lê o arquivo resolv.conf
                if os.path.exists("/etc/resolv.conf"):
                    with open("/etc/resolv.conf", "r") as f:
                        resolv_conf = f.read()
                    dns_servers = re.findall(r"nameserver\s+([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)", resolv_conf)
        except Exception as e:
            dns_servers = []
            
        # Se nenhum servidor DNS for encontrado, fornece opções de DNS públicos
        if not dns_servers:
            dns_servers = ["8.8.8.8 (Google DNS)", "1.1.1.1 (Cloudflare DNS)", "208.67.222.222 (OpenDNS)"]
            
        return dns_servers
        
    def get_system_info(self):
        """
        Obtém informações gerais sobre o sistema.
        
        Retorna um dicionário com informações básicas sobre o sistema,
        incluindo nome de host, plataforma, versão do Python e nome do SO.
        
        Returns:
            dict: Informações do sistema
        """
        return {
            "hostname": self.hostname,         # Nome do host
            "platform": self.system_platform,  # Plataforma completa
            "python_version": self.python_version,  # Versão do Python
            "os_name": self.os_name            # Nome do sistema operacional
        }
