# Kian Farsany
# Chess
# Console/Main

import game_logic


def _run() -> None:
    game_state = game_logic.GameState()
    while True:
        _print_board(game_state)
        if game_state.check:
            print("CZECH!!!!!!!!!!")
        _print_turn(game_state)
        #####################################################
        for kv in game_state.all_possible_moves.items():
            print(kv)
        #####################################################
        try:
            user_move = _retrieve_move_input(game_state)
        except NameError:
            print("I know not what that piece is...\n")
            continue
        except IndexError:
            print("I'm afraid that piece cannot move...\n")
            continue
        except ArithmeticError:
            print("It's ok, we all make mistakes...\n")
            continue

        game_state.execute_move(user_move)
        print()


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
        user_input = 'W' + user_input.upper()
    else:
        user_input = 'B' + user_input.upper()
    for p in state.pieces:
        if user_input == p.name:
            moves = list(p.possible_moves.keys())
            piece = p
            break
    else:
        raise NameError()

    if not moves:
        raise IndexError()
    else:
        _print_moves(moves)

    return _user_select_move(piece, moves)


def _print_moves(moves: [(int, int)]) -> None:
    print("Possible moves: ")
    count = 1
    for move in moves:
        print(str(count) + ": " + str(move))
        count += 1
    print("0: Back->")


def _user_select_move(piece: game_logic.Piece, moves: [(int, int)]) -> (game_logic.Piece, int, int):
    while True:
        try:
            move = int(input("Enter move number: "))
            if int(move) == 0:
                raise ArithmeticError()
            return piece, moves[move - 1][0], moves[move - 1][1]
        except ValueError or IndexError:
            print("Huh?")
            continue


if __name__ == "__main__":
    _run()
