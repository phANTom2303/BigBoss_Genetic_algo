import random
import heapq

GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)

# Precomputed goal positions
GOAL_POS = {
    val: (i // 3, i % 3) for i, val in enumerate(GOAL)
}


def manhattan_distance(state):
    return sum(
        abs(i // 3 - GOAL_POS[val][0]) + abs(i % 3 - GOAL_POS[val][1])
        for i, val in enumerate(state) if val != 0
    )


def get_adjacent(zero):
    moves = []
    if zero % 3 != 0: moves.append(zero - 1)
    if zero % 3 != 2: moves.append(zero + 1)
    if zero >= 3:     moves.append(zero - 3)
    if zero <= 5:     moves.append(zero + 3)
    return moves


def solve_puzzle(start, use_astar=True):
    start = tuple(start)
    seen = set()

    if use_astar:
        heap = [(manhattan_distance(start), 0, start, [])]
    else:
        heap = [(manhattan_distance(start), start, [])]

    while heap:
        if use_astar:
            f, g, curr, moves = heapq.heappop(heap)
        else:
            h, curr, moves = heapq.heappop(heap)
            g = len(moves)

        if curr == GOAL:
            return moves

        if curr in seen:
            continue
        seen.add(curr)

        if not use_astar and g > 300:
            return moves  # In BFS if the contestant uses more than 300 moves - give up and return

        zero = curr.index(0)

        for nxt in get_adjacent(zero):
            new_state = list(curr)
            new_state[zero], new_state[nxt] = new_state[nxt], new_state[zero]
            new_tuple = tuple(new_state)

            if new_tuple in seen:
                continue

            new_moves = moves + [new_state[zero]]

            if use_astar:
                heapq.heappush(
                    heap,
                    (g + 1 + manhattan_distance(new_state), g + 1, new_tuple, new_moves)
                )
            else:
                heapq.heappush(
                    heap,
                    (manhattan_distance(new_state), new_tuple, new_moves)
                )

    return []


def generate_puzzle(shuffles=100):
    tiles = list(GOAL)
    for _ in range(shuffles):
        zero = tiles.index(0)
        swap = random.choice(get_adjacent(zero))
        tiles[zero], tiles[swap] = tiles[swap], tiles[zero]
    return tiles


#“Take a contestant, give them a random puzzle, let their mental state decide how they solve it, 
# and score them based on how efficiently they perform.”

def play_8puzzle(contestant):
    print(f"\n  8-PUZZLE TASK — Contestant: {contestant.name}")

    # Performance IQ
    performance_iq = max(0, min(100, random.gauss(contestant.intelligence, 8)))

    # Generate puzzle
    tiles = generate_puzzle()

    # Difficulty factor
    task_difficulty = random.uniform(0.8, 1.2)

    # Choose strategy
    use_astar = performance_iq > 75

    if use_astar:
        print(f"  {contestant.name} is 'In the Zone'. Using A*...")
    else:
        print(f"  {contestant.name} is under pressure. Using Best-First...")

    moves = solve_puzzle(tiles, use_astar)

    move_count = len(moves)
    print(f"  Solved in {move_count} moves.")

    # Scoring
    base = max(0, 100 - (move_count * 3 * task_difficulty))
    bonus = round(performance_iq * 0.25)
    final_score = round(min(100, base + bonus))

    print(f"  Efficiency Score: {round(base)} | Bonus: +{bonus}")
    print(f"  TOTAL ROUND SCORE: {final_score}")

    return final_score