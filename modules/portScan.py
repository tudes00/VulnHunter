import subprocess
import sys
import shutil
import os
import re
from lxml import etree
import time
import platform

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from tool_res.data import RESET, GREEN, RED, YELLOW, BLUE, CYAN, MAGENTA, translate
from main import clear_screen



def display_installation_guide():
    print(f"\n{YELLOW}Instructions for configuring Nmap on Windows:{RESET}")
    
    print(f"{CYAN}On Windows:{RESET}")
    print(
        """
1. Locate the Nmap installation folder (e.g., "C:\\Program Files (x86)\\Nmap").
2. Open 'System Properties':
- Right-click 'This PC' or 'My Computer' and select 'Properties'.
- Click on 'Advanced system settings'.
- Go to the 'Environment Variables' section.
3. Find the 'Path' variable under 'System variables' and click 'Edit'.
4. Click 'New' and add the full path to the Nmap installation directory (e.g., "C:\\Program Files (x86)\\Nmap").
5. Save changes by clicking 'OK' in all open dialogs.
6. Restart your terminal or IDE to apply the changes.
""")


def execute_nmap_command(command, output_file=None):
    try:
        print(f"{CYAN}Executing Nmap command: {command}{RESET}")
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.stdout:
            print(f"{GREEN}Output:{RESET}\n{result.stdout}")
            if output_file:
                print(f"{BLUE}Results saved to {output_file}{RESET}")
        
        if result.stderr:
            print(f"{RED}Error:{RESET}\n{result.stderr}")
    except Exception as e:
        print(f"{RED}Failed to execute command: {e}{RESET}")


def display_help_page():
    print(f"{CYAN}Fetching Nmap help page...{RESET}")
    execute_nmap_command("nmap --help")

def convert_xml_to_html(xml_file, output_file):
    xml_tree = etree.parse(xml_file)
    xsl_tree = etree.parse("./tool_res/xsl/nmap.xsl")

    transformer = etree.XSLT(xsl_tree)

    html_tree = transformer(xml_tree)

    with open(output_file, 'wb') as f:
        f.write(etree.tostring(html_tree, pretty_print=True))

    try:
        os.remove(xml_file)
    except OSError as e:
        print(f"{RED}Erreur lors de la suppression du fichier XML : {e}{RESET}")

def ask_for_command():
    clear_screen()
    
    while True:
        print(f"\n{YELLOW}Let's configure your Nmap command!{RESET}")
        targets = input(f"{CYAN}Enter the target IPs, domains, or URLs (comma-separated, e.g., '192.168.1.1, 192.168.1.2'), type 'HELP' for help or 'EXIT' to return to menu: {RESET}").strip()

        if targets.lower() == 'help':
            clear_screen()
            print(f"{BLUE}Help: Enter valid IP addresses, domain names, or URLs for your targets, separated by commas.\n{RESET}")
            continue
        elif targets.lower() == 'exit':
            return None, None, None
        
        targets = [target.strip() for target in targets.split(',')]
        
        valid_targets = [target for target in targets if is_valid_target(target)]
        if not valid_targets:
            print(f"{RED}Invalid targets! Please enter valid IP addresses, domains, or URLs.{RESET}")
            continue
        
        break

    while True:
        scan_type = input(f"{CYAN}Enter the scan type (or press Enter to skip), type 'HELP' for help or 'EXIT' to return to menu: {RESET}").strip()
        
        if scan_type.lower() == 'help':
            print(f"{BLUE}Help: You can specify the scan type such as:\n- {GREEN}'-sS'{BLUE} for SYN scan\n- {GREEN}'-A'{BLUE} for aggressive scan\n- {GREEN}'-Pn'{BLUE} for no ping\nFor a full list of scan types, refer to the Nmap documentation.\n{RESET}")            
            continue
        elif scan_type.lower() == 'exit':
             return None, None, None

        if not scan_type:
            break
        
        if not is_valid_scan_type(scan_type):
            print(f"{RED}Invalid scan type! Choose a valid option (e.g., -sS, -A, -Pn, etc.) or leave it blank.{RESET}")
            continue
        break

    while True:
        additional_flags = input(f"{CYAN}Enter any additional flags (or press Enter to skip) or 'EXIT' to return to menu: {RESET}").strip()
        
        if additional_flags.lower() == 'help':
            print(f"{BLUE}Help: You can specify additional flags for the scan.\nFor example:\n- {GREEN}'-p 80'{BLUE} to specify ports\n- {GREEN}'-T4'{BLUE} to set timing options\n{RESET}")            
            continue
        elif additional_flags.lower() == 'exit':
             return None, None, None

        break

    save_result = input(f"{YELLOW}Do you want to save the result to a file? (yes/no): {RESET}").strip().lower()
    
    output_file = None
    convert = False
    if save_result in ['yes', 'y']:
        output_file = input(f"{CYAN}Enter the filename to save the result (e.g., 'scan_results' without .txt!): {RESET}").strip()
        if output_file == "":
            output_file = targets[0]

        file_format = input(f"{CYAN}Enter the file format (txt, xml, html): {RESET}").strip().lower()
        if file_format not in ['txt', 'xml', 'html']:
            print(f"{RED}Invalid format! Defaulting to '.txt'.{RESET}")
            file_format = 'txt'

        if not output_file.endswith(f".{file_format}"):
            if file_format == "html":
                output_file += f".xml"
                convert = True
            else:
                output_file += f".{file_format}"
        
        output_directory = 'scan_results'
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        
        output_file_path = os.path.join(output_directory, output_file).replace("\\", "/")
        if file_format == 'txt':
            additional_flags += f" -oN {output_file_path}"
        elif file_format in ['xml', 'html']:
            additional_flags += f" -oX {output_file_path}"
        print(f"{GREEN}Result will be saved to: {output_file_path}{RESET}")

    
    command = "nmap " + " ".join([f"{scan_type} {additional_flags} {target}" for target in valid_targets]).strip()
    return command, output_file_path if output_file else None, convert



