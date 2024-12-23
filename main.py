import subprocess
import sys
import time
import json
import platform

from tool_res.data import RESET, GREEN, RED, YELLOW, BLUE, CYAN, MAGENTA, tools, Version, check_update_setting, translate

def clear_screen(type=""):
    if sys.platform == "win32":
        subprocess.call("cls", shell=True)
    else:
        subprocess.call("clear", shell=True)
    display_logo()
    if type == "tools":
        display_tools()

def run_setup():
    print(f"{BLUE}Running setup.py to install dependencies...{RESET}")
    
    try:
        subprocess.check_call([sys.executable, "setup.py"])
        print(f"{GREEN}Dependencies installation completed successfully.{RESET}")
    except Exception as e:
        print(f"{RED}Error during dependencies installation: {e}{RESET}")
        sys.exit(1)

def display_logo():
    version = Version
    
    print(MAGENTA+r"""
 _____     _     _____         _           
|  |  |_ _| |___|  |  |_ _ ___| |_ ___ ___ 
|  |  | | | |   |     | | |   |  _| -_|  _|
 \___/|___|_|_|_|__|__|___|_|_|_| |___|_|  """)
                                          
    print(f"      {RED}made by Tudes{RESET} - Version {version}")
    print(f"{YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")

def display_tools():
    print(YELLOW + translate('ava_tool') + RESET)
    for i, tool in enumerate(tools, start=1):
        print(f"{GREEN}  -> {i}. {translate(tool['name'])}{RESET} -> {translate(tool['description'])}")
       
    while True:
        try:
            print(f"\r{CYAN + translate('choice_tools') + GREEN}", end='', flush=True)
            choice = int(input())

            if choice < 1 or choice > len(tools):
                print(f"\r{' ' * 100}", end='', flush=True)
                print(f"\r{RED + translate('inv_number') + RESET}", flush=True)
                time.sleep(1)
                clear_screen("tools")
            else:
                selected_tool = tools[choice - 1]

                if selected_tool["name"] == "exit":
                    print(f"{RESET}\n", end='', flush=True)
                    clear_screen()
                    sys.exit()
                    break

                try:
                    clear_screen()
                    if selected_tool['file_target'].endswith('.py'):
                        subprocess.run([sys.executable, selected_tool['file_target']], check=True)
                    else:
                        subprocess.run([selected_tool['file_target']], check=True)
                    break
                except subprocess.CalledProcessError as e:
                    print(f"{RED}Error executing the tool: {e}{RESET}")
                    time.sleep(1.5)
                    clear_screen("tools")
        except ValueError:
            print(f"\r{' ' * 100}", end='', flush=True)
            print(f"\r{RED + translate('inv_number') + RESET}", flush=True)
            time.sleep(1)
            clear_screen("tools")

def main():
    try:
        clear_screen()

        os_name = platform.system()
        if not os_name == "Linux" and os_name == "Windows":
                print(f"{RED}Your OS is not supported. Contact me to help me improve this project! {RESET}")
                input(f"{BLUE}Enter to exit")
                sys.exit()
        
        if not check_update_setting():
            run_setup() 
        clear_screen("tools")
    except KeyboardInterrupt:
        print(f"{GREEN}\nProcess interrupted by user. Exiting...{RESET}")


if __name__ == "__main__":
    main()
