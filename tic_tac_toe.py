import random
from language_manager import LanguageManager

#
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
ORANGE = "\033[38;5;214m"
PURPLE = "\033[38;5;129m"
RESET = "\033[0m"

# Board erstellen und ausgeben
def print_board():
    board = f" {fields[1]} | " + fields[2] + " | " + fields[3] + " \n---|---|---\n " + fields[4] + " | " + fields[5] + " | " + fields[6] + " \n---|---|---\n " + fields[7] + " | " + fields[8] + " | " + fields[9] + " "
    new_board = board.replace("x", f"{PURPLE}x{RESET}")
    new_board = new_board.replace("o", f"{ORANGE}o{RESET}")
    print(new_board)

# Nächsten Schritt
def next_step(player_int):
    while not check_winner():
        player_str = str(player_int)
        question = f"Spieler " + player_str + ": Wie willst du fortfahren? Bitte Feldziffer eingeben!: "
        new_question = question.replace("Spieler 1", f"{PURPLE}Spieler 1{RESET}")
        new_question = new_question.replace("Spieler 2", f"{ORANGE}Spieler 2{RESET}")

        try:
            game_input = int(input(new_question))
        except ValueError:
            print(f"{RED}Ungültige Eingabe! Bitte gib eine Zahl zwischen 1 und 9 ein.{RESET}")
            continue

        if game_input > 0 and game_input <= 9:
            if fields[game_input] != "x" and fields[game_input] != "o":
                if player_int == 1:
                    fields[game_input] = "x"
                    print_board()
                    player_int = 2
                elif player_int == 2:
                    fields[game_input] = "o"
                    print_board()
                    player_int = 1
            else:
                print(f"{RED}Dieses Feld ist bereits belegt!{RESET}")
        else:
            print(f"{RED}Ungültige Zahl! Bitte verwende nur Zahlen zwischen 1 und 9{RESET}")

# Gewinner überprüfen
def check_winner():

    for player_number in ["1", "2"]:
        player_key = "x" if player_number == "1" else "o"
        other_player = "1" if player_number == "2" else "2"
        if (fields[1] == player_key and fields[2] == player_key and fields[3] == player_key) or \
           (fields[4] == player_key and fields[5] == player_key and fields[6] == player_key) or \
           (fields[7] == player_key and fields[8] == player_key and fields[9] == player_key) or \
           (fields[1] == player_key and fields[4] == player_key and fields[7] == player_key) or \
           (fields[2] == player_key and fields[5] == player_key and fields[8] == player_key) or \
           (fields[3] == player_key and fields[6] == player_key and fields[9] == player_key) or \
           (fields[1] == player_key and fields[5] == player_key and fields[9] == player_key) or \
           (fields[3] == player_key and fields[5] == player_key and fields[7] == player_key):
            print(f"{GREEN}Spieler {player_number} hat das Spiel gewonnen! Spieler {other_player} beginnt die nächste RUnde.{RESET}")
            player_points[int(player_number)] += 1
            new_game(int(other_player))
            return True

    if all(value == "x" or value == "o" for value in fields.values()):
        next_player = random.choice([1, 2])
        print(f"{YELLOW}Kein Spieler hat gewonnen! Es gibt ein Unentschieden! Spieler {next_player} beginnt die nächste Runde.{RESET}")
        new_game(next_player)
        return True


    return False

# Neues Spiel starten
def new_game(player_number):
    global fields
    fields = {i: str(i) for i in range(1, 10)}
    print(f"{BLUE}Punkte: Spieler 1 - {player_points[1]} | Spieler 2 - {player_points[2]}{RESET}")
    print_board()

    while True:
        try:
            question = f"Spieler {player_number}: Was tust du? Bitte Feldziffer eingeben!: "
            new_question = question.replace("Spieler 1", f"{PURPLE}Spieler 1{RESET}")
            new_question = new_question.replace("Spieler 2", f"{ORANGE}Spieler 2{RESET}")
            start_new_game_input = int(input(new_question))
            if fields[start_new_game_input] not in ["x", "o"]:
                break
            else:
                print(f"{RED}Dieses Feld ist bereits belegt!{RESET}")
        except (ValueError, KeyError):
            print(f"{RED}Ungültige Eingabe! Bitte wähle eine Zahl zwischen 1 und 9.{RESET}")

    if player_number == 1:
        fields[start_new_game_input] = "x"
        next_player_number = 2
    else:
        fields[start_new_game_input] = "o"
        next_player_number = 1

    print_board()
    next_step(next_player_number)


# Initialize with a default language (e.g. 'de_DE')
language_manager = LanguageManager(default_language='de_DE')

print(language_manager.get_message("test", "TEST_TEST_123 34"))

fields = {}
player_points = {1: 0, 2: 0}


new_game(1)