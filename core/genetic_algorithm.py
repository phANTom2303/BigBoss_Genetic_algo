# genetic_algorithm.py - Simple GA

import random
from contestant import Contestant

# -----------------------------
# SELECTION
# -----------------------------

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


# -----------------------------
# MUTATION (EVOLUTION)
# -----------------------------

def improve_stats(winners):
    """Make winners better based on score"""
    best_score = max(c.game_score for c in winners) or 1
    
    for c in winners:
        boost_size = round((c.game_score / best_score) * random.randint(3, 10))
        
        c.intelligence  += random.randint(0, boost_size)
        c.communication += random.randint(0, boost_size)
        c.physical      += random.randint(0, boost_size)
        c.adaptability  += random.randint(0, boost_size)
        
        # cap at 99
        c.intelligence  = min(99, c.intelligence)
        c.communication = min(99, c.communication)
        c.physical      = min(99, c.physical)
        c.adaptability  = min(99, c.adaptability)
        
        c.calculate_popularity()
    
    print(f"Improved {len(winners)} winners")


# -----------------------------
# WILDCARD (STREAMLIT SAFE)
# -----------------------------

def add_new_guy(contestants):
    """Add wildcard player (no CLI input)"""

    name = f"Wildcard{len(contestants) + 1}"

    intel = random.randint(40, 100)
    talk  = random.randint(40, 100)
    body  = random.randint(40, 100)
    adaptability = random.randint(40, 100)

    new_guy = Contestant(name, intel, talk, body, adaptability)
    new_guy.calculate_popularity()
    new_guy.is_wildcard = True

    contestants.append(new_guy)

    print(f"NEW: {new_guy.name} (pop {new_guy.popularity})")

    return new_guy


# -----------------------------
# ALIASES (USED BY ENGINE)
# -----------------------------

select_top   = pick_best
mutate       = improve_stats
add_wildcard = add_new_guy