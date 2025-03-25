#!/usr/bin/env python3
"""
Network Utility Script - A comprehensive CLI network utility

This script provides a suite of network tools including system information display,
website analysis, and network diagnostics capabilities with an interactive menu system.
"""

import os
import sys
import time
import click
import readline  # For command history support

from modules.ui import (
    display_main_menu, 
    display_submenu, 
    display_banner, 
    print_color, 
    print_loading,
    print_result,
    print_error,
    get_user_selection,
    display_progress
)
from modules.system_info import (
    get_local_ip, 
    get_public_ip, 
    get_mac_address, 
    get_network_interfaces,
    get_network_speed,
    get_dns_servers
)
from modules.website_analysis import (
    domain_ip_lookup,
    get_dns_records,
    ping_test,
    port_scan,
    get_whois_info,
    get_ssl_certificate
)
from modules.network_diagnostics import (
    run_speed_test,
    check_latency,
    analyze_packet_loss,
    trace_route
)
from modules.export import export_results

# Initialize command history
command_history = []

# Store results for potential export
current_results = {}

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def system_info_menu():
    """Display system information submenu and handle selections."""
    while True:
        clear_screen()
        options = [
            "Local IP Address (IPv4 & IPv6)",
            "Public IP Address",
            "MAC Address",
            "Network Interface Details",
            "Current Network Speed",
            "DNS Servers",
            "All System Information",
            "Back to Main Menu"
        ]
        
        choice = display_submenu("System Network Information", options)
        command_history.append(f"System Info: {options[choice-1]}")
        
        if choice == 8:
            break
        
        # Display the appropriate system information
        clear_screen()
        
        if choice == 1:
            result = get_local_ip()
            print_result("Local IP Addresses", result)
            current_results["Local IP Addresses"] = result
        
        elif choice == 2:
            with display_progress("Retrieving public IP..."):
                result = get_public_ip()
            print_result("Public IP Address", result)
            current_results["Public IP Address"] = result
        
        elif choice == 3:
            result = get_mac_address()
            print_result("MAC Address", result)
            current_results["MAC Address"] = result
        
        elif choice == 4:
            result = get_network_interfaces()
            print_result("Network Interface Details", result)
            current_results["Network Interface Details"] = result
        
        elif choice == 5:
            result = get_network_speed()
            print_result("Current Network Speed", result)
            current_results["Current Network Speed"] = result
        
        elif choice == 6:
            result = get_dns_servers()
            print_result("DNS Servers", result)
            current_results["DNS Servers"] = result
        
        elif choice == 7:
            # Get all system information
            results = {}
            print_loading("Gathering all system information...")
            
            results["Local IP Addresses"] = get_local_ip()
            results["Public IP Address"] = get_public_ip()
            results["MAC Address"] = get_mac_address()
            results["Network Interface Details"] = get_network_interfaces()
            results["Current Network Speed"] = get_network_speed()
            results["DNS Servers"] = get_dns_servers()
            
            for title, data in results.items():
                print_result(title, data)
                current_results[title] = data
        
        input("\nPress Enter to continue...")

