# utils/helpers.py
# Small reusable utility functions

def sep(n=55):
    print("=" * n)

def get_int(prompt, lo=1, hi=100):
    while True:
        try:
            val = int(input(prompt))
            if lo <= val <= hi:
                return val
            print(f"  Enter a value between {lo} and {hi}!")
        except ValueError:
            print("  Enter only numbers!")

def draw_maze(maze, rows, cols, pos=None, start=None, end=None, path=None):
    for r in range(rows):
        row = "  "
        for c in range(cols):
            if pos and (r, c) == pos:
                row += " * "
            elif start and (r, c) == start:
                row += " S "
            elif end and (r, c) == end:
                row += " E "
            elif path and (r, c) in path:
                row += "[P]"
            elif maze[r][c] == 0:
                row += " # "
            else:
                row += " . "
        print(row)
    print()
