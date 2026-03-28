# games/dfs_maze.py

MAZE = [
    [1,1,0,1,1,1],
    [0,1,0,1,0,1],
    [0,1,1,1,0,1],
    [0,0,0,1,1,1],
    [1,1,1,0,0,1],
    [1,0,1,1,1,1],
]

ROWS, COLS = 6, 6
START = (0, 0)
END   = (5, 5)

def play_dfs(contestant):

    stack    = [(START, [START])]
    visited  = set()
    explored = []
    path     = None

    while stack:
        (r,c), curr_path = stack.pop()

        if (r,c) in visited:
            continue

        visited.add((r,c))
        explored.append((r, c))

        if (r,c) == END:
            path = curr_path
            break

        for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr,nc = r+dr, c+dc
            if 0<=nr<ROWS and 0<=nc<COLS and MAZE[nr][nc]==1 and (nr,nc) not in visited:
                stack.append(((nr,nc), curr_path+[(nr,nc)]))

    if path:
        base = max(20, 100 -len(explored)//3)
    else:
        base = 10
        path = []

    bonus = round(contestant.adaptability * 0.3)
    score = min(100, base + bonus)

    return {
    "score": score,
    "path": path if path else [],
    "explored": explored,
    "strategy": "dfs"
}