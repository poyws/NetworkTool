# Network Utility Tool

A comprehensive Python CLI network utility script with system information, website analysis, and network diagnostics capabilities.

## Features

- **System Network Information**: View detailed information about your network system including local/public IP addresses, MAC address, network interfaces, network speed, and DNS servers.
- **Website Analysis**: Analyze websites with domain IP lookup, DNS records, ping test, port scanning, WHOIS information, and SSL certificate details.
- **Network Diagnostics**: Perform network diagnostics with speed test, latency check, packet loss analysis, and route tracing.
- **Command History**: Track and view command history.
- **Export Options**: Export results in JSON, CSV, or text format.

## Installation

1. Clone this repository:
```bash
git clone https://github.com/poyws/NetworkTool
cd network-utility
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Interactive Mode

Run the script without arguments to use the interactive menu:

```bash
python network_utility.py
```

### Command Line Interface

Use specific commands for direct access to features:

#### System Information
```bash
python network_utility.py system
```

#### Website Analysis
```bash
python network_utility.py website --domain example.com
```

#### Network Diagnostics
```bash
python network_utility.py diagnostics
```

#### Command History
```bash
python network_utility.py history
```

### Help
```bash
python network_utility.py --help
```

## Dependencies

- click: CLI framework
- colorama: Terminal text colors
- dnspython: DNS toolkit
- pandas: Data manipulation and analysis
- psutil: System information retrieval
- pyfiglet: ASCII art text banner generation
- pyopenssl: SSL certificate analysis
- python-whois: WHOIS information retrieval
- requests: HTTP requests
- tqdm: Progress bars

## Modules

- **system_info.py**: System network information functionality.
- **website_analysis.py**: Website analysis capabilities.
- **network_diagnostics.py**: Network diagnostic tools.
- **ui_components.py**: UI components including menus and banners.
- **export.py**: Result export functionality.

## Export Functionality

Results can be exported in three formats:
- **JSON**: Structured data in JSON format.
- **CSV**: Tabular data in CSV format.
- **Text**: Human-readable text file.

Exports are saved in a directory called "NetworkUtility_exports" in your home directory.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
