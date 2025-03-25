"""
Módulo de Componentes de Interface

Este módulo oferece componentes avançados de interface para o utilitário de rede,
incluindo banners personalizados com arte ASCII, menus interativos,
animações de carregamento e barras de progresso para operações longas.

O módulo é projetado para fornecer uma experiência de usuário rica em
terminais de linha de comando, com suporte a cores e elementos visuais.
"""

import os
import sys
import time
import pyfiglet
from colorama import Fore, Style, Back
import random
import platform
from tqdm import tqdm

def display_banner(text):
    """
    Exibe um banner estilizado com o texto fornecido usando arte ASCII.
    
    O banner é exibido com cores e formatação para melhorar a experiência visual.
    A tela é limpa antes da exibição para garantir uma apresentação limpa.
    
    Args:
        text (str): O texto a ser mostrado no banner.
    """
    # Limpa a tela com comando apropriado de acordo com o sistema operacional
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Fontes para estilo mais sóbrio
    font_options = ["standard", "slant", "smslant"]
    selected_font = random.choice(font_options)
    
    # Usar cores minimalistas para o banner
    banner_color = Fore.WHITE + Style.BRIGHT
    
    # Use pyfiglet to create ASCII art
    banner = pyfiglet.figlet_format(text, font=selected_font)
    
    # Criar decoração estilizada minimalista
    border_length = 70
    border_color = Fore.WHITE + Style.DIM
    
    # Exibir o banner com tema minimalista
    print("\n" + border_color + "="*border_length + Style.RESET_ALL)
    print(banner_color + banner + Style.RESET_ALL)
    print(border_color + "="*border_length + Style.RESET_ALL)
    
    # Adicionar descrição do utilitário com estilo minimalista
    if "Network Utility" in text or "Network Diagnostics" in text:
        tagline = Fore.WHITE + Style.DIM + "A Powerful Network Diagnostic Tool" + Style.RESET_ALL
        center_padding = (border_length - len("A Powerful Network Diagnostic Tool")) // 2
        print(" " * center_padding + tagline)
        print()

def display_menu(prompt, options):
    """
    Display a menu and get user's choice.
    
    Args:
        prompt (str): The prompt to display.
        options (list): List of option strings.
        
    Returns:
        str: The user's choice.
    """
    # Tema preto/escuro para o menu
    menu_width = 60
    box_color = Fore.WHITE + Style.DIM
    title_color = Fore.WHITE + Style.BRIGHT
    
    # Título do menu com caixa
    print("\n" + box_color + "┌" + "─" * menu_width + "┐" + Style.RESET_ALL)
    title_line = f"{title_color}{prompt}{Style.RESET_ALL}"
    padding = (menu_width - len(prompt)) // 2
    print(box_color + "│" + " " * padding + title_line + " " * (menu_width - padding - len(prompt)) + "│" + Style.RESET_ALL)
    print(box_color + "├" + "─" * menu_width + "┤" + Style.RESET_ALL)
    
    # Opções do menu
    for option in options:
        option_text = option
        
        # Se a opção começa com um número (ex: "1. Option"), extraímos o número
        if option_text[0].isdigit() and '. ' in option_text:
            num, text = option_text.split('. ', 1)
            
            # Para um tema preto/escuro, simples, sem emojis
            if num == "0":
                # Opção Exit com cor vermelha
                colored_option = num + ". " + Fore.RED + text + Style.RESET_ALL
            else:
                # Outras opções em branco
                colored_option = num + ". " + Fore.WHITE + text + Style.RESET_ALL
                
            print(box_color + "│ " + Style.RESET_ALL + colored_option + 
                  " " * (menu_width - len(text) - len(num) - 2) + box_color + "│" + Style.RESET_ALL)
        else:
            # Opção sem número
            print(box_color + "│ " + Style.RESET_ALL + option_text + 
                  " " * (menu_width - len(option_text) - 1) + box_color + "│" + Style.RESET_ALL)
    
    # Rodapé da caixa
    print(box_color + "└" + "─" * menu_width + "┘" + Style.RESET_ALL)
    
    # Input minimalista
    try:
        input_prompt = Fore.WHITE + Style.DIM + "> " + Style.RESET_ALL
        choice = input(input_prompt)
        return choice
    except EOFError:
        # Em caso de erro EOF (como quando rodando em modo não-interativo)
        print(Fore.WHITE + Style.DIM + "Executando em modo não-interativo. Usando a primeira opção por padrão." + Style.RESET_ALL)
        return "1"

