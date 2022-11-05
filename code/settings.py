import tkinter as tk

root = tk.Tk()

WIDTH = root.winfo_screenwidth() - 100
HEIGHT  = root.winfo_screenheight() - 100

FPS = 60
TILESIZE = HEIGHT/12

empty_row = [' ' for i in range(23)]
player_row = [' ' for i in range(10)] + ['p', 'X'] + [' ' for i in range(10)]
block_row = ['X' for i in range(23)]

WORLD_MAP = [
    empty_row,
    empty_row,
    empty_row,
    empty_row,
    empty_row,
    empty_row,
    empty_row,
    player_row,
    block_row,
    empty_row,
    empty_row,
    empty_row
]