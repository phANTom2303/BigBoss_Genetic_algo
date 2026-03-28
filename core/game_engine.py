import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.helpers import sep
from genetic_algorithm import select_top, mutate, add_wildcard


#  PvP handler
def play_pvp_round(active_players, game_function):
    import random

    print("\n⚔️ PLAYER vs PLAYER MATCHES\n")

    random.shuffle(active_players)

    for i in range(0, len(active_players), 2):

        if i + 1 >= len(active_players):
            p = active_players[i]
            p.game_score = random.randint(40, 70)
            print(f"{p.name} gets a bye. Score: {p.game_score}")
            continue

        p1 = active_players[i]
        p2 = active_players[i+1]

        print("\n" + "="*20 + f" {p1.name} vs {p2.name} " + "="*20)

        results = game_function(p1, p2)

        for player, score in results:
            player.game_score = score
            print(f"{player.name} scored: {score}")


#  MAIN ROUND FUNCTION
def play_round(contestants, game_data, round_num):

    active_players = [p for p in contestants if p.alive]

    print("\n" + "="*50)
    print("ROUND", round_num)
    print("Game:", game_data['name'])
    print("Main skill:", game_data['main_attr'])
    print("="*50)
    print(len(active_players), "players competing\n")

    game_function = game_data["fn"]

    # PvP game
    if game_data["name"] == "Tic Tac Toe":
        play_pvp_round(active_players, game_function)

    # 🎮 Normal games
    else:
        for player in active_players:
            print("\n" + "="*25, player.name + "'s turn", "="*25)
            player.game_score = game_function(player)
            print(player.name, "scored:", player.game_score)

    #  COMMON (for ALL games)
    for player in active_players:
        player.calculate_popularity()

    print("\nROUND RESULTS")
    print("-" * 40)
    for player in sorted(active_players, key=lambda p: p.game_score, reverse=True):
        print(f"{player.name:12} | Score: {player.game_score:3d} | Pop: {player.popularity:3d}")

    print("\nELIMINATION")
    survivors = select_top(contestants)

    if len([p for p in contestants if p.alive]) == 1:
        return True

    print("\nEVOLUTION PHASE")
    mutate(survivors)

    return False


#  TOURNAMENT LOOP
def run_tournament(contestants, games_list):

    print("\nSTARTING LINEUP")
    for i, player in enumerate(contestants, 1):
        print(f"{i:2d}. {player.name} - Pop: {player.popularity}")

    round_count = 0
    wildcard_done = False

    while True:
        live_players = [p for p in contestants if p.alive]
        if len(live_players) == 1:
            break

        round_count += 1
        current_game = games_list[(round_count - 1) % len(games_list)]

        finished = play_round(contestants, current_game, round_count)
        if finished:
            break

        if not wildcard_done and 2 <= round_count <= 4:
            answer = input("Add wildcard? (y/n): ").strip().lower()
            if answer == 'y':
                add_wildcard(contestants)
                wildcard_done = True

        print("\nCURRENT STANDINGS")
        print("-" * 25)
        for rank, player in enumerate(
            sorted([p for p in contestants if p.alive],
                   key=lambda p: p.popularity, reverse=True), 1):
            print(f"{rank:2d}. {player.name} (Pop: {player.popularity})")

    winner = [p for p in contestants if p.alive][0]
    sep()
    print("FINAL WINNER:")
    print(winner.name)
    print(winner)
    sep()

    return input("Play again? (y/n): ").strip().lower() == 'y'


run_simulation = run_tournament