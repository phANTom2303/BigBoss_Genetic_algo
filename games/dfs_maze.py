# games/dfs_maze.py
# DFS explores path automatically
# Main attribute: adaptability

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

def play_dfs(contestant):
    print(f"\n  DFS MAZE — {contestant.name}")
    print(f"  Start:{START} → End:{END}")
    print("  DFS exploring path...\n")

    stack    = [(START, [START])]
    visited  = set()
    explored = 0
    path     = None

    while stack:
        (r,c), curr_path = stack.pop()
        if (r,c) in visited: continue
        visited.add((r,c))
        explored += 1

        if (r,c) == END:
            path = curr_path
            break

        for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr,nc = r+dr, c+dc
            if 0<=nr<ROWS and 0<=nc<COLS and MAZE[nr][nc]==1 and (nr,nc) not in visited:
                stack.append(((nr,nc), curr_path+[(nr,nc)]))

    if path:
        print(f"  Path found! Length:{len(path)} steps  Explored:{explored} nodes")
        for r in range(ROWS):
            row = "  "
            for c in range(COLS):
                if   (r,c)==START:      row+="[S]"
                elif (r,c)==END:        row+="[E]"
                elif (r,c) in path:     row+="[P]"
                elif MAZE[r][c]==0:     row+="[#]"
                else:                   row+="[.]"
            print(row)
        base = max(20, 100 - explored//3)
    else:
        print("  No path found!")
        base = 10

    bonus = round(contestant.adaptability * 0.3)
    score = min(100, base + bonus)
    print(f"  Base:{base}  Adaptability bonus:+{bonus}  Score:{score}")
    return score
