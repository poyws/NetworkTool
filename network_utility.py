#!/usr/bin/env python3
"""
Utilitário de Rede Avançado - CLI

Uma ferramenta de linha de comando completa para análise de redes,
fornecendo informações detalhadas sobre o sistema, análise de websites,
e diagnósticos de conectividade de rede.

Desenvolvido com Python, o utilitário combina múltiplas funcionalidades:
- Verificação de IP local e público
- Informações detalhadas das interfaces de rede
- Análise de domínios e websites (DNS, ping, portas, WHOIS, certificados SSL)
- Diagnósticos de rede (teste de velocidade, latência, perda de pacotes, rota)
- Exportação de resultados em vários formatos

Versão: 2.0
"""

import os
import sys
import click
import pyfiglet
from colorama import init, Fore, Style, Back
import time
import socket
import platform
from datetime import datetime

from modules.system_info import SystemInfo
from modules.website_analysis import WebsiteAnalysis
from modules.network_diagnostics import NetworkDiagnostics
from modules.ui_components import (
    display_banner, 
    display_menu, 
    display_loading, 
    display_error, 
    confirm_action, 
    display_success, 
    display_result_table, 
    display_multi_result
)
from modules.export import export_results

init(autoreset=True)

command_history = []
VERSION = "2.0"
AUTHOR = "Network Utility Team"

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """Network Utility Script - A comprehensive network analysis tool."""
    if ctx.invoked_subcommand is None:
        main_menu()