def website_analysis_menu():
    """Display website analysis submenu and handle selections."""
    while True:
        clear_screen()
        options = [
            "Domain IP Lookup",
            "DNS Records",
            "Ping Test",
            "Port Scanning",
            "WHOIS Information",
            "SSL Certificate Details",
            "Complete Website Analysis",
            "Back to Main Menu"
        ]
        
        choice = display_submenu("Website Analysis", options)
        
        if choice == 8:
            break
        
        # Ask for domain
        clear_screen()
        display_banner("Website Analysis")
        domain = input("Enter domain name (e.g. example.com): ").strip()
        
        if not domain:
            print_error("Domain name cannot be empty.")
            input("\nPress Enter to continue...")
            continue
        
        command_history.append(f"Website Analysis: {options[choice-1]} for {domain}")
        
        # Perform the selected analysis
        if choice == 1:
            with display_progress(f"Looking up IP for {domain}..."):
                result = domain_ip_lookup(domain)
            print_result(f"IP Lookup for {domain}", result)
            current_results[f"IP Lookup for {domain}"] = result
        
        elif choice == 2:
            with display_progress(f"Retrieving DNS records for {domain}..."):
                result = get_dns_records(domain)
            print_result(f"DNS Records for {domain}", result)
            current_results[f"DNS Records for {domain}"] = result
        
        elif choice == 3:
            with display_progress(f"Pinging {domain}..."):
                result = ping_test(domain)
            print_result(f"Ping Test for {domain}", result)
            current_results[f"Ping Test for {domain}"] = result
        
        elif choice == 4:
            ports = input("Enter ports to scan (e.g. 80,443,8080) or leave empty for common ports: ").strip()
            ports = [int(p) for p in ports.split(',')] if ports else None
            
            with display_progress(f"Scanning ports on {domain}..."):
                result = port_scan(domain, ports)
            print_result(f"Port Scan for {domain}", result)
            current_results[f"Port Scan for {domain}"] = result
        
        elif choice == 5:
            with display_progress(f"Retrieving WHOIS information for {domain}..."):
                result = get_whois_info(domain)
            print_result(f"WHOIS Information for {domain}", result)
            current_results[f"WHOIS Information for {domain}"] = result
        
        elif choice == 6:
            with display_progress(f"Analyzing SSL certificate for {domain}..."):
                result = get_ssl_certificate(domain)
            print_result(f"SSL Certificate for {domain}", result)
            current_results[f"SSL Certificate for {domain}"] = result
        
        elif choice == 7:
            # Complete analysis
            results = {}
            print_loading(f"Performing complete analysis on {domain}...")
            
            print_loading("Step 1/6: IP Lookup")
            results[f"IP Lookup for {domain}"] = domain_ip_lookup(domain)
            
            print_loading("Step 2/6: DNS Records")
            results[f"DNS Records for {domain}"] = get_dns_records(domain)
            
            print_loading("Step 3/6: Ping Test")
            results[f"Ping Test for {domain}"] = ping_test(domain)
            
            print_loading("Step 4/6: Port Scan (Common Ports)")
            results[f"Port Scan for {domain}"] = port_scan(domain)
            
            print_loading("Step 5/6: WHOIS Information")
            results[f"WHOIS Information for {domain}"] = get_whois_info(domain)
            
            print_loading("Step 6/6: SSL Certificate Analysis")
            results[f"SSL Certificate for {domain}"] = get_ssl_certificate(domain)
            
            for title, data in results.items():
                print_result(title, data)
                current_results[title] = data
        
        input("\nPress Enter to continue...")

