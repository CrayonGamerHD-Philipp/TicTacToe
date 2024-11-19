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

fields = {}
player_points = {1: 0, 2: 0}
play_against_ai = False
ai_difficulty = "Easy"  # Standard-Schwierigkeitsgrad


def print_board():
    board = f" " + fields[1] + " | " + fields[2] + " | " + fields[3] + " \n---|---|---\n " + fields[4] + " | " + fields[
        5] + " | " + fields[6] + " \n---|---|---\n " + fields[7] + " | " + fields[8] + " | " + fields[9] + " "
    new_board = board.replace("x", f"{PURPLE}x{RESET}")
    new_board = new_board.replace("o", f"{ORANGE}o{RESET}")
    print(new_board)


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
            print(language_manager.get_message("winner","{GREEN}Player {player_number} has won the game! Player {other_player} starts the next round.{RESET}", player_number=player_number, other_player=other_player, GREEN=GREEN, RESET=RESET))
            player_points[int(player_number)] += 1
            new_game(int(other_player))
            return True

    if all(value == "x" or value == "o" for value in fields.values()):
        next_player = random.choice([1, 2])
        print(language_manager.get_message("draw", "{YELLOW}No player has won! It’s a tie! Player {next_player} starts the next round.{RESET}", next_player=next_player, YELLOW=YELLOW, RESET=RESET))
        new_game(next_player)
        return True

    return False


def ai_move():
    if ai_difficulty == "Easy":
        return ai_easy()
    elif ai_difficulty == "Medium":
        return ai_medium()
    elif ai_difficulty == "Hard":
        return ai_hard()
    elif ai_difficulty == "Extreme":
        return ai_extreme()


def ai_easy():
    free_fields = [key for key, value in fields.items() if value not in ["x", "o"]]
    return random.choice(free_fields)


def ai_medium():
    free_fields = [key for key, value in fields.items() if value not in ["x", "o"]]
    for key in free_fields:
        fields[key] = "x"
        if check_winner_no_reset("x"):
            fields[key] = "o"
            return key
        fields[key] = str(key)
    return random.choice(free_fields)


def ai_hard():
    free_fields = [key for key, value in fields.items() if value not in ["x", "o"]]
    for key in free_fields:
        fields[key] = "o"
        if check_winner_no_reset("o"):
            return key
        fields[key] = "x"
        if check_winner_no_reset("x"):
            fields[key] = "o"
            return key
        fields[key] = str(key)
    return random.choice(free_fields)


def ai_extreme():
    best_score = float('-inf')
    best_move = None
    for key in [key for key in fields if fields[key] not in ["x", "o"]]:
        fields[key] = "o"
        score = minimax(False)
        fields[key] = str(key)
        if score > best_score:
            best_score = score
            best_move = key
    return best_move


def minimax(is_maximizing):
    if check_winner_no_reset("o"):
        return 1
    if check_winner_no_reset("x"):
        return -1
    if all(value in ["x", "o"] for value in fields.values()):
        return 0

    if is_maximizing:
        best_score = float('-inf')
        for key in [key for key in fields if fields[key] not in ["x", "o"]]:
            fields[key] = "o"
            score = minimax(False)
            fields[key] = str(key)
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for key in [key for key in fields if fields[key] not in ["x", "o"]]:
            fields[key] = "x"
            score = minimax(True)
            fields[key] = str(key)
            best_score = min(score, best_score)
        return best_score


def check_winner_no_reset(player_key):
    return (
            (fields[1] == player_key and fields[2] == player_key and fields[3] == player_key) or
            (fields[4] == player_key and fields[5] == player_key and fields[6] == player_key) or
            (fields[7] == player_key and fields[8] == player_key and fields[9] == player_key) or
            (fields[1] == player_key and fields[4] == player_key and fields[7] == player_key) or
            (fields[2] == player_key and fields[5] == player_key and fields[8] == player_key) or
            (fields[3] == player_key and fields[6] == player_key and fields[9] == player_key) or
            (fields[1] == player_key and fields[5] == player_key and fields[9] == player_key) or
            (fields[3] == player_key and fields[5] == player_key and fields[7] == player_key)
    )


