import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from tool_res.data import RESET, GREEN, RED, YELLOW, BLUE, CYAN, MAGENTA, soonTools
from main import clear_screen

def main():
    try:
        clear_screen()
        print(f"{YELLOW}Upcoming Features:")
        for tool in soonTools:
            print(f"{RED}  ->{tool['name']}:{RESET} {tool['description']}")
        input(f"\n{CYAN}Press Enter to exit...")
        clear_screen("tools")
        
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
