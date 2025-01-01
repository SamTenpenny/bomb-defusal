import time
import os
import threading

# Initial timers and game states
bomb_timer = 20
defuse_timer = 10
bomb_active = True
defusing = False
round_over_flag = False
game_over_flag = False

# Scoreboard
counter_terrorist_score = 0
terrorist_score = 0
winning_score = 10

# Thread handles
threads = []

# Function to create a progress bar
def create_progress_bar(current, total, length=30, label=""):
    filled_length = int(length * current / total)
    bar = '█' * filled_length + '-' * (length - filled_length)
    return f"{label} |{bar}|"

# Round-over function
def round_over(message, team):
    global bomb_active, round_over_flag, bomb_timer, defuse_timer
    bomb_active = False
    round_over_flag = True
    os.system('cls' if os.name == 'nt' else 'clear')
    time.sleep(2)
    print(message)
    time.sleep(2)
    print(team)
    time.sleep(2)
    print("Round Over")
    time.sleep(2)
    print(f"Counter-Terrorists: {counter_terrorist_score} | Terrorists: {terrorist_score}")
    time.sleep(4)
    reset_round()

# Game-over function
def game_over():
    global game_over_flag
    game_over_flag = True
    os.system('cls' if os.name == 'nt' else 'clear')
    winner = "Counter-Terrorists" if counter_terrorist_score == winning_score else "Terrorists"
    print(f"Game Over! {winner} win!")
    time.sleep(2)
    print(f"Final Score:\nCounter-Terrorists: {counter_terrorist_score}\nTerrorists: {terrorist_score}")
    time.sleep(5)
    os.system('cls' if os.name == 'nt' else 'clear')
    exit()

# Reset round function
def reset_round():
    global bomb_timer, defuse_timer, bomb_active, round_over_flag, threads
    bomb_timer = 20
    defuse_timer = 10
    bomb_active = True
    round_over_flag = False
    threads = []  # Clear thread list
    start_round()  # Start the next round

# Bomb countdown function
def bomb_countdown():
    global bomb_timer, bomb_active, terrorist_score
    while bomb_timer > 0 and not round_over_flag and not game_over_flag:
        if not bomb_active:
            break
        bomb_bar = create_progress_bar(bomb_timer, 20, label="Bomb Timer")
        defuse_bar = create_progress_bar(defuse_timer, 10, label="Defuse Timer") if defusing else create_progress_bar(10, 10, label="Defuse Timer")
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Counter-Terrorists: {counter_terrorist_score} | Terrorists: {terrorist_score}")
        print(bomb_bar)
        print(defuse_bar)
        time.sleep(.5)
        bomb_timer -= .5
    if bomb_timer == 0 and not round_over_flag and not game_over_flag:
        terrorist_score += 1
        if terrorist_score == winning_score:
            game_over()
        else:
            round_over("Detonating!", "Terrorists Win!")

# Defuse function
def defuse():
    global defuse_timer, counter_terrorist_score
    while not round_over_flag and not game_over_flag:
        if not bomb_active:
            continue
        if defusing:
            if defuse_timer > 0:
                defuse_timer -= .5
            else:
                counter_terrorist_score += 1
                if counter_terrorist_score == winning_score:
                    game_over()
                else:
                    round_over("Bomb defused!", "Counter-Terrorists Win!")
        else:
            defuse_timer = 10
        time.sleep(.5)

# Key listener function
def listen_for_defuse():
    global defusing
    try:
        import keyboard
        while not round_over_flag and not game_over_flag:
            if keyboard.is_pressed('e'):
                defusing = True
            else:
                defusing = False
            time.sleep(0.1)
    except ImportError:
        print("\nThe `keyboard` module is required for this script.")
        exit()

# Start round function
def start_round():
    global threads
    bomb_thread = threading.Thread(target=bomb_countdown)
    defuse_thread = threading.Thread(target=defuse)
    key_listener_thread = threading.Thread(target=listen_for_defuse)
    threads = [bomb_thread, defuse_thread, key_listener_thread]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

# Main game loop
if __name__ == "__main__":
    while not game_over_flag:
        start_round()
