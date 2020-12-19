# Kian Farsany
# Chess
# Console/Main

import game_logic
import random


def _run() -> None:
    """
    Runs the chess game
    Handles executing moves and printing GameState info to the console
    Handles victories or stalemates
    :return: None
    """
    game_state = game_logic.GameState()
    while True:
        _print_board(game_state)
        if _is_endgame(game_state):
            break
        _print_turn(game_state)
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
    """
    Prints the board to the console using standard chess notation
    :param state: GameState
    :return: None
    """
    text = ''
    count = 8
    for i in state.board:
        text += str(count) + '\t'
        for x in i:
            if isinstance(x, game_logic.Piece):
                text += x.name + "  "
            else:
                text += "...  "
        text = text.rstrip() + "\n"
        count -= 1
    text += " \t a    b    c    d    e    f    g    h"
    print(text)


def _is_endgame(state: game_logic.GameState) -> bool:
    """
    Prints check, checkmate, and stalemate info to the console if applicable
    :param state: GameState
    :return: True if game is over (checkmate or stalemate). False if not
    """
    if state.mate:
        if state.check is game_logic.WHITE:
            print("BLACK is the victor")
        else:
            print("WHITE is the victor")
        return True
    elif state.check != 0:
        checks = ["CZECH", "CHUBBY CHECKER", "CHECK PLEASE"]
        print(checks[random.randint(0, 2)])
        return False
    elif state.stalemate:
        print("Such a stale finish...")
        return True
    else:
        return False


def _print_turn(state: game_logic.GameState) -> None:
    """Print whose turn it is"""
    print("Turn: ", end='')
    if state.turn is game_logic.WHITE:
        print("W")
    else:
        print('B')


def _retrieve_move_input(state: game_logic.GameState) -> (game_logic.Piece, int, int):
    """
    Receives input from the user(s) on which to move execute
    Lists the possible moves the user can make with their selected piece
    :param state: GameState
    :return: (Piece the user wants to move, desired row to move to, desired column to move to)
    """
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
    """
    Prints out the list of moves that the selected piece can make
    :param moves: List of (row, column) coordinates that represent moves
    :return: None
    """
    print("Possible moves: ")
    count = 1
    for move in moves:
        print(str(count) + ": " + _convert_move_format(move))
        count += 1
    print("0: Back->")


def _convert_move_format(move: (int, int)) -> str:
    """
    Converts move from (row, column) to typical chess format (e.g. a4, h3)
    :param move: (row: int, column: int)
    :return: str in chess format
    """
    cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    return str(cols[move[1]]) + str(8 - move[0])


def _user_select_move(piece: game_logic.Piece, moves: [(int, int)]) -> (game_logic.Piece, int, int):
    """
    Asks the user to select a certain move from the already printed list of possible moves for their selected piece
    Returns the final 3-tuple to _retrieve_move_input() so the GameState can execute the move
    :param piece: User's piece they chose to move
    :param moves: List of move coordinates that the piece can go to
    :return: (Piece to move, desired row, desired column)
    """
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
