# game_engine.py - Main game controller

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.helpers import sep
from genetic_algorithm import select_top, mutate, add_wildcard

def play_round(contestants, game_data, round_num):
    """Handle one full round: challenge, scoring, elimination, evolution"""
    
    active_players = [p for p in contestants if p.alive]
    
    print("\n" + "="*50)
    print("ROUND", round_num)
    print("Game:", game_data['name'])
    print("Main skill:", game_data['main_attr']) 
    print("="*50)
    print()
    print(len(active_players), "players competing")
    print()
    
    # All players take their turn
    for player in active_players:
        print("\n" + "="*25, player.name + "'s turn", "="*25)
        player.game_score = game_data["fn"](player)
        print(player.name, "scored:", player.game_score)
        input("Press Enter for next player...")
    
    # Recalculate popularity based on performance
    for player in active_players:
        player.calculate_popularity()
    
    # Display results table
    print("\nROUND RESULTS")
    print("-" * 40)
    sorted_players = sorted(active_players, key=lambda p: p.game_score, reverse=True)
    for player in sorted_players:
        print(f"{player.name:12} | Score: {player.game_score:3d} | Pop: {player.popularity:3d}")
    
    # Eliminate bottom performers
    print("\nELIMINATION")
    survivors = select_top(contestants)
    
    # Check for single winner
    if len([p for p in contestants if p.alive]) == 1:
        return True
    
    # Survivors improve their stats
    print("\nEVOLUTION PHASE")
    mutate(survivors)
    
    return False

def run_tournament(contestants, games_list):
    """Complete game from start to winner"""
    
    print("\nSTARTING LINEUP")
    for i, player in enumerate(contestants, 1):
        print(f"{i:2d}. {player.name} - Pop: {player.popularity}")
    
    input("Press Enter to begin...")
    
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
        
        # Wildcard entry option
        if not wildcard_done and 2 <= round_count <= 4:
            answer = input("Add wildcard player? (y/n): ").strip().lower()
            if answer == 'y':
                add_wildcard(contestants)
                wildcard_done = True
        
        # Show current standings
        print("\nCURRENT STANDINGS")
        print("-" * 25)
        standings = sorted([p for p in contestants if p.alive], 
                          key=lambda p: p.popularity, reverse=True)
        for rank, player in enumerate(standings, 1):
            print(f"{rank:2d}. {player.name} (Pop: {player.popularity})")
        
        input("Press Enter for next round...")
    
    # Announce winner
    winner = [p for p in contestants if p.alive][0]
    sep()
    print("FINAL WINNER:")
    print(winner.name)
    print(winner)
    sep()
    
    # Ask to replay
    return input("Play again? (y/n): ").strip().lower() == 'y'