import math

# -------------------------------
# CREATE EMPTY BOARD
# -------------------------------

board = []

for i in range(9):
    board.append(" ")


# -------------------------------
# PRINT THE BOARD
# -------------------------------

def print_board():

    print("\nBoard State:\n")

    print(board[0] + " | " + board[1] + " | " + board[2])
    print("--+---+--")

    print(board[3] + " | " + board[4] + " | " + board[5])
    print("--+---+--")

    print(board[6] + " | " + board[7] + " | " + board[8])


# -------------------------------
# CHECK WINNER
# -------------------------------

def check_winner(current_board):

    win_conditions = []

    win_conditions.append([0, 1, 2])
    win_conditions.append([3, 4, 5])
    win_conditions.append([6, 7, 8])

    win_conditions.append([0, 3, 6])
    win_conditions.append([1, 4, 7])
    win_conditions.append([2, 5, 8])

    win_conditions.append([0, 4, 8])
    win_conditions.append([2, 4, 6])

    for condition in win_conditions:

        first = condition[0]
        second = condition[1]
        third = condition[2]

        if current_board[first] != " ":
            if current_board[first] == current_board[second]:
                if current_board[second] == current_board[third]:
                    return current_board[first]

    # Check for draw
    empty_found = False

    for cell in current_board:
        if cell == " ":
            empty_found = True

    if empty_found == False:
        return "Draw"

    return None


# -------------------------------
# MINIMAX ALGORITHM
# -------------------------------

def minimax(current_board, is_maximizing):

    result = check_winner(current_board)

    # Base cases
    if result == "X":
        return -1

    if result == "O":
        return 1

    if result == "Draw":
        return 0

    # -----------------------
    # O is MAXIMIZING AI
    # -----------------------
    if is_maximizing == True:

        best_score = -math.inf

        for i in range(9):

            if current_board[i] == " ":

                current_board[i] = "O"

                score = minimax(current_board, False)

                current_board[i] = " "

                if score > best_score:
                    best_score = score

        return best_score

    # -----------------------
    # X is MINIMIZING AI
    # -----------------------
    else:

        best_score = math.inf

        for i in range(9):

            if current_board[i] == " ":

                current_board[i] = "X"

                score = minimax(current_board, True)

                current_board[i] = " "

                if score < best_score:
                    best_score = score

        return best_score


# -------------------------------
# FIND BEST MOVE FOR ANY PLAYER
# -------------------------------

def find_best_move_for_player(player):

    # If player is O → maximize
    if player == "O":
        best_score = -math.inf
    else:
        best_score = math.inf

    best_move = -1

    for i in range(9):

        if board[i] == " ":

            # Try move
            board[i] = player

            # Decide next turn
            if player == "O":
                score = minimax(board, False)
            else:
                score = minimax(board, True)

            # Undo move
            board[i] = " "

            # Update best move
            if player == "O":
                if score > best_score:
                    best_score = score
                    best_move = i
            else:
                if score < best_score:
                    best_score = score
                    best_move = i

    return best_move


# -------------------------------
# AI vs AI GAME LOOP
# -------------------------------

def play_ai_vs_ai():

    print("AI vs AI Game Started!\n")

    current_player = "X"   # X starts first

    print_board()

    while True:

        print("\nCurrent Player:", current_player)

        # Get best move for current AI
        move = find_best_move_for_player(current_player)

        # Apply move
        board[move] = current_player

        print_board()

        # Check result
        result = check_winner(board)

        if result != None:
            break

        # Switch player
        if current_player == "X":
            current_player = "O"
        else:
            current_player = "X"

    # -------------------
    # FINAL RESULT
    # -------------------

    print("\nGame Over!")

    if result == "Draw":
        print("It's a draw!")
    else:
        print(result + " wins!")


# -------------------------------
# START GAME
# -------------------------------

play_ai_vs_ai()