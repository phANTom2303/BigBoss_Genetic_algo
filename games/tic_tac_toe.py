# games/tic_tac_toe.py

import random

SIZE = 5


def play_tictactoe(contestant):
    print(f"\n  TIC TAC TOE 5x5 — {contestant.name} vs AI")

    board = [' '] * (SIZE * SIZE)

    # ---------- DRAW ----------
    def draw():
        print()
        for r in range(SIZE):
            row = board[r*SIZE:(r+1)*SIZE]
            print("    " + " | ".join(row))
            if r < SIZE - 1:
                print("    " + "-" * (SIZE * 4 - 3))
        print()

    # ---------- WIN CHECK ----------
    def check_winner(b, mark):
        # rows
        for r in range(SIZE):
            if all(b[r*SIZE + c] == mark for c in range(SIZE)):
                return True

        # cols
        for c in range(SIZE):
            if all(b[r*SIZE + c] == mark for r in range(SIZE)):
                return True

        # diagonal \
        if all(b[i*SIZE + i] == mark for i in range(SIZE)):
            return True

        # diagonal /
        if all(b[i*SIZE + (SIZE-1-i)] == mark for i in range(SIZE)):
            return True

        return False

    def is_full(b):
        return all(x != ' ' for x in b)

    # ---------- INTELLIGENCE → DEPTH ----------
    def get_depth(intelligence):
        if intelligence >= 80: return 4
        if intelligence >= 60: return 3
        if intelligence >= 40: return 2
        return 1

    # ---------- EVALUATION ----------
    def evaluate(b):
        if check_winner(b, 'X'):
            return 100
        if check_winner(b, 'O'):
            return -100
        return 0

    # ---------- MINIMAX ----------
    def minimax(b, depth, is_max, alpha, beta):
        score = evaluate(b)

        if abs(score) == 100 or depth == 0 or is_full(b):
            return score

        if is_max:
            best = -float('inf')
            for i in range(SIZE * SIZE):
                if b[i] == ' ':
                    b[i] = 'X'
                    val = minimax(b, depth - 1, False, alpha, beta)
                    b[i] = ' '
                    best = max(best, val)
                    alpha = max(alpha, best)
                    if beta <= alpha:
                        break
            return best
        else:
            best = float('inf')
            for i in range(SIZE * SIZE):
                if b[i] == ' ':
                    b[i] = 'O'
                    val = minimax(b, depth - 1, True, alpha, beta)
                    b[i] = ' '
                    best = min(best, val)
                    beta = min(beta, best)
                    if beta <= alpha:
                        break
            return best

    # ---------- BEST MOVE ----------
    def get_best_move(b, intelligence, mark):
        depth = get_depth(intelligence)

        best_val = -float('inf') if mark == 'X' else float('inf')
        best_move = -1

        for i in range(SIZE * SIZE):
            if b[i] == ' ':
                b[i] = mark
                val = minimax(b, depth - 1, mark != 'X', -float('inf'), float('inf'))
                b[i] = ' '

                if mark == 'X':
                    if val > best_val:
                        best_val = val
                        best_move = i
                else:
                    if val < best_val:
                        best_val = val
                        best_move = i

        return best_move

    # ---------- GAME LOOP ----------
    result = "draw"

    for turn in range(SIZE * SIZE):

        if turn % 2 == 0:
            # 🎯 Contestant
            if random.random() < 0.85:
                pos = get_best_move(board, contestant.intelligence, 'X')
            else:
                empty = [i for i in range(SIZE * SIZE) if board[i] == ' ']
                pos = random.choice(empty) if empty else -1

        else:
            # 🤖 AI (medium level)
            if random.random() < 0.9:
                pos = get_best_move(board, 65, 'O')
            else:
                empty = [i for i in range(SIZE * SIZE) if board[i] == ' ']
                pos = random.choice(empty) if empty else -1

        if pos == -1:
            break

        board[pos] = 'X' if turn % 2 == 0 else 'O'

        if check_winner(board, 'X'):
            result = "win"
            break

        if check_winner(board, 'O'):
            result = "loss"
            break

    # ---------- RESULT ----------
    draw()
    print(f"  Result: {result.upper()}")

    base = {"win": 100, "draw": 60, "loss": 20}[result]
    score = max(0, min(100, base - random.randint(0, 15)))

    print(f"  Score: {score}")
    return score