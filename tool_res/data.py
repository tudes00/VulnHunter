import os
import json

RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"

Version = "1.0.0"

tools = [
    {"name": "port_scan", "description": "port_scan_desc", "file_target":"./modules/portScan.py"},
    {"name": "upcoming_features", "description": "upcoming_features_desc", "file_target":"./modules/soon.py"},
    {"name": "settings", "description": "settings", "file_target":"./modules/settings.py"},
    {"name": "exit", "description": "exit_desc"}
]

soonTools = [
    {"name": "Subdomain Enumeration", "description": "Perform subdomain enumeration."},
    {"name": "Password Cracking", "description": "Perform password cracking attempts."},
    {"name": "Test All Tools (Generate a full report)", "description": "Run all the available tests on a target website and generate a report."},
]

translations = {
    "en": {
        "ava_tools": "Available tools:",
        "choice_tools": "Enter the number of the tool you want to use: ",
        "port_scan": "Port Scanning",
        "port_scan_desc": "Perform port scanning to find open ports.",
        "upcoming_features": "Upcoming Features",
        "upcoming_features_desc": "Planned updates and improvements.",
        "settings": "Settings",
        "exit": "Exit",
        "exit_desc": "Exit the program",
        "enter_select":"Enter the selection: ",
        "select_changed": "Selection changed to ",
        "select_inv": "Invalid selection!",
        "enter_choice": "Enter your choice: ",
        "choice_inv": "Invalid choice! Please select a valid option.",
        "language": "Language: ",
        "check_updt_time": "check for update every time: ",
        "check_updt": "check for update: ",
        "select_to_check": "select to check (Useful if the above option is disabled)",
        "yes": "Yes",
        "no": "No",
        "language_desc": "Select your preferred language (French is not fully supported)",
        "check_updt_time_desc" : "Automatically check for updates when launching this tool",
        "check_updt_desc": "Check for updates (tool version and dependencies)",
        "inv_number": "Invalid number! Please select a number from the list."

    },
    "fr": {
        "ava_tool": "Outils disponibles:",
        "choice_tools": "Entrez le numéro de l'outil que vous souhaitez utiliser: ",
        "port_scan": "Analyse de ports",
        "port_scan_desc": "Effectuer une analyse de ports pour trouver des ports ouverts.",
        "upcoming_features": "Fonctionnalités à venir",
        "upcoming_features_desc": "Mises à jour et améliorations prévues.",
        "settings": "Paramètres",
        "exit": "Exit",
        "exit_desc": "Quitter le programme",
        "enter_select":"Entrez la sélection: ",
        "select_changed": "Sélection modifiée en ",
        "select_inv": "Selection invalide!",
        "enter_choice": "Entrez votre choix: ",
        "choice_inv": "Choix invalide ! Veuillez sélectionner une option valide.",
        "language": "Langue: ",
        "check_updt_time": "vérifier les mises à jour à chaque fois: ",
        "check_updt": "vérifier les mises à jour: ",
        "select_to_check": "sélectionnez pour vérifier (utile si l'option ci-dessus est désactivée)",
        "yes": "oui",
        "no": "non",
        "language_desc": "Sélectionnez votre langue préférée (le français n'est pas entièrement pris en charge)",
        "check_updt_time_desc": "Vérifier automatiquement les mises à jour lors du lancement de cet outil",
        "check_updt_desc": "Vérifier les mises à jour (version de l'outil et dépendances)",
        "inv_number": "Numéro non valide ! Veuillez sélectionner un numéro dans la liste."
    }
}

CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'settings.json')

def load_settings():
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None
    
def save_settings(settings):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(settings, f, indent=4)

def check_update_setting():
    settings = load_settings()
    for setting in settings:
        if setting["name"] == "check_updt_time" and setting["current"] == "no":
            return True
    return False

def get_current_language():
    settings = load_settings()
    for setting in settings:
        if setting["name"] == "language":
            return setting["current"]
        
def translate(key):
    language = get_current_language()
    return translations.get(language, {}).get(key, key)