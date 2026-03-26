# games/__init__.py
# List of all games

from .snake_ladder import play_snake_ladder
from .tic_tac_toe  import play_tictactoe
from .bfs_maze     import play_bfs
from .dfs_maze     import play_dfs
from .puzzle_8     import play_8puzzle
from .maze_solver  import play_maze


ALL_GAMES = [
    {"no": 1, "name": "Snake and Ladder", "main_attr": "adaptability", "fn": play_snake_ladder},
    {"no": 2, "name": "Tic Tac Toe",      "main_attr": "intelligence", "fn": play_tictactoe},
    {"no": 3, "name": "BFS Maze Solver",  "main_attr": "intelligence", "fn": play_bfs},
    {"no": 4, "name": "DFS Maze Solver",  "main_attr": "adaptability", "fn": play_dfs},
    {"no": 5, "name": "8-Puzzle",         "main_attr": "intelligence", "fn": play_8puzzle},
    {"no": 6, "name": "Maze Solver",      "main_attr": "intelligence", "fn": play_maze},
]