def display_loading(duration=2):
    """
    Display a loading animation.
    
    Args:
        duration (int): Duration of the animation in seconds.
    """
    # Animações mais minimalistas, adequadas para tema escuro
    animations = [
        "█▁▁▁▁",
        "▁█▁▁▁",
        "▁▁█▁▁",
        "▁▁▁█▁",
        "▁▁▁▁█",
        "▁▁▁█▁",
        "▁▁█▁▁",
        "▁█▁▁▁"
    ]
    
    # Frases para exibir durante o carregamento (mantidas)
    loading_messages = [
        "Preparando análise...",
        "Inicializando componentes...",
        "Carregando módulos...",
        "Processando dados...",
        "Verificando conexões...",
        "Configurando parâmetros...",
        "Analisando rede...",
        "Calculando métricas...",
        "Consultando interfaces...",
        "Coletando informações..."
    ]
    
    # Seleciona mensagem de carregamento
    loading_message = random.choice(loading_messages)
    
    # Define barra de progresso minimalista em preto e branco
    bar_format = "{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt}"
    
    # Exibe a barra de progresso com tema minimalista
    for _ in tqdm(range(0, 100), 
                 desc=f"{Fore.WHITE + Style.DIM}{loading_message}{Style.RESET_ALL}", 
                 bar_format=bar_format, 
                 ncols=80, 
                 leave=False,
                 colour='white'):
        time.sleep(duration / 100)
    
    # Exibe mensagem de conclusão simples
    print(f"\n{Fore.WHITE + Style.DIM}Concluído.{Style.RESET_ALL}")

def display_error(message):
    """
    Display an error message.
    
    Args:
        message (str): The error message to display.
    """
    # Cria uma caixa simples para a mensagem de erro
    box_width = len(message) + 10
    
    print("\n")
    print(Fore.RED + "┌" + "─" * box_width + "┐")
    print("│" + " " * box_width + "│")
    print("│" + " " * 4 + "ERRO" + " " * (box_width - 8) + "│")
    print("│" + " " * box_width + "│")
    print("│" + " " * 2 + message + " " * (box_width - len(message) - 2) + "│")
    print("│" + " " * box_width + "│")
    print("└" + "─" * box_width + "┘" + Style.RESET_ALL)
    print()
    time.sleep(1)

def display_success(message):
    """
    Display a success message.
    
    Args:
        message (str): The success message to display.
    """
    # Cria uma caixa simples para a mensagem de sucesso
    box_width = len(message) + 10
    
    print("\n")
    print(Fore.WHITE + Style.DIM + "┌" + "─" * box_width + "┐")
    print("│" + " " * box_width + "│")
    print("│" + " " * 4 + "SUCESSO" + " " * (box_width - 11) + "│")
    print("│" + " " * box_width + "│")
    print("│" + " " * 2 + message + " " * (box_width - len(message) - 2) + "│")
    print("│" + " " * box_width + "│")
    print("└" + "─" * box_width + "┘" + Style.RESET_ALL)
    print()
    time.sleep(1)

def confirm_action(prompt):
    """
    Ask for confirmation of an action.
    
    Args:
        prompt (str): The prompt to display.
        
    Returns:
        bool: True if confirmed, False otherwise.
    """
    try:
        # Interface minimalista para confirmação
        print("\n" + Fore.WHITE + Style.DIM + prompt + Style.RESET_ALL)
        print(Fore.WHITE + Style.DIM + "─" * len(prompt) + Style.RESET_ALL)
        
        # Opções simples sem emojis
        print(f"{Fore.WHITE}[y] Sim{Style.RESET_ALL}   {Fore.WHITE}[n] Não{Style.RESET_ALL}")
        
        choice = input(Fore.WHITE + Style.DIM + "> " + Style.RESET_ALL).lower()
        return choice.startswith('y')
    except EOFError:
        # Em caso de erro EOF (como quando rodando em modo não-interativo)
        print(Fore.WHITE + Style.DIM + "Executando em modo não-interativo. Usando 'sim' por padrão." + Style.RESET_ALL)
        return True

