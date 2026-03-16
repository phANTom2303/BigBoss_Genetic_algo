# main.py - Start here

import sys
import os
import random

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.helpers import sep
from contestant import Contestant
from games import ALL_GAMES
from core.game_engine import run_tournament as run_simulation

def make_team():
    """Make 20 players"""
    print("Making team...")
    team = []
    
    for i in range(20):
        name = f"Player{i+1}"
        brain = random.randint(40, 100)
        talk = random.randint(40, 100)
        body = random.randint(40, 100)
        flex = random.randint(40, 100)
        
        player = Contestant(name, brain, talk, body, flex)
        player.calculate_popularity()
        team.append(player)
    
    print("Team ready!")
    return team

def pick_games():
    """Choose games"""
    print("\nGames:")
    for game in ALL_GAMES:
        print(f"{game['no']}. {game['name']}")
    
    choice = input("Pick numbers or 'all': ")
    
    if choice == 'all':
        return ALL_GAMES
    
    numbers = [int(x) for x in choice.split(',')]
    games = [g for g in ALL_GAMES if g['no'] in numbers]
    return games

def main():
    """Run game"""
    while True:
        print("\nStart game!")
        players = make_team()
        games = pick_games()
        
        play_again = run_simulation(players, games)
        if not play_again:
            print("Bye!")
            break

if __name__ == "__main__":
    main()