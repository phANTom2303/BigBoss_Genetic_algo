import streamlit as st
import time
import random
from games.puzzle_8 import play_8puzzle, manhattan_distance

GOAL = [1,2,3,4,5,6,7,8,0]

# 🎨 Draw puzzle grid
def draw_puzzle(tiles):
    html = "<div style='display:inline-block;'>"

    for i in range(0, 9, 3):
        html += "<div style='display:flex;'>"

        for v in tiles[i:i+3]:
            bg = "#ffffff"
            color = "#000"

            if v == 0:
                bg = "#222"
                color = "#fff"

            html += f"<div style=\"width:25px;height:25px;margin:2px;border-radius:6px;border:1px solid #ccc;display:flex;align-items:center;justify-content:center;background:{bg};color:{color};font-size:15px;font-weight:bold;\">{v if v != 0 else ""}</div>"

        html += "</div>"

    html += "</div>"
    return html


def run(player):

    st.subheader(f"🧩 8 Puzzle — {player.name}")

    board_area = st.empty()
    log_area = st.empty()

    # 🔀 Generate solvable shuffle
    tiles = [1,2,3,4,5,6,7,8,0]
    for _ in range(20):
        zero = tiles.index(0)
        possible = []
        if zero % 3 != 0: possible.append(zero-1)
        if zero % 3 != 2: possible.append(zero+1)
        if zero >= 3: possible.append(zero-3)
        if zero <= 5: possible.append(zero+3)

        swap = random.choice(possible)
        tiles[zero], tiles[swap] = tiles[swap], tiles[zero]

    # 🖥 Initial display
    board_area.markdown(draw_puzzle(tiles), unsafe_allow_html=True)
    log_area.info(f"Initial Manhattan Distance: {manhattan_distance(tiles)}")

    time.sleep(1)

    # ✅ USE STRUCTURED SOLVER
    result = play_8puzzle(player)

    moves = result["moves"]
    steps = result["steps"]
    score = result["score"]

    # 🎬 Animate solution
    for move in moves:
        zero = tiles.index(0)
        ti = tiles.index(move)

        tiles[zero], tiles[ti] = tiles[ti], tiles[zero]

        board_area.markdown(draw_puzzle(tiles), unsafe_allow_html=True)
        time.sleep(0.2)

    st.success(f"✅ Solved in {steps} moves")
    st.success(f"🏆 Score: {score}")

    return {
    "score": score,
    "moves": moves
}  # ✅ ONLY SCORE