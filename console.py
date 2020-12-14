# Kian Farsany
# Chess
# Console/Main

import game_logic


def _print_board(state: game_logic.GameState) -> None:
    text = ''
    for i in state.board:
        for x in i:
            if isinstance(x, game_logic.Piece):
                text += x.name + "  "
            else:
                text += "...  "
        text = text.rstrip() + "\n"
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
        except KeyError:
            print("Input Error\n")
            continue
        try:
            game_state.execute_move(user_move)
        except game_logic.InvalidPositionError:
            print("Invalid Move\n")
            continue
        print()
