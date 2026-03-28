import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.helpers import sep
from genetic_algorithm import select_top, mutate, add_wildcard
from streamlit_games.game_router import run_game_visual


def play_round(contestants, game_data, round_num):

    active_players = [p for p in contestants if p.alive]

    # 🧠 store round data
    round_info = {
        "round": round_num,
        "game": game_data["name"],
        "players": [],
        "eliminated": []
    }

    # 🎮 Play game for each player
    for player in active_players:

        # ✅ FIXED: use result properly
        result = run_game_visual(game_data, player)

        if isinstance(result, dict):
            score = result.get("score", 0)
        else:
            score = result or 0

        player.game_score = score
        player.calculate_popularity()

        # 📦 store player data
        round_info["players"].append({
            "name": player.name,
            "score": score,
            "popularity": player.popularity
        })

    # ❌ elimination
    survivors = select_top(contestants)

    eliminated_players = [p.name for p in contestants if not p.alive]
    round_info["eliminated"] = eliminated_players

    # 🔁 evolution
    mutate(survivors)

    return round_info


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

        round_info = play_round(contestants, current_game, round_count)

        # ⚠️ NOTE: This still uses input (we’ll fix later)(yaha apr wild card input code tha)
    

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


# alias
run_simulation = run_tournament