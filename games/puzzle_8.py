# games/puzzle_8.py
# Solve 8-puzzle manually
# Type 'hint' — A* will suggest the best move
# Main attribute: intelligence

import random
import heapq

GOAL = [1,2,3,4,5,6,7,8,0]

def manhattan_distance(state):
    goal_pos = {1:(0,0),2:(0,1),3:(0,2),
                4:(1,0),5:(1,1),6:(1,2),
                7:(2,0),8:(2,1),0:(2,2)}
    dist = 0
    for r in range(3):
        for c in range(3):
            tile = state[r*3+c]
            if tile != 0:
                gr, gc = goal_pos[tile]
                dist  += abs(r-gr) + abs(c-gc)
    return dist

def draw_puzzle(tiles):
    for i in range(0, 9, 3):
        row = "  "
        for v in tiles[i:i+3]:
            row += f"[{v if v != 0 else ' '}]"
        print(row)
    print(f"  Manhattan distance: {manhattan_distance(tiles)}\n")

def astar_next_move(state):
    start = tuple(state)
    heap  = [(manhattan_distance(state), 0, start, [])]
    seen  = set()

    while heap:
        f, g, curr, path = heapq.heappop(heap)
        if list(curr) == GOAL:
            return path[0] if path else None
        if curr in seen:
            continue
        seen.add(curr)

        zero = curr.index(0)
        adj  = []
        if zero%3 != 0: adj.append(zero-1)
        if zero%3 != 2: adj.append(zero+1)
        if zero >= 3:   adj.append(zero-3)
        if zero <= 5:   adj.append(zero+3)

        for s in adj:
            lst       = list(curr)
            lst[zero], lst[s] = lst[s], lst[zero]
            t2        = tuple(lst)
            if t2 not in seen:
                heapq.heappush(heap, (g+1+manhattan_distance(lst), g+1, t2, path+[lst[zero]]))
    return None

def play_8puzzle(contestant):
    print(f"\n  {'='*50}")
    print(f"  8-PUZZLE  —  {contestant.name}")
    print(f"  {'='*50}")
    print("  Goal:  [1][2][3]")
    print("         [4][5][6]")
    print("         [7][8][ ]")
    print("  0 = blank. Enter the tile number adjacent to blank.")
    print("  Type 'hint' — A* will suggest best move (1 time only)\n")

    # Solvable shuffle
    tiles = [1,2,3,4,5,6,7,8,0]
    for _ in range(30):
        zero = tiles.index(0)
        adj  = []
        if zero%3 != 0: adj.append(zero-1)
        if zero%3 != 2: adj.append(zero+1)
        if zero >= 3:   adj.append(zero-3)
        if zero <= 5:   adj.append(zero+3)
        swap = random.choice(adj)
        tiles[zero], tiles[swap] = tiles[swap], tiles[zero]

    moves     = 0
    max_moves = 40
    hint_used = False
    draw_puzzle(tiles)

    while tiles != GOAL:
        if moves >= max_moves:
            print(f"  {max_moves} moves completed!")
            break

        print(f"  Moves: {moves}/{max_moves}")
        inp = input("  Tile (1-8) or 'hint': ").strip().lower()

        if inp == 'hint':
            if hint_used:
                print("  Hint already used!")
            else:
                next_tile = astar_next_move(tiles)
                if next_tile:
                    print(f"  A* Hint: Move tile {next_tile}!")
                else:
                    print("  A* cannot provide a hint.")
                hint_used = True
            continue

        try:
            tile = int(inp)
            if tile < 1 or tile > 8:
                print("  Enter a number between 1-8!")
                continue
            ti   = tiles.index(tile)
            zero = tiles.index(0)
            adj  = []
            if zero%3 != 0: adj.append(zero-1)
            if zero%3 != 2: adj.append(zero+1)
            if zero >= 3:   adj.append(zero-3)
            if zero <= 5:   adj.append(zero+3)
            if ti in adj:
                tiles[zero], tiles[ti] = tiles[ti], tiles[zero]
                moves += 1
                draw_puzzle(tiles)
            else:
                print("  This tile is not adjacent to blank!")
        except ValueError:
            print("  Enter a number or 'hint'!")

    if tiles == GOAL:
        print(f"  Puzzle solved in {moves} moves!")
        hint_penalty = 15 if hint_used else 0
        base = max(0, 100 - moves*2 - hint_penalty)
        if hint_used:
            print("  (-15 hint penalty)")
    else:
        base = max(5, 40 - manhattan_distance(tiles))

    bonus = round(contestant.intelligence * 0.3)
    score = min(100, base + bonus)
    print(f"  Base: {base}  Intelligence bonus: +{bonus}  Score: {score}")
    return score
