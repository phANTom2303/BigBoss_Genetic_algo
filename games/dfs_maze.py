# games/dfs_maze.py
# DFS explores path using a stack
# Explores more nodes than BFS
# Main attribute: adaptability

import time
from utils.helpers import draw_maze

MAZE = [
    [1,1,0,1,1,1],
    [0,1,0,1,0,1],
    [0,1,1,1,0,1],
    [0,0,0,1,1,1],
    [1,1,1,0,0,1],
    [1,0,1,1,1,1],
]
ROWS, COLS = 6, 6

def get_valid_cell(label, maze, rows, cols):
    while True:
        try:
            r = int(input(f"  {label} Row (0-{rows-1}): "))
            c = int(input(f"  {label} Col (0-{cols-1}): "))
            if 0<=r<rows and 0<=c<cols:
                if maze[r][c] == 1:
                    return (r, c)
                print("  Wall here! Choose an empty cell.")
            else:
                print(f"  Enter a value between 0 and {rows-1}!")
        except ValueError:
            print("  Enter only numbers!")

def play_dfs(contestant):
    print(f"\n  {'='*50}")
    print(f"  DFS MAZE SOLVER  —  {contestant.name}")
    print(f"  {'='*50}")
    print("  DFS will explore deeply using a stack!")
    print("  Compare with BFS — explores more nodes.\n")

    print("  Maze:")
    draw_maze(MAZE, ROWS, COLS)

    print("  Choose start and end positions:")
    start = get_valid_cell("Start", MAZE, ROWS, COLS)
    end   = get_valid_cell("End  ", MAZE, ROWS, COLS)

    if start == end:
        print("  Same position! Score: 50")
        return 50

    print(f"\n  DFS running: {start} → {end}")
    print("  Stack-based exploration:\n")

    stack    = [(start, [start])]
    visited  = set()
    explored = 0
    path     = None

    while stack:
        (r, c), curr_path = stack.pop()
        if (r, c) in visited:
            continue
        visited.add((r, c))
        explored += 1
        print(f"  Exploring: ({r},{c})  |  Stack size:{len(stack)}  |  Visited:{explored}")
        time.sleep(0.1)

        if (r, c) == end:
            path = curr_path
            break

        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r+dr, c+dc
            if 0<=nr<ROWS and 0<=nc<COLS and MAZE[nr][nc]==1 and (nr,nc) not in visited:
                stack.append(((nr,nc), curr_path+[(nr,nc)]))

    print()
    if path:
        print(f"  Path found! Length: {len(path)} steps")
        print(f"  Path: {' → '.join(str(p) for p in path)}")
        print("\n  Maze with DFS path:")
        draw_maze(MAZE, ROWS, COLS, start=start, end=end, path=path)
        base = max(20, 100 - explored//3)
    else:
        print("  Path not found!")
        base = 10

    bonus = round(contestant.adaptability * 0.3)
    score = min(100, base + bonus)
    print(f"  Explored: {explored} nodes  Path: {len(path) if path else 0} steps")
    print(f"  Base: {base}  Adaptability bonus: +{bonus}  Score: {score}")
    return score
