import streamlit as st
import time

ROWS, COLS = 6, 6
START = (0, 0)
END = (5, 5)

MAZE = [
    [1,1,0,1,1,1],
    [0,1,0,1,0,1],
    [0,1,1,1,0,1],
    [0,0,0,1,1,1],
    [1,1,1,0,0,1],
    [1,0,1,1,1,1],
]

# 🎨 Draw Maze Grid
def draw_maze(explored=set(), path=set()):
    html = "<div style='display:inline-block;'>"

    for r in range(ROWS):
        html += "<div style='display:flex;'>"

        for c in range(COLS):
            bg = "#eee"

            if (r,c) == START:
                bg = "#9b59b6"   # purple
            elif (r,c) == END:
                bg = "#e74c3c"   # red
            elif MAZE[r][c] == 0:
                bg = "#000"      # wall
            elif (r,c) in path:
                bg = "#2ecc71"   # green path
            elif (r,c) in explored:
                bg = "#3498db"   # blue explored

            html += f"<div style=\"width:25px;height:25px;margin:1px;border-radius:4px;background:{bg};\"></div>"

        html += "</div>"

    html += "</div>"
    return html


def run(player):

    st.subheader(f"🧱 Maze Solver — {player.name}")

    grid_area = st.empty()
    info_area = st.empty()

    # 🔥 Run logic (through router → already structured)
    from games.bfs_maze import play_bfs
    from games.dfs_maze import play_dfs

    # Decide which to use based on name
    if player.intelligence > player.adaptability:
        result = play_bfs(player)
    else:
        result = play_dfs(player)

    explored = result["explored"]
    path = result["path"]
    score = result["score"]
    strategy = result["strategy"]

    st.info(f"Strategy Used: {strategy}")

    explored_set = set()

    # 🎬 Animate exploration
    for node in explored:
        explored_set.add(node)
        grid_area.markdown(
            draw_maze(explored=explored_set),
            unsafe_allow_html=True
        )
        time.sleep(0.1)

    # 🎯 Show final path
    path_set = set(path)

    grid_area.markdown(
        draw_maze(explored=explored_set, path=path_set),
        unsafe_allow_html=True
    )

    st.success(f"🏁 Completed! Score: {score}")

    return {
        "score": score
    }