def network_diagnostics_menu():
    """Display network diagnostics submenu and handle selections."""
    while True:
        clear_screen()
        options = [
            "Network Speed Test",
            "Latency Check",
            "Packet Loss Analysis",
            "Route Tracing",
            "Complete Network Diagnostics",
            "Back to Main Menu"
        ]
        
        choice = display_submenu("Network Diagnostics", options)
        command_history.append(f"Network Diagnostics: {options[choice-1]}")
        
        if choice == 6:
            break
        
        # Perform the selected diagnostic
        clear_screen()
        
        if choice == 1:
            with display_progress("Running network speed test..."):
                result = run_speed_test()
            print_result("Network Speed Test", result)
            current_results["Network Speed Test"] = result
        
        elif choice == 2:
            target = input("Enter target hostname/IP (default: 8.8.8.8): ").strip() or "8.8.8.8"
            with display_progress(f"Checking latency to {target}..."):
                result = check_latency(target)
            print_result(f"Latency Check to {target}", result)
            current_results[f"Latency Check to {target}"] = result
        
        elif choice == 3:
            target = input("Enter target hostname/IP (default: 8.8.8.8): ").strip() or "8.8.8.8"
            with display_progress(f"Analyzing packet loss to {target}..."):
                result = analyze_packet_loss(target)
            print_result(f"Packet Loss Analysis to {target}", result)
            current_results[f"Packet Loss Analysis to {target}"] = result
        
        elif choice == 4:
            target = input("Enter target hostname/IP: ").strip()
            if not target:
                print_error("Target cannot be empty.")
                input("\nPress Enter to continue...")
                continue
                
            with display_progress(f"Tracing route to {target}..."):
                result = trace_route(target)
            print_result(f"Route Trace to {target}", result)
            current_results[f"Route Trace to {target}"] = result
        
        elif choice == 5:
            # Complete diagnostics
            results = {}
            target = input("Enter target hostname/IP (default: 8.8.8.8): ").strip() or "8.8.8.8"
            
            print_loading("Running complete network diagnostics...")
            
            print_loading("Step 1/4: Network Speed Test")
            results["Network Speed Test"] = run_speed_test()
            
            print_loading(f"Step 2/4: Latency Check to {target}")
            results[f"Latency Check to {target}"] = check_latency(target)
            
            print_loading(f"Step 3/4: Packet Loss Analysis to {target}")
            results[f"Packet Loss Analysis to {target}"] = analyze_packet_loss(target)
            
            print_loading(f"Step 4/4: Route Tracing to {target}")
            results[f"Route Trace to {target}"] = trace_route(target)
            
            for title, data in results.items():
                print_result(title, data)
                current_results[title] = data
        
        input("\nPress Enter to continue...")

def view_command_history():
    """Display command history."""
    clear_screen()
    display_banner("Command History")
    
    if not command_history:
        print_color("No commands in history.", "yellow")
    else:
        for i, cmd in enumerate(command_history, 1):
            print_color(f"{i}. {cmd}", "cyan")
    
    input("\nPress Enter to continue...")

def export_menu():
    """Display export options and handle selection."""
    if not current_results:
        clear_screen()
        print_error("No results to export.")
        input("\nPress Enter to continue...")
        return
    
    clear_screen()
    options = [
        "Export to CSV",
        "Export to JSON",
        "Export to Text File",
        "Back to Main Menu"
    ]
    
    choice = display_submenu("Export Results", options)
    
    if choice == 4:
        return
    
    file_format = options[choice-1].split(" ")[-1].lower()
    command_history.append(f"Export: {options[choice-1]}")
    
    # Get filename from user
    clear_screen()
    display_banner("Export Results")
    filename = input(f"Enter filename (without extension): ").strip()
    
    if not filename:
        filename = f"netutil_export_{int(time.time())}"
    
    with display_progress(f"Exporting to {file_format.upper()}..."):
        export_path = export_results(current_results, filename, file_format)
    
    if export_path:
        print_color(f"Results exported to: {export_path}", "green")
    else:
        print_error("Export failed.")
    
    input("\nPress Enter to continue...")

def main_menu():
    """Display main menu and handle top-level selections."""
    while True:
        clear_screen()
        
        options = [
            "System Network Information",
            "Website Analysis",
            "Network Diagnostics",
            "View Command History",
            "Export Results",
            "Exit"
        ]
        
        choice = display_main_menu(options)
        
        if choice == 1:
            system_info_menu()
        elif choice == 2:
            website_analysis_menu()
        elif choice == 3:
            network_diagnostics_menu()
        elif choice == 4:
            view_command_history()
        elif choice == 5:
            export_menu()
        elif choice == 6:
            clear_screen()
            display_banner("Goodbye!")
            print_color("Thank you for using Network Utility Script.", "cyan")
            time.sleep(1)
            sys.exit(0)

@click.command()
def main():
    """Run the network utility script."""
    try:
        # Start the interactive menu system
        clear_screen()
        display_banner("Network Utility Script")
        print_color("Loading...", "cyan")
        time.sleep(1)
        
        main_menu()
    except KeyboardInterrupt:
        clear_screen()
        display_banner("Goodbye!")
        print_color("Program terminated by user.", "yellow")
        sys.exit(0)
    except Exception as e:
        print_error(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
