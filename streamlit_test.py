# streamlit_visual_test.py

import streamlit as st
import time
import random

st.set_page_config(page_title="Game Visual Test", layout="wide")

st.title("🎮 Game Visualization Test (Live)")

# -----------------------------
# GAME SELECTOR
# -----------------------------

game_choice = st.sidebar.selectbox(
    "Choose Game",
    ["Snake & Ladder", "8 Puzzle", "Maze BFS", "Tic Tac Toe"]
)

# -----------------------------
# 🐍 SNAKE & LADDER
# -----------------------------

def draw_snake_board(pos):
    board = ""
    for i in range(100, 0, -10):
        row = []
        for j in range(10):
            num = i - j
            if num == pos:
                row.append(f"🧍{num}")
            else:
                row.append(f"{num:2}")
        board += " | ".join(row) + "\n\n"
    return board

def play_snake():
    pos = 0
    board = st.empty()
    log = st.empty()

    for _ in range(15):
        dice = random.randint(1, 6)

        log.write(f"🎲 Dice: {dice}")

        pos += dice
        if pos > 100:
            pos -= dice

        board.text(draw_snake_board(pos))

        time.sleep(1)

        if pos >= 100:
            log.success("🏆 Reached 100!")
            break

# -----------------------------
# 🧩 8 PUZZLE
# -----------------------------

def draw_puzzle(tiles):
    text = ""
    for i in range(0, 9, 3):
        row = ""
        for v in tiles[i:i+3]:
            row += f"[{v if v!=0 else ' '}]"
        text += row + "\n"
    return text

def play_puzzle():
    tiles = [1,2,3,4,5,6,7,8,0]
    random.shuffle(tiles)

    board = st.empty()

    for _ in range(10):
        zero = tiles.index(0)
        swap = random.choice([i for i in range(9) if i != zero])
        tiles[zero], tiles[swap] = tiles[swap], tiles[zero]

        board.text(draw_puzzle(tiles))
        time.sleep(0.8)

# -----------------------------
# 🧱 MAZE BFS (SIMPLIFIED)
# -----------------------------

maze = [
    [1,1,0,1],
    [0,1,1,1],
    [0,0,1,0],
    [1,1,1,1]
]

def draw_maze(path):
    text = ""
    for r in range(4):
        row = ""
        for c in range(4):
            if (r,c) in path:
                row += "🟩"
            elif maze[r][c] == 0:
                row += "⬛"
            else:
                row += "⬜"
        text += row + "\n"
    return text

def play_maze():
    path = []
    board = st.empty()

    for step in [(0,0),(0,1),(1,1),(1,2),(2,2),(3,2),(3,3)]:
        path.append(step)
        board.text(draw_maze(path))
        time.sleep(0.7)

# -----------------------------
# ❌⭕ TIC TAC TOE
# -----------------------------

def draw_ttt(board):
    return f"""
 {board[0]} | {board[1]} | {board[2]}
---------
 {board[3]} | {board[4]} | {board[5]}
---------
 {board[6]} | {board[7]} | {board[8]}
"""

def play_ttt():
    board = [' '] * 9
    placeholder = st.empty()

    for turn in range(9):
        pos = random.choice([i for i in range(9) if board[i]==' '])
        board[pos] = 'X' if turn % 2 == 0 else 'O'

        placeholder.text(draw_ttt(board))
        time.sleep(0.8)

# -----------------------------
# RUN BUTTON
# -----------------------------

if st.button("▶ Run Visualization"):

    if game_choice == "Snake & Ladder":
        play_snake()

    elif game_choice == "8 Puzzle":
        play_puzzle()

    elif game_choice == "Maze BFS":
        play_maze()

    elif game_choice == "Tic Tac Toe":
        play_ttt()