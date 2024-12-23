import subprocess
import sys
import os

from tool_res.data import RESET, GREEN, RED, YELLOW, BLUE, CYAN

def install_package(package_name):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--break-system-packages", package_name])

def is_package_installed(package_name):
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "show", package_name],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return bool(result.stdout)
    except subprocess.CalledProcessError:
        return False

def install_dependencies():
    packages = ["requests", "beautifulsoup4", "tqdm", "python-nmap", "lxml"]
    for package in packages:
        print(f"{CYAN}Checking and installing {package}...{RESET}")
        if not is_package_installed(package):
            try:
                print(f"{CYAN}Installing {package}...{RESET}")
                install_package(package)
                print(f"{GREEN}{package} installed successfully.{RESET}")
            except Exception as e:
                print(f"{RED}Failed to install {package}: {e}{RESET}")
                sys.exit(1)
        else:
            print(f"{GREEN}{package} is already installed.{RESET}")

def main():
    try:
        print(f"{BLUE}Starting dependency installation...{RESET}")
        install_dependencies()
        print(f"{GREEN}All dependencies installed successfully.{RESET}")
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
