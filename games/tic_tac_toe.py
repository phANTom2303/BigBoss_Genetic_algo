# games/tic_tac_toe.py

import random

SIZE = 5


def play_tictactoe(player1, player2):
    print(f"\n  TIC TAC TOE 5x5 — {player1.name} (X) vs {player2.name} (O)")

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

        # diagonals
        if all(b[i*SIZE + i] == mark for i in range(SIZE)):
            return True
        if all(b[i*SIZE + (SIZE-1-i)] == mark for i in range(SIZE)):
            return True

        return False

    def is_full(b):
        return all(x != ' ' for x in b)

    # ---------- DEPTH ----------
    def get_depth(intelligence):
        if intelligence >= 80: return 4
        if intelligence >= 60: return 3
        if intelligence >= 40: return 2
        return 1

    # ---------- EVALUATION ----------
    def evaluate(b):
        if check_winner(b, 'X'): return 100
        if check_winner(b, 'O'): return -100
        return 0

    # ---------- MINIMAX ----------
    def minimax(b, depth, is_max):
        score = evaluate(b)

        if abs(score) == 100 or depth == 0 or is_full(b):
            return score

        if is_max:
            best = -999
            for i in range(SIZE * SIZE):
                if b[i] == ' ':
                    b[i] = 'X'
                    val = minimax(b, depth - 1, False)
                    b[i] = ' '
                    best = max(best, val)
            return best
        else:
            best = 999
            for i in range(SIZE * SIZE):
                if b[i] == ' ':
                    b[i] = 'O'
                    val = minimax(b, depth - 1, True)
                    b[i] = ' '
                    best = min(best, val)
            return best

    # ---------- BEST MOVE ----------
    def get_best_move(b, intelligence, mark):
        depth = get_depth(intelligence)

        best_val = -999 if mark == 'X' else 999
        best_move = -1

        for i in range(SIZE * SIZE):
            if b[i] == ' ':
                b[i] = mark
                val = minimax(b, depth - 1, mark != 'X')
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
    players = [(player1, 'X'), (player2, 'O')]
    winner = None

    for turn in range(SIZE * SIZE):
        player, mark = players[turn % 2]

        # 🔥 mix intelligence + randomness
        if random.random() < 0.85:
            pos = get_best_move(board, player.intelligence, mark)
        else:
            empty = [i for i in range(SIZE * SIZE) if board[i] == ' ']
            pos = random.choice(empty) if empty else -1

        if pos == -1:
            break

        board[pos] = mark

        if check_winner(board, mark):
            winner = player
            break

    # ---------- RESULT ----------
    draw()

    if winner is None:
        print("  Result: DRAW")
        score1, score2 = 60, 60
    else:
        print(f"  Winner: {winner.name}")
        if winner == player1:
            score1, score2 = 100, 20
        else:
            score1, score2 = 20, 100

    # slight randomness
    score1 = max(0, min(100, score1 - random.randint(0, 10)))
    score2 = max(0, min(100, score2 - random.randint(0, 10)))

    print(f"  {player1.name} Score: {score1}")
    print(f"  {player2.name} Score: {score2}")

    return [(player1, score1), (player2, score2)]