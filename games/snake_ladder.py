# games/snake_ladder.py
# Roll dice and reach 100
# Main attribute: adaptability

import random

SNAKES  = {16:6, 47:26, 49:11, 56:53, 62:19, 64:60, 87:24, 93:73, 95:75, 99:78}
LADDERS = {4:14, 9:31, 20:38, 28:84, 40:59, 51:67, 63:81, 71:91}

def play_snake_ladder(contestant):
    print(f"\n  {'='*50}")
    print(f"  SNAKE AND LADDER  —  {contestant.name}")
    print(f"  {'='*50}")
    print("  Reach 100! Press Enter to roll the dice.")
    print(f"  Snakes:  {SNAKES}")
    print(f"  Ladders: {LADDERS}\n")

    pos       = 0
    turns     = 0
    max_turns = 30

    while pos < 100 and turns < max_turns:
        input(f"  [Turn {turns+1}] Position: {pos} — Press Enter...")
        dice = random.randint(1, 6)
        new  = pos + dice
        print(f"  Dice: {dice}  →  {pos} + {dice} = {new}", end="")

        if new > 100:
            print("  (Overshot, stay)")
        elif new in SNAKES:
            print(f"  SNAKE! {new} → {SNAKES[new]}  (Bitten!)")
            pos = SNAKES[new]
        elif new in LADDERS:
            print(f"  LADDER! {new} → {LADDERS[new]}  (Climbed!)")
            pos = LADDERS[new]
        else:
            pos = new
            print()

        print(f"  Current position: {pos}\n")
        turns += 1

        if pos >= 100:
            print(f"  WINNER! Reached 100 in {turns} turns!")
            break

    if pos < 100:
        print(f"  {max_turns} turns completed. Final position: {pos}")

    base  = round((pos / 100) * 80) + max(0, max_turns - turns)
    bonus = round(contestant.adaptability * 0.25)
    score = min(100, base + bonus)
    print(f"\n  Position: {pos}/100  Base: {base}  Adaptability bonus: +{bonus}  Score: {score}")
    return score
