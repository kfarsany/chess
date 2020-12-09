# Kian Farsany
# Chess
# Console/Main

import game_logic
import pieces


def _print_board(state) -> None:
    text = ''
    for i in state.board:
        for x in i:
            if isinstance(x, pieces.Piece):
                text += x.name + "  "
            else:
                text += "...  "
        text = text.rstrip() + "\n"
    print(text[:-1])


if __name__ == "__main__":
    game_state = game_logic.GameState()
    _print_board(game_state)
