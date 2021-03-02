# Kian Farsany
# Chess
# GUI

import game_logic
import tkinter
from PIL import ImageTk, Image


class Chess:
    def __init__(self):
        self._root_window = tkinter.Tk()

        self.game_state = game_logic.GameState()

        self._canvas = tkinter.Canvas(
            master=self._root_window,
            width=800, height=800,
            background='#9f6934')
        self._canvas.grid(row=0, column=0)
        self._draw_board()

        self._root_window.rowconfigure(0, weight=1)
        self._root_window.columnconfigure(0, weight=1)

    def run(self) -> None:
        self._root_window.mainloop()

    def _draw_board(self) -> None:
        cell_width, cell_height = 100, 100
        for r in range(8):
            for c in range(8):
                x0, y0 = c * cell_width, r * cell_height
                x1, y1 = x0 + cell_width, y0 + cell_height
                if r % 2 == 0:
                    if c % 2 == 0:
                        self._canvas.create_rectangle(x0, y0, x1, y1, outline='black', fill='#ffdead')
                    else:
                        self._canvas.create_rectangle(x0, y0, x1, y1, outline='black')
                else:
                    if c % 2 == 0:
                        self._canvas.create_rectangle(x0, y0, x1, y1, outline='black')
                    else:
                        self._canvas.create_rectangle(x0, y0, x1, y1, outline='black', fill='#ffdead')
                self._draw_piece((x0+x1)/2, (y0+y1)/2, r, c, cell_width, cell_height)

    def _draw_piece(self, x: int, y: int, row: int, col: int, cell_width: int, cell_height: int) -> None:
        self.image = ImageTk.PhotoImage(Image.open("images\\w_king.jpg"))
        self._canvas.create_image(x, y, image=self.image, anchor="center")


if __name__ == "__main__":
    Chess().run()
