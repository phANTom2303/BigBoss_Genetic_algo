import random
from collections import deque

MAZE = [
    [1, 1, 0, 1, 1, 1],
    [0, 1, 0, 1, 0, 1],
    [0, 1, 1, 1, 0, 1],
    [0, 0, 0, 1, 1, 1],
    [1, 1, 1, 0, 0, 1],
    [1, 0, 1, 1, 1, 1],
]

ROWS, COLS = 6, 6
START, END = (0, 0), (5, 5)


"""
1. Generate a random focus score → represents current mental state
2. Choose strategy:
   - High focus → BFS (calm, systematic)
   - Low focus → DFS (panic, impulsive)
3. Limit exploration using stamina (based on intelligence + adaptability)
4. Explore maze using chosen strategy
5. Randomize movement order to mimic human intuition
6. If exit found → success, else → failure
7. Score based on efficiency (steps) or effort (nodes explored)
"""

def play_maze(contestant):
    print(f"\n  --- MAZE CHALLENGE: {contestant.name} ---")

    # Mental state
    focus = random.gauss(contestant.intelligence, 10)

    # Strategy decision
    use_bfs = focus > 70

    if use_bfs:
        print(f"  {contestant.name} is staying calm. Using Methodical Mapping (BFS)...")
    else:
        print(f"  {contestant.name} is panicking! Rushing through corridors (DFS)...")

    # Stamina
    stamina = 15 + contestant.intelligence // 4 + contestant.adaptability // 5

    # Solve maze
    path, explored = maze_engine(use_bfs, stamina)

    # Scoring
    if path:
        steps = len(path)
        print(f"  SUCCESS! Exit found in {steps} steps.")
        base = 100 - steps * 2
        score = max(40, base + contestant.intelligence // 5)
    else:
        print(f"  FAILURE! {contestant.name} collapsed after exploring {explored} areas.")
        score = 10 + explored // 2 #reward the effort

    print(f"  FINAL SCORE: {round(score)}")
    return round(score), path, use_bfs


def maze_engine(use_bfs, stamina):
    container = deque([(START, [START])])
    visited = {START}
    explored = 0

    while container and explored < stamina:

        if use_bfs:
            curr, path = container.popleft()
        else:
            curr, path = container.pop()

        # Goal check
        if curr == END:
            return path, explored

        explored += 1
        r, c = curr

        # Explore neighbors
        neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        random.shuffle(neighbors)

        for dr, dc in neighbors:
            nr, nc = r + dr, c + dc

            if (
                0 <= nr < ROWS and
                0 <= nc < COLS and
                MAZE[nr][nc] == 1 and
                (nr, nc) not in visited
            ):
                visited.add((nr, nc))
                container.append(((nr, nc), path + [(nr, nc)]))

    return None, explored