def mode_selector():
    global play_against_ai
    print(language_manager.get_message(
        "game_mode_selection",
        "{BLUE}Please select a game mode:{RESET}\n1. Play against another Player\n2. Play against the AI",
        BLUE=BLUE,
        RESET=RESET
    ))
    while True:
        try:
            mode = int(input(language_manager.get_message(
                "select_game_mode",
                "{BLUE}Select game mode: {RESET}",
                BLUE=BLUE,
                RESET=RESET
            )))
            if mode == 1:
                play_against_ai = False
                break
            elif mode == 2:
                play_against_ai = True
                difficulty_selector()
                break
            else:
                print(language_manager.get_message(
                    "invalid_selection",
                    "{RED}Invalid selection! Please try again.{RESET}",
                    RED=RED,
                    RESET=RESET
                ))
        except ValueError:
            print(language_manager.get_message(
                "invalid_selection",
                "{RED}Invalid selection! Please try again.{RESET}",
                RED=RED,
                RESET=RESET
            ))


def difficulty_selector():
    global ai_difficulty
    print(language_manager.get_message(
        "difficulty_selection",
        "{BLUE}Please select AI difficulty:{RESET}\n1. Easy\n2. Medium\n3. Hard\n4. Extreme",
        BLUE=BLUE,
        RESET=RESET
    ))
    difficulties = ["Easy", "Medium", "Hard", "Extreme"]
    while True:
        try:
            choice = int(input(language_manager.get_message(
                "your_choice",
                "{BLUE}Your choice: {RESET}",
                BLUE=BLUE,
                RESET=RESET
            ))) - 1
            if 0 <= choice < len(difficulties):
                ai_difficulty = difficulties[choice]
                break
            else:
                print(language_manager.get_message(
                    "invalid_selection",
                    "{RED}Invalid selection! Please try again.{RESET}",
                    RED=RED,
                    RESET=RESET
                ))
        except ValueError:
            print(language_manager.get_message(
                "invalid_selection",
                "{RED}Invalid selection! Please try again.{RESET}",
                RED=RED,
                RESET=RESET
            ))

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


def next_step(player_int):
    while not check_winner():
        if not play_against_ai or (play_against_ai and player_int == 1):
            player_color = PURPLE if player_int == 1 else ORANGE
            question = language_manager.get_message("next_step_message", "{player_color}Player {player_str}{RESET}: How do you want to proceed? Please enter field number!: ",
                player_str=str(player_int),  # Hier wird player_str korrekt übergeben
                RESET=RESET,
                player_color=player_color
            )

            try:
                game_input = int(input(question))
            except ValueError:
                print(language_manager.get_message(
                    "invalid_input",
                    "{RED}Invalid input! Please select a number between 1 and 9.{RESET}",
                    RED=RED,
                    RESET=RESET
                ))
                continue

            if 0 < game_input <= 9 and fields[game_input] not in ["x", "o"]:
                fields[game_input] = "x" if player_int == 1 else "o"
                print_board()
                player_int = 2 if player_int == 1 else 1
            else:
                print(language_manager.get_message(
                    "field_taken",
                    "{RED}This field is already taken!{RESET}",
                    RED=RED,
                    RESET=RESET
                ))
        elif play_against_ai and player_int == 2:
            print(language_manager.get_message(
                "ai_move",
                "{ORANGE}AI is making its move...{RESET}",
                ORANGE=ORANGE,
                RESET=RESET
            ))
            ai_choice = ai_move()
            fields[ai_choice] = "o"
            print_board()
            player_int = 1


def new_game(player_number):
    global fields
    fields = {i: str(i) for i in range(1, 10)}
    print(language_manager.get_message("points",
                                       "{BLUE}Points: Player 1 - {player_points_1} | Player 2 - {player_points_2}{RESET}",
                                       player_points_1=player_points[1], player_points_2=player_points[2], BLUE=BLUE,
                                       RESET=RESET))
    print_board()
    next_step(player_number)


language_manager = LanguageManager(default_language="en_US")
language_selector()
mode_selector()

new_game(1)
