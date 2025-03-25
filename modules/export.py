"""
Módulo de Exportação

Este módulo oferece funcionalidades completas para exportação de resultados
em diversos formatos incluindo CSV, JSON, e TXT.

Inclui recursos para formatação automática e estruturação dos dados,
permitindo que os resultados das análises sejam facilmente arquivados,
compartilhados ou processados posteriormente em outras aplicações.
"""

import os
import json
import csv
import pandas as pd
from datetime import datetime
import time
import platform
import sys
from colorama import Fore, Style, Back

def export_results(data, prefix):
    """
    Exporta resultados para um arquivo.
    
    Esta função converte e exporta os dados fornecidos para um formato
    selecionado pelo usuário. Suporta JSON, CSV e TXT, criando arquivos
    com nomes baseados no prefixo e timestamp atual.
    
    Args:
        data (dict): Os dados a serem exportados (dicionário).
        prefix (str): Prefixo para o nome do arquivo.
        
    Returns:
        str: O caminho para o arquivo exportado.
    """
    # Create exports directory if it doesn't exist
    os_name = platform.system()
    
    if os_name == "Windows":
        home_dir = os.path.expanduser("~")
        export_dir = os.path.join(home_dir, "NetworkUtility_exports")
    else:
        export_dir = os.path.expanduser("~/NetworkUtility_exports")
    
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)
    
    # Get current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Ask for export format
    print(Fore.YELLOW + "\nExport format options:" + Style.RESET_ALL)
    print("1. JSON")
    print("2. CSV")
    print("3. Text")
    
    try:
        choice = input(Fore.GREEN + "Select export format (1-3): " + Style.RESET_ALL)
    except EOFError:
        # Default to JSON in non-interactive mode
        print(Fore.YELLOW + "Running in non-interactive mode. Defaulting to JSON format." + Style.RESET_ALL)
        choice = "1"
    
    if choice == "1" or choice.lower() == "json":
        # Export as JSON
        filename = os.path.join(export_dir, f"{prefix}_{timestamp}.json")
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4, default=str)
            
    elif choice == "2" or choice.lower() == "csv":
        # Export as CSV - convert dict to DataFrame
        filename = os.path.join(export_dir, f"{prefix}_{timestamp}.csv")
        
        # Flatten nested dictionaries for CSV export
        flat_data = flatten_dict(data)
        
        df = pd.DataFrame([flat_data])
        df.to_csv(filename, index=False)
        
    else:
        # Export as plain text
        filename = os.path.join(export_dir, f"{prefix}_{timestamp}.txt")
        
        with open(filename, 'w') as f:
            f.write(f"Network Utility Export - {prefix}\n")
            f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Write the data in a readable format
            write_dict_to_text(f, data)
    
    return filename

def flatten_dict(d, parent_key='', sep='_'):
    """
    Flatten a nested dictionary.
    
    Args:
        d (dict): The dictionary to flatten.
        parent_key (str): The parent key for nested dictionaries.
        sep (str): Separator for nested keys.
        
    Returns:
        dict: Flattened dictionary.
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            for i, item in enumerate(v):
                if isinstance(item, dict):
                    items.extend(flatten_dict(item, f"{new_key}{sep}{i}", sep=sep).items())
                else:
                    items.append((f"{new_key}{sep}{i}", item))
        else:
            items.append((new_key, v))
            
    return dict(items)

def write_dict_to_text(file, d, indent=0):
    """
    Write a dictionary to a text file in a readable format.
    
    Args:
        file: The file object to write to.
        d (dict): The dictionary to write.
        indent (int): The indentation level.
    """
    for k, v in d.items():
        if isinstance(v, dict):
            file.write(f"{' ' * indent}{k}:\n")
            write_dict_to_text(file, v, indent + 2)
        elif isinstance(v, list):
            file.write(f"{' ' * indent}{k}:\n")
            for item in v:
                if isinstance(item, dict):
                    write_dict_to_text(file, item, indent + 2)
                else:
                    file.write(f"{' ' * (indent + 2)}- {item}\n")
        else:
            file.write(f"{' ' * indent}{k}: {v}\n")