def is_valid_target(target):
    target = target.strip()
    ip_pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    domain_pattern = re.compile(r"^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$")
    url_pattern = re.compile(r"^(https?://)([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(/.*)?$")
    return ip_pattern.match(target) or domain_pattern.match(target) or url_pattern.match(target)


def is_valid_scan_type(scan_type):
    scan_type = scan_type.strip()
    valid_scan_types = [
        '-sS', '-sT', '-sP', '-sU', '-sV', '-A', '-O', 
        '--top-ports', '--open', '-sC', '-sW', '-sX', '-Pn',
        '-T0', '-T1', '-T2', '-T3', '-T4', '-T5'
    ]
    return scan_type in valid_scan_types

def execute_full_command(command):
    try:
        print(f"{CYAN}Executing full Nmap command: {command}{RESET}")
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.stdout:
            print(f"{GREEN}Output:{RESET}\n{result.stdout}")
        
        if result.stderr:
            print(f"{RED}Error:{RESET}\n{result.stderr}")
    except Exception as e:
        print(f"{RED}Failed to execute command: {e}{RESET}")

def check_nmap():
    os_name = platform.system()
    try:
        subprocess.run(["nmap", "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        print(f"{RED}nmap is not installed.{RESET}")
        if os_name == "Linux":
                subprocess.run(["sudo", "apt-get", "update"], check=True)
                subprocess.run(["sudo", "apt-get", "install", "-y", "nmap"], check=True)
                print("Nmap was installed successfully.")
        elif os_name == "Windows":
                print(f"{CYAN}You can download nmap from the following link:{RESET}")
                print("https://nmap.org/download.html")
                display_installation_guide()
                input(f"{BLUE}Restart your terminal or IDE{RESET}")
                sys.exit()
        else:
                print(f"{RED}Your OS is not supported. Please refer to the official Nmap documentation: https://nmap.org/download.html{RESET}and contact me to help me improve this project")
                input(f"{BLUE}Enter to exit")
                sys.exit()


def main():
    try:
        check_nmap()
        clear_screen()
        while True:
            print(f"{YELLOW}Options:{RESET}")
            print("   1. Run a guided Nmap command")
            print("   2. Run a full Nmap command")
            print("   3. Display Nmap help page")
            print("   4. Exit")
            choice = input(f"{BLUE}Enter your choice (1-4): {RESET}")

            if choice == '1':
                command, output_file, convert = ask_for_command()
                if command:
                    execute_nmap_command(command, output_file)
                    if convert:
                        html_output_file = os.path.splitext(output_file)[0] + ".html"
                        convert_xml_to_html(output_file, html_output_file)
                        print(f"Converted {output_file} to {html_output_file}")
                    
            elif choice == '3':
                display_help_page()
            elif choice == '2':
                full_command = input(f"{CYAN}Enter the full Nmap command (se.g., 'nmap -sS 192.168.1.1') or 'EXIT' to return to menu: {RESET}").strip()
                if not full_command == "exit":
                    execute_full_command(full_command)
            elif choice == '4':
                print(f"{GREEN}Exiting the program. Goodbye!{RESET}")
                clear_screen("tools")
                break
            else:
                print(f"{RED}Invalid choice! Please select a valid option.{RESET}")
                clear_screen()

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()