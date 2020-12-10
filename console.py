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
    print(text)


def _print_turn(state) -> None:
    print("Turn: ", end='')
    if state.turn is game_logic.WHITE:
        print("W")
    else:
        print('B')


def _retrieve_move_input() -> (pieces.Piece, int, int):
    piece = input("Piece Row and Column? ")
    piece = piece.split()
    piece[0], piece[1] = int(piece[0]), int(piece[1])
    row = int(input("Row? "))
    col = int(input("Column? "))
    return game_state.board[piece[0]][piece[1]], row, col


if __name__ == "__main__":
    game_state = game_logic.GameState()
    while True:
        _print_board(game_state)
        _print_turn(game_state)
        try:
            move = _retrieve_move_input()
        except IndexError or TypeError or ValueError:
            print("Input Error\n")
            continue
        if move[0].color != game_state.turn:
            print("Wrong Piece Chosen\n")
            continue
        print(move)
        print()
