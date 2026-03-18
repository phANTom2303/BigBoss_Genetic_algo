# games/puzzle_8.py
# A* solves 8-puzzle automatically
# Main attribute: intelligence

import random
import heapq

GOAL = [1,2,3,4,5,6,7,8,0]

def manhattan_distance(state):
    goal_pos = {1:(0,0), 2:(0,1), 3:(0,2),
                4:(1,0), 5:(1,1), 6:(1,2),
                7:(2,0), 8:(2,1), 0:(2,2)}
    dist = 0
    for r in range(3):
        for c in range(3):
            tile = state[r*3+c]
            if tile != 0:
                gr, gc = goal_pos[tile]
                dist  += abs(r-gr) + abs(c-gc)
    return dist

def astar_solve(state):
    start = tuple(state)
    heap  = [(manhattan_distance(state), 0, start, [])]
    seen  = set()

    while heap:
        f, g, curr, moves = heapq.heappop(heap)

        if list(curr) == GOAL:
            return moves

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
            lst = list(curr)
            lst[zero], lst[s] = lst[s], lst[zero]
            t2 = tuple(lst)
            if t2 not in seen:
                heapq.heappush(heap,
                    (g+1+manhattan_distance(lst), g+1, t2, moves+[lst[zero]]))
    return []

def draw_puzzle(tiles):
    for i in range(0, 9, 3):
        row = "  "
        for v in tiles[i:i+3]:
            row += f"[{v if v!=0 else ' '}]"
        print(row)

def play_8puzzle(contestant):
    print(f"\n  8-PUZZLE — {contestant.name}")
    print("  A* solving automatically...\n")

    # Generate solvable shuffle
    tiles = [1,2,3,4,5,6,7,8,0]
    for _ in range(20):
        zero = tiles.index(0)
        adj  = []
        if zero%3 != 0: adj.append(zero-1)
        if zero%3 != 2: adj.append(zero+1)
        if zero >= 3:   adj.append(zero-3)
        if zero <= 5:   adj.append(zero+3)
        swap = random.choice(adj)
        tiles[zero], tiles[swap] = tiles[swap], tiles[zero]

    print("  Initial state:")
    draw_puzzle(tiles)
    print(f"  Manhattan distance: {manhattan_distance(tiles)}")

    # A* solves automatically
    moves = astar_solve(tiles)

    # Apply all moves
    for tile in moves:
        ti   = tiles.index(tile)
        zero = tiles.index(0)
        tiles[zero], tiles[ti] = tiles[ti], tiles[zero]

    print(f"\n  Solved in {len(moves)} moves!")
    print("  Final state:")
    draw_puzzle(tiles)

    base  = max(0, 100 - len(moves)*2)
    bonus = round(contestant.intelligence * 0.3)
    score = min(100, base + bonus)
    print(f"  Base:{base}  Intelligence bonus:+{bonus}  Score:{score}")
    return score
