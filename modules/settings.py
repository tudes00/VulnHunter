import sys
import os
import time
import json

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from tool_res.data import RESET, GREEN, RED, YELLOW, BLUE, CYAN, MAGENTA, load_settings, save_settings, translate
from main import clear_screen, run_setup


def display_and_change_setting(choice, settings):
    setting = settings[int(choice) - 1]
    clear_screen()
    print(f"{YELLOW}Options:{RESET}")
    
    for option in setting['options']:
        print(f"   {option}")
    
    new_choice = input(CYAN + translate('enter_select') + RESET).strip()

    if new_choice in setting['options']:
        setting["current"] = new_choice
        save_settings(settings)
        print(GREEN+ translate('select_changed') + new_choice + RESET)
        time.sleep(1)
        clear_screen()
    else:
        print(RED + translate('select_inv') + RESET)
        time.sleep(1)
        clear_screen()

def main():
    try:
        settings = load_settings()
        while True:
            print(f"{YELLOW+translate('settings')}:")
            for i, setting in enumerate(settings, start=1):
                print(f"{GREEN}  -> {i}. {translate(setting['name'])}{RESET}{translate(setting['current'])} -> {translate(setting['description'])}")

            choice = input(BLUE+ translate('enter_choice') + RESET)

            if choice == '1' or choice == '2':
                display_and_change_setting(choice, settings)
            elif choice == '3':
                clear_screen()
                run_setup()
                clear_screen()
            elif choice == '4':
                clear_screen("tools")
                break
            else:
                print(RED + translate('choice_inv') + RESET)
                clear_screen()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
