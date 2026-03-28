# games/bfs_maze.py

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
START = (0, 0)
END   = (5, 5)

def play_bfs(contestant):

    queue    = deque([(START, [START])])
    visited  = {START}
    explored = []
    path     = None

    while queue:
        (r,c), curr_path = queue.popleft()
        explored.append((r, c))

        if (r,c) == END:
            path = curr_path
            break

        for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr,nc = r+dr, c+dc
            if 0<=nr<ROWS and 0<=nc<COLS and MAZE[nr][nc]==1 and (nr,nc) not in visited:
                visited.add((nr,nc))
                queue.append(((nr,nc), curr_path+[(nr,nc)]))

    if path:
        base = max(20, 100 - len(path)*5 -len( explored)//3)
    else:
        base = 10
        path = []

    bonus = round(contestant.intelligence * 0.3)
    score = min(100, base + bonus)

    return {
    "score": score,
    "path": path if path else [],
    "explored": explored,
    "strategy": "BFS"
}