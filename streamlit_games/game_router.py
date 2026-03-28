def run_game_visual(game, player):

    import streamlit as st

    name = game["name"].lower()

    try:
        result = 0  # default safe value

        if "snake" in name:
            from streamlit_games.snake_ui import run as runSnake
            result = runSnake(player)

        elif "maze" in name or "bfs" in name or "dfs" in name:
            from streamlit_games.maze_ui import run as runMaze
            result = runMaze(player)

        elif "puzzle" in name:
            from streamlit_games.puzzle_ui import run as runPuzzle
            result = runPuzzle(player)

        elif "tic" in name:
            result = 0

        else:
            # fallback safety
            return 0

        # -----------------------------
        # ✅ UNIFIED RESULT HANDLING
        # -----------------------------
        if isinstance(result, tuple):
            result = result[0]

        if isinstance(result, dict):
            result = result.get("score", 0)

        if result is None:
            result = 0

        return result

    except Exception as e:
        st.error(f"Game crashed: {e}")
        return 0