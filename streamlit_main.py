import streamlit as st
import time
from main import get_initial_players
from games import ALL_GAMES
from core.genetic_algorithm import add_wildcard, select_top, mutate
from streamlit_games.game_router import run_game_visual

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Bigg Boss AI", layout="wide")


# -----------------------------
# 🔥 CLEAN + FIXED CSS
# -----------------------------
st.markdown("""
<style>

/* 🚫 HARD LOCK — NO SCROLL ANYWHERE */
html, body, [data-testid="stAppViewContainer"] {
    height: 100vh;
    overflow: hidden !important;
}

/* 🎯 MAIN APP FIT */
.block-container {
    height: 100vh;
    padding: 0.3rem 0.6rem !important;
    display: flex;
    flex-direction: column;
}

/* 🧠 REMOVE ALL DEFAULT GAPS */
[data-testid="stVerticalBlock"] {
    gap: 4px !important;
}

/* 🧱 MAIN ROW (LEFT + RIGHT) */
[data-testid="stHorizontalBlock"] {
    flex-grow: 1;
    height: 100%;
    align-items: stretch;
}

/* ---------------- LEFT PANEL ---------------- */
[data-testid="column"]:first-child {
    height: 100%;
    overflow: hidden;
}

/* PLAYERS LIST FIT */
.left-panel-scroll {
    height: 100%;
    overflow: hidden;  /* 🚫 NO SCROLL */
    font-size: 10px;
    line-height: 1.0;
}

/* ---------------- RIGHT PANEL ---------------- */
[data-testid="column"]:nth-child(2) {
    height: 100%;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

/* 🎮 GAME AREA AUTO FIT */
.game-container-fixed {
    flex-grow: 1;
    overflow: hidden;
    padding: 6px;
    border: 1px solid #333;
    border-radius: 6px;
    background: rgba(255,255,255,0.02);
}

/* ---------------- GLOBAL SHRINK ---------------- */

/* TITLE */
h1 {
    font-size: 16px !important;
    margin: 0 !important;
}

/* HEADERS */
h2, h3, h4 {
    font-size: 16px !important;
    margin: 1px 0 !important;
}

/* TEXT */
p, div {
    font-size: 14px !important;
    margin: 0 !important;
}

/* BUTTONS */
.stButton button {
    padding: 2px 6px !important;
    font-size: 18px !important;
}

/* PROGRESS BAR */
.stProgress {
    margin: 2px 0 !important;
}
.stProgress > div > div {
    height: 3px !important;
}

/* ALERT BOXES (BLUE/GREEN) */
.stAlert {
    padding: 1px 3px !important;
    font-size: 14px !important;
    margin: 1px 0 !important;
}

/* REMOVE EXTRA SPACE */
.stMarkdown {
    margin: 0 !important;
}

/* 🔥 SCALE GAME VISUAL (MOST IMPORTANT) */
.game-container-fixed > div {
    transform: scale(0.65);
    transform-origin: top left;
    width: 150%;
}

/* 🔴 ELIMINATED */
.eliminated-player {
    font-size: 10px;
    opacity: 0.6;
}

/* 🚀 FORCE EVERYTHING INSIDE VIEWPORT */
[data-testid="stAppViewContainer"] > div {
    max-height: 100vh;
    overflow: hidden;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# SESSION STATE
# -----------------------------
if "players" not in st.session_state:
    st.session_state.players = []
if "round" not in st.session_state:
    st.session_state.round = 0
if "started" not in st.session_state:
    st.session_state.started = False
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "round_running" not in st.session_state:
    st.session_state.round_running = False
if "current_game" not in st.session_state:
    st.session_state.current_game = None

# -----------------------------
# START BUTTON
# -----------------------------
st.markdown("<h2 style='font-size:22px;margin-bottom:4px;'>🎮 Bigg Boss Game</h2>", unsafe_allow_html=True)
if not st.session_state.started:
    if st.button("🚀 Start Game", use_container_width=True):
        st.session_state.players = get_initial_players()
        st.session_state.started = True
        st.session_state.round = 1
        st.rerun()

# -----------------------------
# MAIN UI
# -----------------------------

if st.session_state.started:

    players = st.session_state.players
    
    left, right = st.columns([1, 3])

    # -----------------------------
    # LEFT → PLAYERS (FULL LIST)
    # -----------------------------
    
    with left:
        # --- ADDED BIGG BOSS TITLE HERE ---
        st.markdown("<h2 style='font-size:32px !important; color: #28a745; margin-bottom: 2px;'>👁️ Bigg Boss</h2>", unsafe_allow_html=True)
        st.markdown("### 🧑 Players")

        alive = sorted(
            [p for p in players if p.alive],
            key=lambda x: x.popularity,
            reverse=True
        )

        dead = [p for p in players if not p.alive]

        # 🔥 SHOW ALL PLAYERS (NO CUT)
        col1, col2 = st.columns(2)

        mid = (len(alive) + 1) // 2  # split into 10 + 10

        left_players = alive[:mid]
        right_players = alive[mid:]

        # LEFT SIDE (1–10)
        with col1:
            for i, p in enumerate(left_players, 1):
                tag = "🌟" if getattr(p, "is_wildcard", False) else ""
                st.write(f"{i}. {tag}{p.name} ({p.popularity})")

        # RIGHT SIDE (11–20)
        with col2:
            for i, p in enumerate(right_players, mid + 1):
                tag = "🌟" if getattr(p, "is_wildcard", False) else ""
                st.write(f"{i}. {tag}{p.name} ({p.popularity})")

        if dead:
            st.markdown("<hr style='margin: 5px 0;'>", unsafe_allow_html=True)
            st.markdown("<p style='font-size:12px; opacity:0.8;'>❌ Eliminated</p>", unsafe_allow_html=True)
            
            d_col1, d_col2 = st.columns(2)
            mid_dead = (len(dead) + 1) // 2
            
            with d_col1:
                for p in dead[:mid_dead]:
                    st.markdown(f"<span style='color: #ff4b4b; text-decoration: line-through; font-size: 12px;'>{p.name}</span>", unsafe_allow_html=True)

            with d_col2:
                for p in dead[mid_dead:]:
                    st.markdown(f"<span style='color: #ff4b4b; text-decoration: line-through; font-size: 12px;'>{p.name}</span>", unsafe_allow_html=True)

    # -----------------------------
    # RIGHT → GAME
    # -----------------------------
    with right:

        game_name = (
            st.session_state.current_game["name"]
            if st.session_state.current_game else "Next Game"
        )

        st.markdown(f"### 🔁 Round {st.session_state.round}")
        st.info(f"Game: {game_name}")

        c1, c2, c3 = st.columns(3)

        with c1:
            if st.button("▶ Start"):
                st.session_state.round_running = True
                st.session_state.current_index = 0
                st.session_state.current_game = ALL_GAMES[
                    (st.session_state.round - 1) % len(ALL_GAMES)
                ]
                st.rerun()

        with c2:
            if st.button("✨ Wildcard"):
                add_wildcard(players)
                st.rerun()

        with c3:
            if st.button("⛔ Reset"):
                st.session_state.started = False
                st.rerun()

        # -----------------------------
        # GAME EXECUTION
        # -----------------------------
        if st.session_state.round_running:

            alive_list = [p for p in players if p.alive]

            if st.session_state.current_index < len(alive_list):

                player = alive_list[st.session_state.current_index]

                st.markdown(f"### 🎭 {player.name}")
                st.progress(min(player.popularity / 100, 1.0))

                # 🔥 SCALED GAME
                st.markdown("<div class='game-box'>", unsafe_allow_html=True)

                result = run_game_visual(
                    st.session_state.current_game, player
                )

                st.markdown("</div>", unsafe_allow_html=True)

                score = result.get("score", 0) if isinstance(result, dict) else (result or 0)

                player.game_score = score
                player.calculate_popularity()

                time.sleep(0.2)

                st.session_state.current_index += 1
                st.rerun()

            else:
                st.success("🏁 Round Complete")

                survivors = select_top(players)
                mutate(survivors)

                if st.button("⏭ Next"):
                    st.session_state.round += 1
                    st.session_state.round_running = False
                    st.rerun()

        else:
            st.write("Ready")