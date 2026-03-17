# games/tic_tac_toe.py
import random

def play_tictactoe(contestant):
    print(f"\n  TIC TAC TOE — {contestant.name} vs AI")

    board = [' '] * 9

    def draw():
        print(f"    {board[0]} | {board[1]} | {board[2]}")
        print("    ---------")
        print(f"    {board[3]} | {board[4]} | {board[5]}")
        print("    ---------")
        print(f"    {board[6]} | {board[7]} | {board[8]}")

    def check_winner(b, m):
        for i,j,k in [(0,1,2),(3,4,5),(6,7,8),
                      (0,3,6),(1,4,7),(2,5,8),
                      (0,4,8),(2,4,6)]:
            if b[i]==b[j]==b[k]==m:
                return True
        return False

    def get_move(b, mark):
        opp = 'O' if mark=='X' else 'X'
        for i in range(9):           # try to win
            if b[i]==' ':
                b[i]=mark
                if check_winner(b,mark): return i
                b[i]=' '
        for i in range(9):           # block opponent
            if b[i]==' ':
                b[i]=opp
                if check_winner(b,opp):
                    b[i]=' '; return i
                b[i]=' '
        if b[4]==' ': return 4       # center
        for i in [0,2,6,8]:          # corner
            if b[i]==' ': return i
        for i in range(9):           # any empty
            if b[i]==' ': return i
        return -1

    result = "draw"

    for turn in range(9):
        if turn % 2 == 0:
            # Player X
            if contestant.intelligence >= 60:
                pos = get_move(board, 'X')    # smart move
            else:
                empty = [i for i in range(9) if board[i]==' ']
                pos   = random.choice(empty) if empty else -1  # random move
        else:
            # AI O
            pos = get_move(board, 'O')        # always smart

        if pos == -1: break
        board[pos] = 'X' if turn%2==0 else 'O'

        if check_winner(board, 'X'): result="win";  break
        if check_winner(board, 'O'): result="loss"; break

    draw()
    print(f"  Result: {result.upper()}")
    base  = {"win":100, "draw":55, "loss":15}[result]
    bonus = round(contestant.intelligence * 0.2)
    score = min(100, base + bonus)
    print(f"  Score: {score}")
    return score
