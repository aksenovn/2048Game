import tkinter as tk
from tkinter import messagebox

try:
    from .game_2048 import Game2048
except ImportError:
    from game_2048 import Game2048

class Game2048GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("2048 Game")
        self.master.geometry("400x500") # Initial size, can be adjusted

        self.game = Game2048()

        # Tile colors and fonts
        self.tile_colors = {
            0: {"background": "#cdc1b4", "foreground": "#776e65"},
            2: {"background": "#eee4da", "foreground": "#776e65"},
            4: {"background": "#ede0c8", "foreground": "#776e65"},
            8: {"background": "#f2b179", "foreground": "#f9f6f2"},
            16: {"background": "#f59563", "foreground": "#f9f6f2"},
            32: {"background": "#f67c5f", "foreground": "#f9f6f2"},
            64: {"background": "#f65e3b", "foreground": "#f9f6f2"},
            128: {"background": "#edcf72", "foreground": "#f9f6f2"},
            256: {"background": "#edcc61", "foreground": "#f9f6f2"},
            512: {"background": "#edc850", "foreground": "#f9f6f2"},
            1024: {"background": "#edc53f", "foreground": "#f9f6f2"},
            2048: {"background": "#edc22e", "foreground": "#f9f6f2"},
            # For higher values, just use 2048's color
        }
        self.font = ("Helvetica", 24, "bold")

        self._create_widgets()
        self._draw_board()

        self.master.bind("<Key>", self._key_handler)

    def _create_widgets(self):
        self.score_label = tk.Label(self.master, text="Score: 0", font=("Helvetica", 16))
        self.score_label.pack(pady=10)

        self.game_frame = tk.Frame(self.master, bg="#bbada0", padx=5, pady=5)
        self.game_frame.pack()

        self.grid_cells = []
        for r in range(self.game.size):
            row_cells = []
            for c in range(self.game.size):
                cell_frame = tk.Frame(
                    self.game_frame,
                    bg=self.tile_colors[0]["background"],
                    width=80,
                    height=80
                )
                cell_frame.grid(row=r, column=c, padx=5, pady=5)
                tile_label = tk.Label(cell_frame, text="", bg=self.tile_colors[0]["background"],
                                      font=self.font, width=4, height=2)
                tile_label.pack(expand=True)
                row_cells.append(tile_label)
            self.grid_cells.append(row_cells)

        self.game_over_label = tk.Label(self.master, text="", font=("Helvetica", 24, "bold"), fg="red")
        self.game_over_label.pack(pady=20)

    def _draw_board(self):
        for r in range(self.game.size):
            for c in range(self.game.size):
                tile_value = self.game.board[r][c]
                tile_label = self.grid_cells[r][c]
                tile_label.config(text=str(tile_value) if tile_value != 0 else "")

                # Get colors, default to 2048 colors for values > 2048
                colors = self.tile_colors.get(tile_value, self.tile_colors[2048])
                tile_label.config(bg=colors["background"], fg=colors["foreground"])

        self.score_label.config(text=f"Score: {self.game.score}")

        if self.game.game_over:
            self.game_over_label.config(text="Game Over! Press 'r' to restart.")
        else:
            self.game_over_label.config(text="")

    def _key_handler(self, event):
        if self.game.game_over:
            if event.keysym == 'r':
                self.game = Game2048() # Start a new game
                self._draw_board()
            return

        moved = False
        if event.keysym == 'Up':
            moved = self.game.move('up')
        elif event.keysym == 'Down':
            moved = self.game.move('down')
        elif event.keysym == 'Left':
            moved = self.game.move('left')
        elif event.keysym == 'Right':
            moved = self.game.move('right')

        if moved:
            self._draw_board()
            if self.game.game_over:
                self.game_over_label.config(text="Game Over! Press 'r' to restart.")


if __name__ == "__main__":
    root = tk.Tk()
    gui = Game2048GUI(root)
    root.mainloop()
