# games/bfs_maze.py
# BFS finds shortest path automatically
# Main attribute: intelligence

from collections import deque

MAZE = [
    [1,1,0,1,1,1],
    [0,1,0,1,0,1],
    [0,1,1,1,0,1],
    [0,0,0,1,1,1],
    [1,1,1,0,0,1],
    [1,0,1,1,1,1],
]
ROWS, COLS = 6, 6

# Fixed start and end — no user input needed
START = (0, 0)
END   = (5, 5)

def play_bfs(contestant):
    print(f"\n  BFS MAZE — {contestant.name}")
    print(f"  Start:{START} → End:{END}")
    print("  BFS finding shortest path...\n")

    queue    = deque([(START, [START])])
    visited  = {START}
    explored = 0
    path     = None

    while queue:
        (r,c), curr_path = queue.popleft()
        explored += 1

        if (r,c) == END:
            path = curr_path
            break

        for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr,nc = r+dr, c+dc
            if 0<=nr<ROWS and 0<=nc<COLS and MAZE[nr][nc]==1 and (nr,nc) not in visited:
                visited.add((nr,nc))
                queue.append(((nr,nc), curr_path+[(nr,nc)]))

    if path:
        print(f"  Path found! Length:{len(path)} steps  Explored:{explored} nodes")
        # Show maze with path
        for r in range(ROWS):
            row = "  "
            for c in range(COLS):
                if   (r,c)==START:      row+="[S]"
                elif (r,c)==END:        row+="[E]"
                elif (r,c) in path:     row+="[P]"
                elif MAZE[r][c]==0:     row+="[#]"
                else:                   row+="[.]"
            print(row)
        base = max(20, 100 - len(path)*5 - explored//3)
    else:
        print("  No path found!")
        base = 10

    bonus = round(contestant.intelligence * 0.3)
    score = min(100, base + bonus)
    print(f"  Base:{base}  Intelligence bonus:+{bonus}  Score:{score}")
    return score