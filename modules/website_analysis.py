"""
Módulo de Análise de Websites

Este módulo avançado fornece funcionalidades para análise completa de websites,
incluindo consulta de IP do domínio, registros DNS, teste de ping, escaneamento de portas,
informações WHOIS e detalhes de certificados SSL.

O módulo é projetado para funcionar com diferentes tipos de domínios e protocolos,
suportando análises de segurança e desempenho.
"""

import socket
import dns.resolver
import subprocess
import re
import whois
import ssl
import OpenSSL
import concurrent.futures
from datetime import datetime
import platform
import json
import time
import traceback

class WebsiteAnalysis:
    def __init__(self, domain):
        self.domain = domain
        self.os_name = platform.system()
        self.timeout = 5  # Timeout padrão em segundos
        self.results_cache = {}  # Cache para resultados de análises
    
    def get_domain_ip(self):
        """
        Get domain IP addresses (IPv4 and IPv6).
        
        Returns:
            dict: IPv4 and IPv6 addresses.
        """
        ip_info = {"IPv4": "Not available", "IPv6": "Not available"}
        
        try:
            # Get IPv4 address
            ipv4 = socket.getaddrinfo(self.domain, None, socket.AF_INET)
            if ipv4:
                ip_info["IPv4"] = ipv4[0][4][0]
        except Exception as e:
            ip_info["IPv4"] = f"Error: {str(e)}"
        
        try:
            # Get IPv6 address
            ipv6 = socket.getaddrinfo(self.domain, None, socket.AF_INET6)
            if ipv6:
                ip_info["IPv6"] = ipv6[0][4][0]
        except Exception as e:
            ip_info["IPv6"] = f"Error: {str(e)}"
            
        return ip_info
    
    def get_dns_records(self):
        """
        Get DNS records for the domain.
        
        Returns:
            dict: Dictionary of DNS records by type.
        """
        dns_records = {}
        record_types = ["A", "AAAA", "MX", "TXT", "NS", "CNAME"]
        
        for record_type in record_types:
            try:
                answers = dns.resolver.resolve(self.domain, record_type)
                dns_records[record_type] = [str(answer) for answer in answers]
            except Exception:
                dns_records[record_type] = ["No records found"]
                
        return dns_records
    
    def ping_test(self):
        """
        Perform a ping test to the domain.
        
        Returns:
            dict: Ping statistics including min, avg, max times and packet loss.
        """
        ping_stats = {"min": 0, "avg": 0, "max": 0, "packet_loss": 0}
        
        try:
            if self.os_name == "Windows":
                # Windows ping
                output = subprocess.check_output(f"ping {self.domain} -n 4", shell=True).decode()
                
                # Extract packet loss
                loss_match = re.search(r"Lost = (\d+)", output)
                if loss_match:
                    ping_stats["packet_loss"] = int(loss_match.group(1)) * 25  # 1 lost packet = 25% loss
                
                # Extract times
                times_match = re.search(r"Minimum = (\d+)ms, Maximum = (\d+)ms, Average = (\d+)ms", output)
                if times_match:
                    ping_stats["min"] = int(times_match.group(1))
                    ping_stats["max"] = int(times_match.group(2))
                    ping_stats["avg"] = int(times_match.group(3))
                    
            else:
                # Linux/macOS ping
                output = subprocess.check_output(f"ping -c 4 {self.domain}", shell=True).decode()
                
                # Extract packet loss
                loss_match = re.search(r"(\d+)% packet loss", output)
                if loss_match:
                    ping_stats["packet_loss"] = int(loss_match.group(1))
                
                # Extract times
                times_match = re.search(r"min/avg/max/[^=]+ = (\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)", output)
                if times_match:
                    ping_stats["min"] = float(times_match.group(1))
                    ping_stats["avg"] = float(times_match.group(2))
                    ping_stats["max"] = float(times_match.group(3))
                    
        except Exception as e:
            ping_stats = {
                "min": 0,
                "avg": 0,
                "max": 0,
                "packet_loss": 100,
                "error": str(e)
            }
            
        return ping_stats
    
    def scan_single_port(self, port):
        """
        Scan a single port to check if it's open.
        
        Args:
            port (int): The port number to scan.
            
        Returns:
            tuple: (port, status) where status is "Open" or "Closed".
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((self.domain, port))
        if result == 0:
            sock.close()
            return (port, "Open")
        else:
            sock.close()
            return (port, "Closed")
    
    def scan_ports(self, ports):
        """
        Scan multiple ports to check if they're open.
        
        Args:
            ports (list): List of port numbers to scan.
            
        Returns:
            dict: Dictionary with port numbers as keys and status as values.
        """
        results = {}
        
        # Use thread pool to scan ports concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_port = {executor.submit(self.scan_single_port, port): port for port in ports}
            for future in concurrent.futures.as_completed(future_to_port):
                port, status = future.result()
                results[port] = status
                
        return results
    
    def get_whois_info(self):
        """
        Get WHOIS information for the domain.
        
        Returns:
            dict: WHOIS information.
        """
        whois_info = {}
        
        try:
            w = whois.whois(self.domain)
            
            # Extract relevant information
            whois_info = {
                "Registrar": w.registrar if hasattr(w, 'registrar') else "Unknown",
                "WHOIS Server": w.whois_server if hasattr(w, 'whois_server') else "Unknown",
                "Creation Date": self._format_date(w.creation_date),
                "Expiration Date": self._format_date(w.expiration_date),
                "Updated Date": self._format_date(w.updated_date),
                "Name Servers": ", ".join(w.name_servers) if hasattr(w, 'name_servers') and isinstance(w.name_servers, list) else "Unknown"
            }
            
        except Exception as e:
            whois_info = {"Error": str(e)}
            
        return whois_info
    
    def _format_date(self, date_obj):
        """
        Format a date object or list of date objects to a string.
        
        Args:
            date_obj: Date object or list of date objects.
            
        Returns:
            str: Formatted date string.
        """
        if date_obj is None:
            return "Unknown"
            
        if isinstance(date_obj, list):
            date_obj = date_obj[0]  # Take first date if it's a list
            
        if isinstance(date_obj, datetime):
            return date_obj.strftime("%Y-%m-%d %H:%M:%S")
            
        return str(date_obj)
    
    def get_ssl_info(self):
        """
        Get SSL certificate details for the domain.
        
        Returns:
            dict: SSL certificate information or error message.
        """
        try:
            context = ssl.create_default_context()
            with socket.create_connection((self.domain, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=self.domain) as ssock:
                    cert = ssock.getpeercert()
                    
                    # Extract certificate information
                    cert_info = {
                        "Subject": ", ".join([f"{key}={value}" for key, value in cert['subject'][0]]),
                        "Issuer": ", ".join([f"{key}={value}" for key, value in cert['issuer'][0]]),
                        "Version": cert['version'],
                        "Serial Number": cert['serialNumber'],
                        "Not Before": cert['notBefore'],
                        "Not After": cert['notAfter'],
                    }
                    
                    # Check certificate validity
                    not_after = datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
                    if not_after < datetime.now():
                        cert_info["Status"] = "Expired"
                    else:
                        cert_info["Status"] = "Valid"
                        
                    return cert_info
                    
        except ssl.SSLError as e:
            return f"SSL Error: {str(e)}"
        except socket.error as e:
            return f"Socket Error: {str(e)}"
        except Exception as e:
            return f"Error: {str(e)}"
