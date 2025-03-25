#!/usr/bin/env python3
"""
Script de teste para verificar a exibição de resultados
"""

from modules.ui_components import display_result_table, display_multi_result, display_banner

# Simular alguns dados de teste
speed_test_data = {
    "download": 42.5,
    "upload": 15.2,
    "ping": 12.8
}

latency_data = {
    "min": 8.5,
    "avg": 12.3,
    "max": 15.7
}

packet_loss_data = {
    "sent": 50,
    "received": 48,
    "lost": 2,
    "loss_percentage": 4.0
}

website_data = {
    "domain": "example.com",
    "ip_address": "93.184.216.34",
    "status": "Ativo",
    "response_time": 115.2
}

# Testar display_banner
display_banner("Network Utility Test")

print("\nTestando display_result_table:")
display_result_table("WEBSITE INFO", website_data, include_units=True)

print("\nTestando display_multi_result:")
diagnostic_results = [
    {
        'title': 'NETWORK SPEED TEST RESULTS',
        'data': speed_test_data
    },
    {
        'title': 'LATENCY CHECK RESULTS',
        'data': latency_data
    },
    {
        'title': 'PACKET LOSS ANALYSIS RESULTS',
        'data': packet_loss_data
    }
]

display_multi_result("DIAGNOSTIC SUMMARY", diagnostic_results)