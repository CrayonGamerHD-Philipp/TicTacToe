import random
from language_manager import LanguageManager

# Farben
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
ORANGE = "\033[38;5;214m"
PURPLE = "\033[38;5;129m"
RESET = "\033[0m"

# Create board and print it
def print_board():
    board = f" " + fields[1] + " | " + fields[2] + " | " + fields[3] + " \n---|---|---\n " + fields[4] + " | " + fields[5] + " | " + fields[6] + " \n---|---|---\n " + fields[7] + " | " + fields[8] + " | " + fields[9] + " "
    new_board = board.replace("x", f"{PURPLE}x{RESET}")
    new_board = new_board.replace("o", f"{ORANGE}o{RESET}")
    print(new_board)

# Next step
def next_step(player_int):
    while not check_winner():
        player_str = str(player_int)
        player_color = PURPLE
        if player_int == 2: player_color = ORANGE

        question = language_manager.get_message("next_step_message", "{player_color}Player {player_str}{RESET}: How do you want to proceed? Please enter field number!: ", player_str=player_str, RESET=RESET, player_color=player_color)

        try:
            game_input = int(input(question))
        except ValueError:
            print(language_manager.get_message("invalid_input", "{RED}Invalid input! Please select a number between 1 and 9.{RESET}", RED=RED, RESET=RESET))
            continue

        if 0 < game_input <= 9:
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
                print(language_manager.get_message("field_taken", "{RED}This field is already taken!{RESET}", RED=RED, RESET=RESET))
        else:
            print(language_manager.get_message("invalid_input", "{RED}Invalid input! Please select a number between 1 and 9.{RESET}", RED=RED, RESET=RESET))

# Check winner
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
            print(language_manager.get_message("winner", "{GREEN}Player {player_number} has won the game! Player {other_player} starts the next round.{RESET}", player_number=player_number, other_player=other_player, GREEN=GREEN, RESET=RESET))
            player_points[int(player_number)] += 1
            new_game(int(other_player))
            return True

    if all(value == "x" or value == "o" for value in fields.values()):
        next_player = random.choice([1, 2])
        print(language_manager.get_message("draw", "{YELLOW}No player has won! It’s a tie! Player {next_player} starts the next round.{RESET}", next_player=next_player, YELLOW=YELLOW, RESET=RESET))
        new_game(next_player)
        return True

    return False

# Start new game
def new_game(player_number):
    global fields
    fields = {i: str(i) for i in range(1, 10)}
    print(language_manager.get_message(
        "points",
        "{BLUE}Points: Player 1 - {player_points_1} | Player 2 - {player_points_2}{RESET}",
        player_points_1=player_points[1],
        player_points_2=player_points[2],
        BLUE=BLUE,
        RESET=RESET
    ))

    print_board()

    player_color = PURPLE
    if player_number == 2: player_color = ORANGE

    while True:
        try:

            question = language_manager.get_message("next_game_message", "{player_color}Player {player_str}{RESET}: What would you like to do? Please enter field number!: ", player_str=str(player_number), player_color=player_color, RESET=RESET)
            start_new_game_input = int(input(question))
            if fields[start_new_game_input] not in ["x", "o"]:
                break
            else:
                print(language_manager.get_message("field_taken", "{RED}This field is already taken!{RESET}", RED=RED, RESET=RESET))
        except (ValueError, KeyError):
            print(language_manager.get_message("invalid_input", "{RED}Invalid input! Please select a number between 1 and 9.{RESET}", RED=RED, RESET=RESET))

    if player_number == 1:
        fields[start_new_game_input] = "x"
        next_player_number = 2
    else:
        fields[start_new_game_input] = "o"
        next_player_number = 1

    print_board()
    next_step(next_player_number)

# Language selector in the console
def language_selector():
    available_languages = language_manager.get_available_languages()

    if not available_languages:
        print("No languages available.")
        return

    print("Please select a language by entering the corresponding number:")
    for i, (code, name) in enumerate(available_languages, start=1):
        print(f"{i}. {name} ({code})")

    while True:
        try:
            choice = int(input("\nYour choice: ")) - 1
            if 0 <= choice < len(available_languages):
                selected_language = available_languages[choice][0]  # Get the language code
                language_manager.set_language(selected_language)
                break
            else:
                print("Invalid choice, please enter a valid number.")
        except ValueError:
            print("Please enter a number corresponding to your choice.")

# Init LanguageManager
language_manager = LanguageManager(default_language="en_US")
language_selector()

# Standard variables
fields = {}
player_points = {1: 0, 2: 0}

# Start first game
new_game(1)
