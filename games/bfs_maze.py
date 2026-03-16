# games/bfs_maze.py
# BFS automatically finds shortest path
# Player chooses start/end positions
# Main attribute: intelligence

import time
from collections import deque
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

def play_bfs(contestant):
    print(f"\n  {'='*50}")
    print(f"  BFS MAZE SOLVER  —  {contestant.name}")
    print(f"  {'='*50}")
    print("  BFS will find the shortest path — watch live!")
    print("  [.]=Open  [#]=Wall\n")

    print("  Maze:")
    draw_maze(MAZE, ROWS, COLS)

    print("  Choose start and end positions:")
    start = get_valid_cell("Start", MAZE, ROWS, COLS)
    end   = get_valid_cell("End  ", MAZE, ROWS, COLS)

    if start == end:
        print("  Same position! Score: 50")
        return 50

    print(f"\n  BFS running: {start} → {end}")
    print("  Exploring nodes:\n")

    queue    = deque([(start, [start])])
    visited  = {start}
    explored = 0
    path     = None

    while queue:
        (r, c), curr_path = queue.popleft()
        explored += 1
        print(f"  Exploring: ({r},{c})  |  Visited: {explored}")
        time.sleep(0.1)

        if (r, c) == end:
            path = curr_path
            break

        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r+dr, c+dc
            if 0<=nr<ROWS and 0<=nc<COLS and MAZE[nr][nc]==1 and (nr,nc) not in visited:
                visited.add((nr, nc))
                queue.append(((nr,nc), curr_path+[(nr,nc)]))

    print()
    if path:
        print(f"  Shortest path found! Length: {len(path)} steps")
        print(f"  Path: {' → '.join(str(p) for p in path)}")
        print("\n  Maze with path (P=path S=start E=end):")
        draw_maze(MAZE, ROWS, COLS, start=start, end=end, path=path)
        base = max(20, 100 - len(path)*5 - explored//3)
    else:
        print("  No path found!")
        base = 10

    bonus = round(contestant.intelligence * 0.3)
    score = min(100, base + bonus)
    print(f"  Path: {len(path) if path else 0} steps  Explored: {explored} nodes")
    print(f"  Base: {base}  Intelligence bonus: +{bonus}  Score: {score}")
    return score
