# games/snake_ladder.py
# Roll dice and reach 100
# Main attribute: adaptability

import random

def play_snake_ladder(contestant):
    SNAKES  = {16:6, 47:26, 49:11, 56:53, 62:19, 64:60, 87:24, 93:73, 95:75, 99:78}
    LADDERS = {4:14, 9:31, 20:38, 28:84, 40:59, 51:67, 63:81, 71:91}

    print(f"\n  SNAKE AND LADDER — {contestant.name}")

    pos, turns, max_turns = 0, 0, 30

    while pos < 100 and turns < max_turns:
        dice = random.randint(1, 6)
        new  = pos + dice

        if new > 100:
            print(f"  Turn {turns+1}: Dice={dice} → Out of bounds!")
        elif new in SNAKES:
            print(f"  Turn {turns+1}: Dice={dice} → SNAKE! {new}→{SNAKES[new]}")
            pos = SNAKES[new]
        elif new in LADDERS:
            print(f"  Turn {turns+1}: Dice={dice} → LADDER! {new}→{LADDERS[new]}")
            pos = LADDERS[new]
        else:
            pos = new
            print(f"  Turn {turns+1}: Dice={dice} → Position={pos}")

        turns += 1
        if pos >= 100:
            print(f"  Reached 100 in {turns} turns!")
            break

    base  = round((pos / 100) * 80) + max(0, max_turns - turns)
    bonus = round(contestant.adaptability * 0.25)
    score = min(100, base + bonus)
    print(f"  Final Position:{pos}  Score:{score}")
    return score