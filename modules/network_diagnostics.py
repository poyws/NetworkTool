"""
Módulo de Diagnósticos de Rede

Este módulo avançado fornece funcionalidades para análise e diagnóstico de redes,
incluindo teste de velocidade, verificação de latência, análise de perda de pacotes,
rastreamento de rota entre o sistema e servidores externos, e escaneamento da rede local.

A funcionalidade de escaneamento de rede permite identificar dispositivos ativos
na rede local, suas respostas ao ping e tentativas de resolução de nomes de host.
O escaneamento é otimizado usando threads para verificação simultânea de múltiplos IPs.

As ferramentas deste módulo funcionam em múltiplos sistemas operacionais e
fornecem resultados detalhados para uso em análises de desempenho e conectividade.
"""

import subprocess
import re
import socket
import platform
import time
import random
import math
import statistics
import os
import json
from datetime import datetime
import requests
from tqdm import tqdm

class NetworkDiagnostics:
    def __init__(self):
        self.os_name = platform.system()
        self.timeout = 10  # Tempo limite para operações de rede (segundos)
        self.speed_test_servers = [
            "speedtest.net",
            "fast.com",
            "speedtest.googlefiber.net"
        ]
        self.default_packet_count = 50  # Número padrão de pacotes para análise
    
    def speed_test(self):
        """
        Perform a network speed test.
        
        Returns:
            dict: Download speed, upload speed, and ping in Mbps and ms.
        """
        result = {"download": 0.0, "upload": 0.0, "ping": 0.0}
        
        try:
            # Simple speed test implementation - this is a basic approach
            # For a more accurate test, use speedtest-cli or other specialized tools
            
            # Measure ping
            start_time = time.time()
            requests.get('https://www.google.com', timeout=5)
            end_time = time.time()
            result["ping"] = (end_time - start_time) * 1000  # Convert to ms
            
            # Download speed test
            download_size = 10 * 1024 * 1024  # 10 MB
            download_url = "https://speed.cloudflare.com/__down?bytes=10000000"
            
            start_time = time.time()
            response = requests.get(download_url, stream=True, timeout=30)
            
            with tqdm(total=download_size, unit='B', unit_scale=True, desc="Download", leave=False) as pbar:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        downloaded += len(chunk)
                        pbar.update(len(chunk))
                    
                    # If we've downloaded enough, break
                    if downloaded >= download_size:
                        break
            
            end_time = time.time()
            download_time = end_time - start_time
            
            # Calculate speed in Mbps
            if download_time > 0:
                result["download"] = (downloaded * 8) / (download_time * 1_000_000)
            
            # Upload speed test - simulate with a POST request
            upload_size = 1 * 1024 * 1024  # 1 MB
            data = b'0' * upload_size
            
            start_time = time.time()
            
            with tqdm(total=upload_size, unit='B', unit_scale=True, desc="Upload", leave=False) as pbar:
                response = requests.post(
                    'https://httpbin.org/post',
                    data=data,
                    timeout=30,
                    headers={'Content-Type': 'application/octet-stream'}
                )
                pbar.update(upload_size)
            
            end_time = time.time()
            upload_time = end_time - start_time
            
            # Calculate speed in Mbps
            if upload_time > 0:
                result["upload"] = (upload_size * 8) / (upload_time * 1_000_000)
            
        except Exception as e:
            result["error"] = str(e)
            
        return result
    
    def latency_check(self, host="google.com"):
        """
        Check latency to a host.
        
        Args:
            host (str): The host to check latency to.
            
        Returns:
            dict: Min, avg, and max latency in ms.
        """
        result = {"min": 0.0, "avg": 0.0, "max": 0.0}
        
        try:
            if self.os_name == "Windows":
                # Windows ping
                output = subprocess.check_output(f"ping {host} -n 10", shell=True).decode()
                
                # Extract times
                times_match = re.search(r"Minimum = (\d+)ms, Maximum = (\d+)ms, Average = (\d+)ms", output)
                if times_match:
                    result["min"] = float(times_match.group(1))
                    result["max"] = float(times_match.group(2))
                    result["avg"] = float(times_match.group(3))
                    
            else:
                # Linux/macOS ping
                output = subprocess.check_output(f"ping -c 10 {host}", shell=True).decode()
                
                # Extract times
                times_match = re.search(r"min/avg/max/[^=]+ = (\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)", output)
                if times_match:
                    result["min"] = float(times_match.group(1))
                    result["avg"] = float(times_match.group(2))
                    result["max"] = float(times_match.group(3))
                    
        except Exception as e:
            result["error"] = str(e)
            
        return result
    
    def packet_loss_analysis(self, host="google.com", packets=50):
        """
        Analyze packet loss to a host.
        
        Args:
            host (str): The host to analyze packet loss to.
            packets (int): Number of packets to send.
            
        Returns:
            dict: Packet loss statistics.
        """
        result = {"sent": packets, "received": 0, "lost": 0, "loss_percentage": 0.0}
        
        try:
            if self.os_name == "Windows":
                # Windows ping
                output = subprocess.check_output(f"ping {host} -n {packets}", shell=True).decode()
                
                # Extract packet statistics
                stats_match = re.search(r"Sent = (\d+), Received = (\d+), Lost = (\d+)", output)
                if stats_match:
                    result["sent"] = int(stats_match.group(1))
                    result["received"] = int(stats_match.group(2))
                    result["lost"] = int(stats_match.group(3))
                    result["loss_percentage"] = (result["lost"] / result["sent"]) * 100
                    
            else:
                # Linux/macOS ping
                output = subprocess.check_output(f"ping -c {packets} {host}", shell=True).decode()
                
                # Extract packet statistics
                stats_match = re.search(r"(\d+) packets transmitted, (\d+) [packets ]*received", output)
                if stats_match:
                    result["sent"] = int(stats_match.group(1))
                    result["received"] = int(stats_match.group(2))
                    result["lost"] = result["sent"] - result["received"]
                    result["loss_percentage"] = (result["lost"] / result["sent"]) * 100
                    
        except Exception as e:
            result["error"] = str(e)
            result["loss_percentage"] = 100.0  # Assume 100% loss on error
            
        return result
    
    def route_tracing(self, host="google.com"):
        """
        Trace the route to a host.
        
        Args:
            host (str): The host to trace the route to.
            
        Returns:
            list: List of hops with host, IP, and time.
        """
        hops = []
        
        try:
            if self.os_name == "Windows":
                # Windows tracert
                output = subprocess.check_output(f"tracert -d {host}", shell=True).decode()
                
                # Parse tracert output
                for line in output.splitlines():
                    # Skip header lines
                    if "Tracing route" in line or "over a maximum" in line or "Trace complete" in line:
                        continue
                        
                    match = re.search(r"^\s*(\d+)\s+(\d+|[*]+)\s+ms\s+(\d+|[*]+)\s+ms\s+(\d+|[*]+)\s+ms\s+(.+)$", line)
                    if match:
                        hop_num = int(match.group(1))
                        times = [t for t in [match.group(2), match.group(3), match.group(4)] if t != "*"]
                        avg_time = sum(map(float, times)) / len(times) if times else 0
                        ip_or_host = match.group(5).strip()
                        
                        # Try to resolve hostname if it's an IP
                        hostname = ip_or_host
                        try:
                            if re.match(r"^\d+\.\d+\.\d+\.\d+$", ip_or_host):
                                hostname_info = socket.gethostbyaddr(ip_or_host)
                                hostname = hostname_info[0]
                        except:
                            pass
                            
                        hops.append({
                            "hop": hop_num,
                            "host": hostname,
                            "ip": ip_or_host,
                            "time": avg_time
                        })
                        
            else:
                # Linux/macOS traceroute
                output = subprocess.check_output(f"traceroute -n {host}", shell=True).decode()
                
                # Parse traceroute output
                for line in output.splitlines():
                    # Skip header line
                    if "traceroute to" in line:
                        continue
                        
                    match = re.search(r"^\s*(\d+)\s+([^\s]+)(?:\s+\(([^\)]+)\))?\s+(?:([0-9.]+)\s+ms\s+)+", line)
                    if match:
                        hop_num = int(match.group(1))
                        ip = match.group(2)
                        
                        # Extract times
                        times = re.findall(r"([0-9.]+)\s+ms", line)
                        avg_time = sum(map(float, times)) / len(times) if times else 0
                        
                        # Try to resolve hostname if it's an IP
                        hostname = ip
                        try:
                            if re.match(r"^\d+\.\d+\.\d+\.\d+$", ip):
                                hostname_info = socket.gethostbyaddr(ip)
                                hostname = hostname_info[0]
                        except:
                            pass
                            
                        hops.append({
                            "hop": hop_num,
                            "host": hostname,
                            "ip": ip,
                            "time": avg_time
                        })
                        
        except Exception as e:
            hops.append({
                "hop": 1,
                "host": "Error",
                "ip": "Error",
                "time": 0,
                "error": str(e)
            })
            
        return hops
        
    def network_scan(self, subnet="192.168.1.0/24"):
        """
        Escaneia a rede local para encontrar dispositivos conectados.
        
        Este método utiliza ping para verificar quais IPs na rede local
        estão respondendo. Por padrão, escaneia a subrede 192.168.1.0/24,
        mas o usuário pode especificar outra subrede.
        
        Args:
            subnet (str): A subrede a ser escaneada (padrão: 192.168.1.0/24)
            
        Returns:
            dict: Dicionário com resultados do escaneamento contendo IPs e status
        """
        import ipaddress
        import concurrent.futures
        
        results = {"active_devices": [], "total_scanned": 0}
        
        try:
            # Verifica o sistema operacional para determinar o comando ping adequado
            param = '-n' if platform.system().lower() == 'windows' else '-c'
            
            # Função para verificar se um único IP está ativo
            def check_ip(ip):
                ip_str = str(ip)
                # Executa o comando ping com timeout curto
                command = f"ping {param} 1 -w 1 {ip_str}"
                response = os.system(command + " > /dev/null 2>&1")
                
                # Tenta resolver o nome do host
                try:
                    hostname = socket.getfqdn(ip_str)
                    if hostname == ip_str:
                        hostname = "N/A"
                except:
                    hostname = "N/A"
                
                if response == 0:
                    return {"ip": ip_str, "status": "Ativo", "hostname": hostname}
                return None
            
            # Analisa a subrede fornecida
            try:
                network = ipaddress.ip_network(subnet, strict=False)
                total_ips = min(254, len(list(network.hosts())))  # Limita a 254 IPs para evitar escaneamentos muito longos
            except ValueError:
                return {"error": f"Subrede inválida: {subnet}", "active_devices": [], "total_scanned": 0}
            
            # Usa ThreadPoolExecutor para verificar múltiplos IPs simultaneamente
            with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                hosts = list(network.hosts())[:total_ips]
                results["total_scanned"] = len(hosts)
                
                # Exibe barra de progresso enquanto escaneia
                with tqdm(total=len(hosts), desc="Escaneando rede", unit="IP") as pbar:
                    futures = {executor.submit(check_ip, ip): ip for ip in hosts}
                    for future in concurrent.futures.as_completed(futures):
                        result = future.result()
                        if result:
                            results["active_devices"].append(result)
                        pbar.update(1)
            
            # Ordena por endereço IP
            results["active_devices"].sort(key=lambda x: [int(part) for part in x["ip"].split('.')])
            results["total_active"] = len(results["active_devices"])
            
            return results
        except Exception as e:
            return {
                "error": f"Erro ao escanear a rede: {str(e)}",
                "active_devices": [],
                "total_scanned": 0,
                "total_active": 0
            }