def display_result_table(title, data, include_units=False):
    """
    Displays a result table with a minimalist, dark format.
    
    Args:
        title (str): The title of the result table.
        data (dict): Dictionary with results to display.
        include_units (bool): Whether to include units when displaying values.
    """
    # Definir unidades para medições comuns
    units = {
        'download': 'Mbps',
        'upload': 'Mbps',
        'ping': 'ms',
        'min': 'ms',
        'avg': 'ms',
        'max': 'ms',
        'loss': '%',
        'time': 'ms',
        'packets_sent': '',
        'packets_received': '',
        'packet_loss': '%',
        'jitter': 'ms'
    }
    
    # Calcular largura da tabela
    max_key_len = max([len(str(k)) for k in data.keys()]) if data else 10
    max_val_len = max([len(str(v)) + 5 for v in data.values()]) if data else 10
    table_width = max_key_len + max_val_len + 8
    
    # Estilo minimalista em preto/branco
    border_color = Fore.WHITE + Style.DIM
    header_color = Fore.WHITE + Style.BRIGHT
    
    # Título com estilo minimalista
    print("\n")
    print(border_color + "┌" + "─" * table_width + "┐" + Style.RESET_ALL)
    
    # Centralizar título
    title_padding = (table_width - len(title)) // 2
    print(border_color + "│" + " " * title_padding + 
          header_color + title + 
          Style.RESET_ALL + border_color + " " * (table_width - title_padding - len(title)) + "│" + Style.RESET_ALL)
    
    print(border_color + "├" + "─" * table_width + "┤" + Style.RESET_ALL)
    
    # Exibir dados da tabela com estilo minimalista
    for key, value in data.items():
        # Formatar valor
        if isinstance(value, float):
            formatted_value = f"{value:.2f}"
        else:
            formatted_value = str(value)
            
        # Adicionar unidade se necessário
        if include_units and key.lower() in units:
            unit = units[key.lower()]
            if unit:  # Só adiciona se houver unidade
                formatted_value = f"{formatted_value} {unit}"
        
        # Formatar chave para exibição (substituir underscore por espaço e capitalize)
        display_key = key.replace('_', ' ').capitalize()
        
        # Imprimir linha da tabela com estilo minimalista
        print(border_color + "│ " + Style.RESET_ALL + 
              Fore.WHITE + display_key + 
              " " * (max_key_len - len(display_key) + 2) + 
              Fore.WHITE + Style.BRIGHT + formatted_value + 
              " " * (max_val_len - len(formatted_value)) + 
              border_color + " │" + Style.RESET_ALL)
    
    # Rodapé da tabela
    print(border_color + "└" + "─" * table_width + "┘" + Style.RESET_ALL)
    print()

def display_multi_result(title, data_list):
    """
    Display a result with multiple sections/tables in minimalist dark style.
    
    Args:
        title (str): The main title of the results.
        data_list (list): List of dictionaries, each with a 'title' and 'data' key.
    """
    # Criar borda decorativa
    border_width = 70
    border_color = Fore.WHITE + Style.DIM
    title_color = Fore.WHITE + Style.BRIGHT
    
    # Título principal
    print("\n")
    print(border_color + "┌" + "─" * border_width + "┐" + Style.RESET_ALL)
    
    # Centralizar título principal
    title_padding = (border_width - len(title)) // 2
    print(border_color + "│" + " " * title_padding + 
          title_color + title + 
          Style.RESET_ALL + border_color + " " * (border_width - title_padding - len(title)) + "│" + Style.RESET_ALL)
    
    print(border_color + "├" + "─" * border_width + "┤" + Style.RESET_ALL)
    
    # Para cada conjunto de dados, criar uma seção
    for i, section in enumerate(data_list):
        section_title = section.get('title', f"Seção {i+1}")
        section_data = section.get('data', {})
        
        # Exibir título da seção
        section_color = Fore.WHITE
        print(border_color + "│ " + Style.RESET_ALL + 
              section_color + Style.BRIGHT + section_title + 
              Style.RESET_ALL + border_color + " " * (border_width - len(section_title) - 2) + "│" + Style.RESET_ALL)
        
        # Linha divisória entre o título da seção e os dados
        print(border_color + "│ " + "─" * (border_width - 4) + 
              border_color + " │" + Style.RESET_ALL)
        
        # Exibir dados da seção
        for key, value in section_data.items():
            # Formatar valor
            if isinstance(value, float):
                formatted_value = f"{value:.2f}"
            else:
                formatted_value = str(value)
                
            # Formatar chave para exibição
            display_key = key.replace('_', ' ').capitalize()
            
            # Imprimir linha de dados
            print(border_color + "│ " + Style.RESET_ALL + 
                  Fore.WHITE + Style.DIM + "  " + display_key + ": " + 
                  Style.RESET_ALL + Fore.WHITE + formatted_value + 
                  " " * (border_width - len(display_key) - len(formatted_value) - 4) + 
                  border_color + "│" + Style.RESET_ALL)
        
        # Se não for a última seção, adicionar divisor entre seções
        if i < len(data_list) - 1:
            print(border_color + "│" + " " * border_width + "│" + Style.RESET_ALL)
    
    # Rodapé
    print(border_color + "└" + "─" * border_width + "┘" + Style.RESET_ALL)
    print()