@cli.command()
def system():
    """Display detailed system network information."""
    display_banner("System Information")
    
    # Add to command history
    command_history.append(("system", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    
    system_info = SystemInfo()
    
    click.echo(Fore.CYAN + "\n[1/6] Getting local IP addresses..." + Style.RESET_ALL)
    display_loading(1)
    local_ips = system_info.get_local_ip()
    
    click.echo(Fore.CYAN + "\n[2/6] Getting public IP address..." + Style.RESET_ALL)
    display_loading(1)
    public_ip = system_info.get_public_ip()
    
    click.echo(Fore.CYAN + "\n[3/6] Getting MAC address..." + Style.RESET_ALL)
    display_loading(1)
    mac_address = system_info.get_mac_address()
    
    click.echo(Fore.CYAN + "\n[4/6] Getting network interface details..." + Style.RESET_ALL)
    display_loading(2)
    interfaces = system_info.get_network_interfaces()
    
    click.echo(Fore.CYAN + "\n[5/6] Getting network speed..." + Style.RESET_ALL)
    display_loading(2)
    speed = system_info.get_network_speed()
    
    click.echo(Fore.CYAN + "\n[6/6] Getting DNS servers..." + Style.RESET_ALL)
    display_loading(1)
    dns_servers = system_info.get_dns_servers()
    
    # Compile results
    results = {
        "Local IPs": local_ips,
        "Public IP": public_ip,
        "MAC Address": mac_address,
        "Network Interfaces": interfaces,
        "Network Speed": speed,
        "DNS Servers": dns_servers
    }
    
    # Display results
    click.echo("\n" + "="*50)
    click.echo(Fore.GREEN + "SYSTEM NETWORK INFORMATION" + Style.RESET_ALL)
    click.echo("="*50 + "\n")
    
    click.echo(Fore.YELLOW + "LOCAL IP ADDRESSES:" + Style.RESET_ALL)
    for ip_type, ip in results["Local IPs"].items():
        click.echo(f"  {ip_type}: {ip}")
    
    click.echo(Fore.YELLOW + "\nPUBLIC IP ADDRESS:" + Style.RESET_ALL)
    click.echo(f"  {results['Public IP']}")
    
    click.echo(Fore.YELLOW + "\nMAC ADDRESS:" + Style.RESET_ALL)
    click.echo(f"  {results['MAC Address']}")
    
    click.echo(Fore.YELLOW + "\nNETWORK INTERFACES:" + Style.RESET_ALL)
    for interface in results["Network Interfaces"]:
        click.echo(f"  - {interface}")
    
    click.echo(Fore.YELLOW + "\nCURRENT NETWORK SPEED:" + Style.RESET_ALL)
    click.echo(f"  Download: {results['Network Speed']['download']} Mbps")
    click.echo(f"  Upload: {results['Network Speed']['upload']} Mbps")
    
    click.echo(Fore.YELLOW + "\nDNS SERVERS:" + Style.RESET_ALL)
    for server in results["DNS Servers"]:
        click.echo(f"  - {server}")
    
    # Ask for export
    if confirm_action("\nDo you want to export these results?"):
        filename = export_results(results, "system_info")
        display_success(f"Results exported to {filename}")
    
    if confirm_action("\nReturn to main menu?"):
        main_menu()
    else:
        sys.exit(0)

@cli.command()
@click.option('--domain', '-d', prompt='Enter domain name', help='Domain to analyze')
def website(domain):
    """Analyze website information."""
    display_banner("Website Analysis")
    
    # Add to command history
    command_history.append(("website", domain, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    
    analyzer = WebsiteAnalysis(domain)
    results = {}
    
    # Menu for website analysis
    while True:
        # Header com estilo minimalista
        click.echo("\n" + Fore.WHITE + Style.DIM + "─"*50 + Style.RESET_ALL)
        click.echo(Fore.WHITE + Style.BRIGHT + f"WEBSITE ANALYSIS FOR: {domain}" + Style.RESET_ALL)
        click.echo(Fore.WHITE + Style.DIM + "─"*50 + Style.RESET_ALL + "\n")
        
        options = [
            "1. Domain IP Lookup",
            "2. DNS Records",
            "3. Ping Test",
            "4. Port Scanning",
            "5. WHOIS Information",
            "6. SSL Certificate Details",
            "7. Run All Analyses",
            "8. Export Results",
            "9. Back to Main Menu",
            "0. Exit"
        ]
        
        choice = display_menu("Select an option:", options)
        
        if choice == "1":
            click.echo(Fore.CYAN + "\nPerforming Domain IP Lookup..." + Style.RESET_ALL)
            display_loading(1)
            ip_info = analyzer.get_domain_ip()
            results["Domain IP"] = ip_info
            click.echo(Fore.YELLOW + "\nDOMAIN IP LOOKUP:" + Style.RESET_ALL)
            for ip_type, ip in ip_info.items():
                click.echo(f"  {ip_type}: {ip}")
                
        elif choice == "2":
            click.echo(Fore.CYAN + "\nGetting DNS Records..." + Style.RESET_ALL)
            display_loading(2)
            dns_records = analyzer.get_dns_records()
            results["DNS Records"] = dns_records
            click.echo(Fore.YELLOW + "\nDNS RECORDS:" + Style.RESET_ALL)
            for record_type, records in dns_records.items():
                click.echo(f"  {record_type}:")
                for record in records:
                    click.echo(f"    - {record}")
                    
        elif choice == "3":
            click.echo(Fore.CYAN + "\nPerforming Ping Test..." + Style.RESET_ALL)
            display_loading(2)
            ping_results = analyzer.ping_test()
            results["Ping Test"] = ping_results
            click.echo(Fore.YELLOW + "\nPING TEST RESULTS:" + Style.RESET_ALL)
            click.echo(f"  Min: {ping_results['min']} ms")
            click.echo(f"  Avg: {ping_results['avg']} ms")
            click.echo(f"  Max: {ping_results['max']} ms")
            click.echo(f"  Packet Loss: {ping_results['packet_loss']}%")
            
        elif choice == "4":
            ports = click.prompt("Enter ports to scan (comma-separated, e.g. 80,443,8080)", default="80,443,8080,21,22,25,3306")
            port_list = [int(p.strip()) for p in ports.split(",")]
            
            click.echo(Fore.CYAN + f"\nScanning ports {ports}..." + Style.RESET_ALL)
            display_loading(3)
            port_results = analyzer.scan_ports(port_list)
            results["Port Scan"] = port_results
            
            click.echo(Fore.YELLOW + "\nPORT SCAN RESULTS:" + Style.RESET_ALL)
            for port, status in port_results.items():
                status_color = Fore.GREEN if status == "Open" else Fore.RED
                click.echo(f"  Port {port}: {status_color}{status}{Style.RESET_ALL}")
                
        elif choice == "5":
            click.echo(Fore.CYAN + "\nGetting WHOIS Information..." + Style.RESET_ALL)
            display_loading(2)
            whois_info = analyzer.get_whois_info()
            results["WHOIS Info"] = whois_info
            
            click.echo(Fore.YELLOW + "\nWHOIS INFORMATION:" + Style.RESET_ALL)
            for key, value in whois_info.items():
                click.echo(f"  {key}: {value}")
                
        elif choice == "6":
            click.echo(Fore.CYAN + "\nChecking SSL Certificate..." + Style.RESET_ALL)
            display_loading(2)
            ssl_info = analyzer.get_ssl_info()
            results["SSL Info"] = ssl_info
            
            click.echo(Fore.YELLOW + "\nSSL CERTIFICATE DETAILS:" + Style.RESET_ALL)
            if isinstance(ssl_info, dict):
                for key, value in ssl_info.items():
                    click.echo(f"  {key}: {value}")
            else:
                click.echo(f"  {ssl_info}")
                
        elif choice == "7":
            click.echo(Fore.CYAN + "\nRunning All Analyses..." + Style.RESET_ALL)
            
            click.echo(Fore.CYAN + "\n[1/6] Domain IP Lookup..." + Style.RESET_ALL)
            display_loading(1)
            results["Domain IP"] = analyzer.get_domain_ip()
            
            click.echo(Fore.CYAN + "\n[2/6] DNS Records..." + Style.RESET_ALL)
            display_loading(1)
            results["DNS Records"] = analyzer.get_dns_records()
            
            click.echo(Fore.CYAN + "\n[3/6] Ping Test..." + Style.RESET_ALL)
            display_loading(1)
            results["Ping Test"] = analyzer.ping_test()
            
            click.echo(Fore.CYAN + "\n[4/6] Port Scanning (common ports)..." + Style.RESET_ALL)
            display_loading(2)
            results["Port Scan"] = analyzer.scan_ports([80, 443, 8080, 21, 22, 25, 3306])
            
            click.echo(Fore.CYAN + "\n[5/6] WHOIS Information..." + Style.RESET_ALL)
            display_loading(1)
            results["WHOIS Info"] = analyzer.get_whois_info()
            
            click.echo(Fore.CYAN + "\n[6/6] SSL Certificate..." + Style.RESET_ALL)
            display_loading(1)
            results["SSL Info"] = analyzer.get_ssl_info()
            
            # Display combined results
            display_banner(f"Analysis Results: {domain}")
            
            click.echo(Fore.YELLOW + "\nDOMAIN IP LOOKUP:" + Style.RESET_ALL)
            for ip_type, ip in results["Domain IP"].items():
                click.echo(f"  {ip_type}: {ip}")
            
            click.echo(Fore.YELLOW + "\nDNS RECORDS:" + Style.RESET_ALL)
            for record_type, records in results["DNS Records"].items():
                click.echo(f"  {record_type}:")
                for record in records:
                    click.echo(f"    - {record}")
            
            click.echo(Fore.YELLOW + "\nPING TEST RESULTS:" + Style.RESET_ALL)
            click.echo(f"  Min: {results['Ping Test']['min']} ms")
            click.echo(f"  Avg: {results['Ping Test']['avg']} ms")
            click.echo(f"  Max: {results['Ping Test']['max']} ms")
            click.echo(f"  Packet Loss: {results['Ping Test']['packet_loss']}%")
            
            click.echo(Fore.YELLOW + "\nPORT SCAN RESULTS:" + Style.RESET_ALL)
            for port, status in results["Port Scan"].items():
                status_color = Fore.GREEN if status == "Open" else Fore.RED
                click.echo(f"  Port {port}: {status_color}{status}{Style.RESET_ALL}")
            
            click.echo(Fore.YELLOW + "\nWHOIS INFORMATION:" + Style.RESET_ALL)
            for key, value in results["WHOIS Info"].items():
                click.echo(f"  {key}: {value}")
            
            click.echo(Fore.YELLOW + "\nSSL CERTIFICATE DETAILS:" + Style.RESET_ALL)
            if isinstance(results["SSL Info"], dict):
                for key, value in results["SSL Info"].items():
                    click.echo(f"  {key}: {value}")
            else:
                click.echo(f"  {results['SSL Info']}")
                
        elif choice == "8":
            if not results:
                display_error("No results to export. Run some analyses first.")
                continue
                
            filename = export_results(results, f"website_analysis_{domain}")
            display_success(f"Results exported to {filename}")
            
        elif choice == "9":
            main_menu()
            return
            
        elif choice == "0":
            sys.exit(0)
            
        else:
            display_error("Invalid option. Please try again.")

@cli.command()
def diagnostics():
    """Perform network diagnostics."""
    display_banner("Network Diagnostics")
    
    # Add to command history
    command_history.append(("diagnostics", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    
    diagnostic = NetworkDiagnostics()
    results = {}
    
    # Menu for network diagnostics
    while True:
        # Header com estilo minimalista
        click.echo("\n" + Fore.WHITE + Style.DIM + "─"*50 + Style.RESET_ALL)
        click.echo(Fore.WHITE + Style.BRIGHT + "NETWORK DIAGNOSTICS" + Style.RESET_ALL)
        click.echo(Fore.WHITE + Style.DIM + "─"*50 + Style.RESET_ALL + "\n")
        
        options = [
            "1. Network Speed Test",
            "2. Latency Check",
            "3. Packet Loss Analysis",
            "4. Route Tracing",
            "5. Network Scan",
            "6. Run All Diagnostics",
            "7. Export Results",
            "8. Back to Main Menu",
            "0. Exit"
        ]
        
        choice = display_menu("Select an option:", options)
        
        if choice == "1":
            click.echo(Fore.CYAN + "\nRealizando Teste de Velocidade da Rede..." + Style.RESET_ALL)
            display_loading(5)
            speed_results = diagnostic.speed_test()
            results["Speed Test"] = speed_results
            
            # Usar a nova função de exibição de resultados
            display_result_table("RESULTADOS DO TESTE DE VELOCIDADE", speed_results, include_units=True)
            
        elif choice == "2":
            host = click.prompt("Enter host to check latency (default: google.com)", default="google.com")
            click.echo(Fore.CYAN + f"\nChecking Latency to {host}..." + Style.RESET_ALL)
            display_loading(3)
            latency_results = diagnostic.latency_check(host)
            results["Latency Check"] = latency_results
            
            # Usar a nova função de exibição de resultados
            display_result_table(f"LATENCY CHECK RESULTS ({host})", latency_results, include_units=True)
            
        elif choice == "3":
            host = click.prompt("Enter host for packet loss analysis (default: google.com)", default="google.com")
            packets = click.prompt("Number of packets to send", default=50, type=int)
            
            click.echo(Fore.CYAN + f"\nPerforming Packet Loss Analysis ({packets} packets to {host})..." + Style.RESET_ALL)
            display_loading(4)
            packet_results = diagnostic.packet_loss_analysis(host, packets)
            results["Packet Loss"] = packet_results
            
            # Usar a nova função de exibição de resultados
            display_result_table(f"PACKET LOSS ANALYSIS RESULTS ({host})", packet_results, include_units=True)
            
        elif choice == "4":
            host = click.prompt("Enter host to trace route (default: google.com)", default="google.com")
            
            click.echo(Fore.CYAN + f"\nTracing Route to {host}..." + Style.RESET_ALL)
            display_loading(6)
            route_results = diagnostic.route_tracing(host)
            results["Route Tracing"] = route_results
            
            click.echo(Fore.YELLOW + f"\nROUTE TRACING RESULTS ({host}):" + Style.RESET_ALL)
            for hop in route_results:
                click.echo(f"  Hop {hop['hop']}: {hop['host']} ({hop['ip']}) - {hop['time']} ms")
                
        elif choice == "5":
            # Network Scan
            subnet = click.prompt("Enter subnet to scan (default: 192.168.1.0/24)", default="192.168.1.0/24")
            click.echo(Fore.CYAN + f"\nEscaneando dispositivos na rede {subnet}..." + Style.RESET_ALL)
            
            scan_results = diagnostic.network_scan(subnet)
            results["Network Scan"] = scan_results
            
            # Exibe resultados
            click.echo(Fore.YELLOW + f"\nRESULTADOS DO ESCANEAMENTO DE REDE ({subnet}):" + Style.RESET_ALL)
            click.echo(f"  Total de IPs escaneados: {scan_results['total_scanned']}")
            
            if "error" in scan_results:
                click.echo(Fore.RED + f"  Erro: {scan_results['error']}" + Style.RESET_ALL)
            else:
                click.echo(f"  Dispositivos ativos encontrados: {len(scan_results['active_devices'])}")
                
                if scan_results['active_devices']:
                    click.echo("\n  " + Fore.GREEN + "DISPOSITIVOS ATIVOS:" + Style.RESET_ALL)
                    for device in scan_results['active_devices']:
                        hostname = device['hostname']
                        hostname_display = f" ({hostname})" if hostname != "N/A" else ""
                        click.echo(f"    • {device['ip']}{hostname_display} - {device['status']}")
                else:
                    click.echo("\n  " + Fore.YELLOW + "Nenhum dispositivo ativo encontrado na rede." + Style.RESET_ALL)
                    
        elif choice == "6":
            click.echo(Fore.CYAN + "\nRunning All Diagnostics..." + Style.RESET_ALL)
            
            click.echo(Fore.CYAN + "\n[1/5] Network Speed Test..." + Style.RESET_ALL)
            display_loading(5)
            results["Speed Test"] = diagnostic.speed_test()
            
            click.echo(Fore.CYAN + "\n[2/5] Latency Check (google.com)..." + Style.RESET_ALL)
            display_loading(3)
            results["Latency Check"] = diagnostic.latency_check("google.com")
            
            click.echo(Fore.CYAN + "\n[3/5] Packet Loss Analysis (google.com)..." + Style.RESET_ALL)
            display_loading(4)
            results["Packet Loss"] = diagnostic.packet_loss_analysis("google.com", 50)
            
            click.echo(Fore.CYAN + "\n[4/5] Route Tracing (google.com)..." + Style.RESET_ALL)
            display_loading(6)
            results["Route Tracing"] = diagnostic.route_tracing("google.com")
            
            click.echo(Fore.CYAN + "\n[5/5] Network Scan (local)..." + Style.RESET_ALL)
            results["Network Scan"] = diagnostic.network_scan()
            
            # Display combined results
            display_banner("Network Diagnostics Results")
            
            # Usar a função de exibição de resultados múltiplos para mostrar todos os resultados
            diagnostic_results = [
                {
                    'title': 'NETWORK SPEED TEST RESULTS',
                    'data': results['Speed Test']
                },
                {
                    'title': 'LATENCY CHECK RESULTS (google.com)',
                    'data': results['Latency Check']
                },
                {
                    'title': 'PACKET LOSS ANALYSIS RESULTS (google.com)',
                    'data': results['Packet Loss']
                }
            ]
            
            # Exibir todos os resultados em um formato consistente
            display_multi_result("DIAGNOSTIC SUMMARY", diagnostic_results)
            
            # Resultados de rastreamento de rota com estilo minimalista
            click.echo("\n" + Fore.WHITE + Style.DIM + "─"*50 + Style.RESET_ALL)
            click.echo(Fore.WHITE + Style.BRIGHT + "ROUTE TRACING RESULTS (google.com)" + Style.RESET_ALL)
            click.echo(Fore.WHITE + Style.DIM + "─"*50 + Style.RESET_ALL + "\n")
            
            for hop in results["Route Tracing"]:
                click.echo(Fore.WHITE + f"  Hop {hop['hop']}: " + 
                           Style.BRIGHT + f"{hop['host']}" + Style.RESET_ALL + 
                           Fore.WHITE + Style.DIM + f" ({hop['ip']})" + Style.RESET_ALL +
                           f" - {hop['time']} ms")
            
            # Exibe resultados do escaneamento de rede
            scan_results = results["Network Scan"]
            click.echo("\n" + Fore.WHITE + Style.DIM + "─"*50 + Style.RESET_ALL)
            click.echo(Fore.WHITE + Style.BRIGHT + "NETWORK SCAN RESULTS" + Style.RESET_ALL)
            click.echo(Fore.WHITE + Style.DIM + "─"*50 + Style.RESET_ALL + "\n")
            
            click.echo(Fore.WHITE + f"  Total de IPs escaneados: " + Style.BRIGHT + f"{scan_results['total_scanned']}" + Style.RESET_ALL)
            
            if "error" in scan_results:
                click.echo(Fore.WHITE + Style.DIM + f"  Erro: {scan_results['error']}" + Style.RESET_ALL)
            else:
                click.echo(Fore.WHITE + f"  Dispositivos ativos encontrados: " + 
                           Style.BRIGHT + f"{len(scan_results['active_devices'])}" + Style.RESET_ALL)
                
                # Exibir detalhes dos dispositivos ativos
                if len(scan_results['active_devices']) > 0:
                    click.echo(Fore.WHITE + Style.DIM + "\n  Dispositivos ativos:" + Style.RESET_ALL)
                    for i, device in enumerate(scan_results['active_devices'], 1):
                        click.echo(Fore.WHITE + f"    {i}. " + Style.BRIGHT + f"{device['ip']}" + Style.RESET_ALL + 
                                  Fore.WHITE + Style.DIM + f" {device.get('hostname', 'Desconhecido')}" + Style.RESET_ALL)
                
        elif choice == "7":
            if not results:
                display_error("No results to export. Run some diagnostics first.")
                continue
                
            filename = export_results(results, "network_diagnostics")
            display_success(f"Results exported to {filename}")
            
        elif choice == "8":
            main_menu()
            return
            
        elif choice == "0":
            sys.exit(0)
            
        else:
            display_error("Invalid option. Please try again.")

@cli.command()
def history():
    """Display command history."""
    display_banner("Command History")
    
    # Header com estilo minimalista
    click.echo("\n" + Fore.WHITE + Style.DIM + "─"*50 + Style.RESET_ALL)
    click.echo(Fore.WHITE + Style.BRIGHT + "COMMAND HISTORY" + Style.RESET_ALL)
    click.echo(Fore.WHITE + Style.DIM + "─"*50 + Style.RESET_ALL + "\n")
    
    if not command_history:
        click.echo(Fore.WHITE + Style.DIM + "No commands have been executed yet." + Style.RESET_ALL)
    else:
        for i, cmd in enumerate(command_history, 1):
            if len(cmd) == 2:  # Commands without additional parameters
                command, timestamp = cmd
                click.echo(Fore.WHITE + f"{i}. " + Fore.WHITE + Style.DIM + f"[{timestamp}]" + 
                          Style.RESET_ALL + f" {command}")
            else:  # Commands with additional parameters
                command, param, timestamp = cmd
                click.echo(Fore.WHITE + f"{i}. " + Fore.WHITE + Style.DIM + f"[{timestamp}]" + 
                          Style.RESET_ALL + f" {command} - {param}")
    
    click.echo("\nPress Enter to return to main menu...")
    input()
    main_menu()

def main_menu():
    """Display the main menu and handle user input."""
    os.system('cls' if os.name == 'nt' else 'clear')
    display_banner("Network Utility Tool")
    
    options = [
        "1. System Network Information",
        "2. Website Analysis",
        "3. Network Diagnostics",
        "4. Command History",
        "0. Exit"
    ]
    
    choice = display_menu("Select an option:", options)
    
    if choice == "1":
        system()
    elif choice == "2":
        domain = input(Fore.WHITE + Style.DIM + "Enter domain name: " + Style.RESET_ALL)
        website(domain)
    elif choice == "3":
        diagnostics()
    elif choice == "4":
        history()
    elif choice == "0":
        click.echo(Fore.WHITE + Style.DIM + "\nThank you for using Network Utility Tool. Goodbye!" + Style.RESET_ALL)
        sys.exit(0)
    else:
        display_error("Invalid option. Please try again.")
        main_menu()

# Register commands
cli.add_command(system)
cli.add_command(website)
cli.add_command(diagnostics)
cli.add_command(history)

if __name__ == "__main__":
    try:
        cli()  # Use the Click CLI functionality
    except KeyboardInterrupt:
        click.echo(Fore.WHITE + Style.DIM + "\n\nOperation cancelled by user. Exiting..." + Style.RESET_ALL)
        sys.exit(0)
    except Exception as e:
        display_error(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)
