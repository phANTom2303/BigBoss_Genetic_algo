    # streamlit_app.py

import streamlit as st
import pandas as pd
import random
import time

from main import make_team
from games import ALL_GAMES
from core.game_engine import play_round

# -------------------------
# INIT SESSION
# -------------------------

if "players" not in st.session_state:
    st.session_state.players = make_team()

if "round" not in st.session_state:
    st.session_state.round = 0

if "history" not in st.session_state:
    st.session_state.history = []

players = st.session_state.players

# -------------------------
# UI HEADER
# -------------------------

st.set_page_config(layout="wide")
st.title("🎮 Big Boss Genetic AI Dashboard")

# -------------------------
# SIDEBAR
# -------------------------

st.sidebar.header("Controls")

if st.sidebar.button("🔄 Restart Game"):
    st.session_state.players = make_team()
    st.session_state.round = 0
    st.session_state.history = []
    st.rerun()

# -------------------------
# METRICS
# -------------------------

alive = [p for p in players if p.alive]

col1, col2, col3 = st.columns(3)

col1.metric("👥 Players Alive", len(alive))
col2.metric("🔁 Round", st.session_state.round)

if alive:
    top_player = max(alive, key=lambda p: p.popularity)
    col3.metric("🏆 Top Player", top_player.name)

# -------------------------
# LEADERBOARD
# -------------------------

st.subheader("🏆 Leaderboard")

df = pd.DataFrame({
    "Name": [p.name for p in players],
    "Popularity": [p.popularity for p in players],
    "Alive": ["✅" if p.alive else "❌" for p in players]
})

df = df.sort_values(by="Popularity", ascending=False)

st.dataframe(df, use_container_width=True)

# -------------------------
# TOP PLAYERS
# -------------------------

st.subheader("🔥 Top 5 Players")

top5 = df.head(5)

for i, row in top5.iterrows():
    st.write(f"{row['Name']} — Pop: {row['Popularity']}")

# -------------------------
# ELIMINATED PLAYERS
# -------------------------

st.subheader("❌ Eliminated Players")

eliminated = [p.name for p in players if not p.alive]

if eliminated:
    st.write(", ".join(eliminated))
else:
    st.write("None yet")

# -------------------------
# GAME PLAY SECTION
# -------------------------

st.subheader("🎮 Play Round")

if st.button("▶ Run Next Round"):

    st.session_state.round += 1

    game = random.choice(ALL_GAMES)

    st.info(f"🎯 Game: {game['name']} ({game['main_attr']})")

    log_box = st.empty()

    alive_players = [p for p in players if p.alive]

    # LIVE PLAYER TURNS
    for p in alive_players:
        log_box.write(f"🎮 {p.name} is playing...")

        score = game["fn"](p)
        p.game_score = score

        log_box.write(f"✅ {p.name} scored {score}")

        time.sleep(0.5)

    # Update popularity
    for p in alive_players:
        p.calculate_popularity()

    # ELIMINATION
    from core.genetic_algorithm import select_top, mutate

    survivors = select_top(players)

    st.warning("⚠️ Elimination happened!")

    # MUTATION
    mutate(survivors)

    st.success("🧬 Evolution applied!")

    st.rerun()

# -------------------------
# POPULARITY GRAPH
# -------------------------

st.subheader("📊 Popularity Distribution")

pop_values = [p.popularity for p in players]

st.bar_chart(pop_values)