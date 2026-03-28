import streamlit as st
import random
from contestant import Contestant
from core.genetic_algorithm import select_top, mutate

# -----------------------------
# CREATE RANDOM WILDCARD
# -----------------------------

def create_random_wildcard():

    name = f"Wildcard{random.randint(100,999)}"

    player = Contestant(
        name,
        random.randint(50,90),
        random.randint(50,90),
        random.randint(50,90),
        random.randint(50,90)
    )

    player.calculate_popularity()
    player.is_wildcard = True

    return player


# -----------------------------
# RUN ONE ROUND (STREAMLIT)
# -----------------------------

def run_round_streamlit(contestants, game_data, round_num):

    st.subheader(f"🔁 Round {round_num}")
    st.info(f"🎯 Game: {game_data['name']}")

    active_players = [p for p in contestants if p.alive]

    scores = []

    # -----------------------------
    # PLAY GAME FOR EACH PLAYER
    # -----------------------------

    for player in active_players:

        st.markdown(f"### 🎮 {player.name}")

        game_fn = game_data["fn"]

        # ⚠️ Later we will plug snake UI here
        score = game_fn(player)

        player.game_score = score
        player.calculate_popularity()

        scores.append((player.name, score, player.popularity))

    # -----------------------------
    # SHOW ROUND RESULTS
    # -----------------------------

    st.subheader("📊 Round Results")

    for name, score, pop in sorted(scores, key=lambda x: x[1], reverse=True):
        st.write(f"{name} | Score: {score} | Pop: {pop}")

    # -----------------------------
    # ELIMINATION
    # -----------------------------

    st.subheader("❌ Elimination")

    survivors = select_top(contestants)

    for p in contestants:
        if not p.alive:
            st.error(f"{p.name} eliminated")

    # -----------------------------
    # EVOLUTION
    # -----------------------------

    st.subheader("🧬 Evolution")
    mutate(survivors)

    # -----------------------------
    # ⭐ WILDCARD SYSTEM (FIXED)
    # -----------------------------

    if "wildcard_used" not in st.session_state:
        st.session_state.wildcard_used = False

    if not st.session_state.wildcard_used and 2 <= round_num <= 4:

        st.warning("⭐ Wildcard Entry Available!")

        if st.button("➕ Add Wildcard Player"):

            new_player = create_random_wildcard()
            contestants.append(new_player)

            st.success(f"🔥 Wildcard Added: {new_player.name}")

            st.session_state.wildcard_used = True

    # -----------------------------
    # CHECK WINNER
    # -----------------------------

    alive_players = [p for p in contestants if p.alive]

    return len(alive_players) == 1