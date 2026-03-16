# genetic_algorithm.py - Simple GA

import random
from contestant import Contestant
from utils.helpers import get_int

def pick_best(contestants):
    """Keep top 65% by popularity"""
    alive = [c for c in contestants if c.alive]
    alive.sort(key=lambda c: c.popularity, reverse=True)
    keep = max(1, round(len(alive) * 0.65))
    
    print(f"\nKeep top {keep} of {len(alive)}")
    for c in alive[keep:]:
        c.alive = False
        print(f"Gone: {c.name} (pop {c.popularity})")
    
    return [c for c in contestants if c.alive]

def improve_stats(winners):
    """Make winners better based on score"""
    best_score = max(c.game_score for c in winners) or 1
    
    for c in winners:
        boost_size = round((c.game_score / best_score) * random.randint(3, 10))
        
        c.intelligence  += random.randint(0, boost_size)
        c.communication += random.randint(0, boost_size)
        c.physical      += random.randint(0, boost_size)
        c.adaptability  += random.randint(0, boost_size)
        
        if c.intelligence  > 99: c.intelligence  = 99
        if c.communication > 99: c.communication = 99
        if c.physical      > 99: c.physical      = 99
        if c.adaptability  > 99: c.adaptability  = 99
        
        c.calculate_popularity()
    
    print(f"Improved {len(winners)} winners")

def add_new_guy(contestants):
    """Add wildcard player"""
    print("\n--- New Player ---")
    name = input("Name: ").strip() or "New★"
    
    intel = get_int("Smart: ")
    talk  = get_int("Talk: ")
    body  = get_int("Body: ")
    flex  = get_int("Flex: ")
    
    new_guy = Contestant(name, intel, talk, body, flex)
    new_guy.calculate_popularity()
    new_guy.is_wildcard = True
    contestants.append(new_guy)
    print(f"NEW: {new_guy.name} (pop {new_guy.popularity})")

# ← Add these 3 lines at the bottom
select_top   = pick_best       # game_engine calls select_top
mutate       = improve_stats   # game_engine calls mutate
add_wildcard = add_new_guy     # game_engine calls add_wildcard