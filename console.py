# Kian Farsany
# Chess
# Console/Main
import time     # ##############################

import game_logic


def _print_board(state: game_logic.GameState) -> None:
    text = ''
    count = 0
    for i in state.board:
        text += str(count) + '\t'
        for x in i:
            if isinstance(x, game_logic.Piece):
                text += x.name + "  "
            else:
                text += "...  "
        text = text.rstrip() + "\n"
        count += 1
    text += " \t 0    1    2    3    4    5    6    7"
    print(text)


def _print_turn(state: game_logic.GameState) -> None:
    print("Turn: ", end='')
    if state.turn is game_logic.WHITE:
        print("W")
    else:
        print('B')


def _retrieve_move_input(state: game_logic.GameState) -> (game_logic.Piece, int, int):
    user_input = input("Piece Name? ")
    if state.turn == game_logic.WHITE:
        user_input = 'W' + user_input
    else:
        user_input = 'B' + user_input
    try:
        row = int(input("Row? "))
        col = int(input("Column? "))
    except ValueError:
        raise KeyError()
    for piece in state.pieces:
        if user_input == piece.name:
            return piece, row, col
    raise KeyError()


if __name__ == "__main__":
    game_state = game_logic.GameState()
    while True:
        _print_board(game_state)
        _print_turn(game_state)
        #####################################################
        for kv in game_state.all_possible_moves.items():
            print(kv)
        #####################################################
        try:
            user_move = _retrieve_move_input(game_state)
            start = time.time()  # ########################
        except KeyError:
            print("Input Error\n")
            continue
        try:
            game_state.execute_move(user_move)
        except game_logic.InvalidPositionError:
            print("Invalid Move\n")
            continue
        print()
        stop = time.time()  # #############################
        print(str(start) + '   ' + str(stop) + 's')  # ###############################
