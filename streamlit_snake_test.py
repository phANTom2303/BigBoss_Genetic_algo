import streamlit as st
import random
import time

# -----------------------------
# SNAKES & LADDERS DATA
# -----------------------------

SNAKES = {
    16:6, 47:26, 49:11, 56:53, 62:19,
    64:60, 87:24, 93:73, 99:78
}

LADDERS = {
    4:14, 9:31, 20:38, 28:84,
    40:59, 51:67, 63:81, 71:91
}

# -----------------------------
# DRAW BOARD (HTML UI)
# -----------------------------

def draw_board_html(pos):

    html = "<div style='display:inline-block;background:#f9f9f9;padding:10px;border-radius:10px;'>"

    for i in range(100, 0, -10):
        html += "<div style='display:flex;'>"

        for j in range(10):
            num = i - j

            bg = "#ffffff"
            color = "#000000"

            # Player
            if num == pos:
                bg = "#2196F3"
                color = "white"

            # Snake
            elif num in SNAKES:
                bg = "#ff4d4d"
                color = "white"

            # Ladder
            elif num in LADDERS:
                bg = "#4CAF50"
                color = "white"

            html += f"<div style='width:45px;height:45px;margin:2px;border-radius:6px;border:1px solid ; display:flex;align-items:center;justify-content:center;background:{bg};color:{color};font-weight:bold;font-size:14px;'>{num}</div>"

        html += "</div>"

    html += "</div>"

    return html

# -----------------------------
# GAME LOGIC
# -----------------------------

def play_snake_ladder():

    pos = 0
    turns = 0
    max_turns = 30

    board_area = st.empty()
    log_area = st.empty()
    progress = st.progress(0)

    while pos < 100 and turns < max_turns:

        dice = random.randint(1, 6)

        log_area.info(f"🎲 Turn {turns+1}: Dice = {dice}")
        time.sleep(0.6)

        new = pos + dice

        if new > 100:
            log_area.warning("⚠️ Out of bounds!")
        elif new in SNAKES:
            log_area.error(f"🐍 Snake! {new} ↓ {SNAKES[new]}")
            pos = SNAKES[new]
        elif new in LADDERS:
            log_area.success(f"🪜 Ladder! {new} ↑ {LADDERS[new]}")
            pos = LADDERS[new]
        else:
            pos = new
            log_area.write(f"📍 Position: {pos}")

        # ✅ FIXED RENDERING
        board_area.markdown(
            draw_board_html(pos),
            unsafe_allow_html=True
        )

        progress.progress(pos / 100)

        time.sleep(1)

        turns += 1

        if pos >= 100:
            log_area.success(f"🏆 Reached 100 in {turns} turns!")
            break

    # -----------------------------
    # SCORE CALCULATION
    # -----------------------------

    base = round((pos / 100) * 80) + max(0, max_turns - turns)

    adaptability = 70
    bonus = round(adaptability * 0.25)

    score = min(100, base + bonus)

    st.success(f"🎯 Final Position: {pos}")
    st.success(f"🏆 Score: {score}")

    st.write(f"🕒 Turns taken: {turns}")

    if pos >= 100:
        st.success("🏁 Game ended: Reached 100")
    else:
        st.warning("⏳ Game ended: Max turns reached")

# -----------------------------
# MAIN UI
# -----------------------------

st.set_page_config(page_title="Snake Ladder", layout="wide")

st.title("🎮 Snake & Ladder Visual Game")

# Legend
st.markdown("""
🔵 Player  
🔴 Snake  
🟢 Ladder  
⚪ Normal  
""")

# Initial Board
st.subheader("📋 Board Preview")
st.markdown(draw_board_html(0), unsafe_allow_html=True)

# Play Button
if st.button("▶ Play Game"):
    play_snake_ladder()