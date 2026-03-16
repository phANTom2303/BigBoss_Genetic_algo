
# games/tic_tac_toe.py
# Player vs AI — AI uses Minimax algorithm
# Main attribute: intelligence

def play_tictactoe(contestant):
    print(f"\n  {'='*50}")
    print(f"  TIC TAC TOE  —  {contestant.name} vs AI")
    print(f"  {'='*50}")
    print("  Tum = X,  AI = O")
    print("  Positions:\n")
    print("    1 | 2 | 3")
    print("    ---------")
    print("    4 | 5 | 6")
    print("    ---------")
    print("    7 | 8 | 9\n")

    board = [' '] * 9

    def draw():
        print(f"\n    {board[0]} | {board[1]} | {board[2]}")
        print("    ---------")
        print(f"    {board[3]} | {board[4]} | {board[5]}")
        print("    ---------")
        print(f"    {board[6]} | {board[7]} | {board[8]}\n")

    def winner(b, m):
        combos = [(0,1,2),(3,4,5),(6,7,8),
                  (0,3,6),(1,4,7),(2,5,8),
                  (0,4,8),(2,4,6)]
        return any(b[i]==b[j]==b[k]==m for i,j,k in combos)

    def minimax(b, is_max):
        if winner(b, 'O'): return  1
        if winner(b, 'X'): return -1
        if ' ' not in b:   return  0
        scores = []
        for i in range(9):
            if b[i] == ' ':
                b[i] = 'O' if is_max else 'X'
                scores.append(minimax(b, not is_max))
                b[i] = ' '
        return max(scores) if is_max else min(scores)

    def ai_best_move(b):
        best_score, best_pos = -99, 0
        for i in range(9):
            if b[i] == ' ':
                b[i] = 'O'
                s    = minimax(b, False)
                b[i] = ' '
                if s > best_score:
                    best_score, best_pos = s, i
        return best_pos

    result = "draw"
    for turn in range(9):
        draw()
        if turn % 2 == 0:
            # Player turn
            while True:
                try:
                    pos = int(input("  Choose position (1-9): ")) - 1
                    if 0 <= pos <= 8 and board[pos] == ' ':
                        board[pos] = 'X'
                        break
                    print("  Invalid! Choose an empty spot.")
                except ValueError:
                    print("  Enter only numbers!")
            if winner(board, 'X'):
                draw()
                print("  Tum jeet gaye!")
                result = "win"
                break
        else:
            # AI turn
            print("  AI soch raha hai...")
            board[ai_best_move(board)] = 'O'
            print("  AI ne move kiya!")
            if winner(board, 'O'):
                draw()
                print("  AI jeet gaya!")
                result = "loss"
                break

    if result == "draw":
        draw()
        print("  Draw!")

    base  = {"win": 100, "draw": 55, "loss": 15}[result]
    bonus = round(contestant.intelligence * 0.2)
    score = min(100, base + bonus)
    print(f"  Result:{result.upper()}  Base:{base}  Intelligence bonus:+{bonus}  Score:{score}")
    return score
