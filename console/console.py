# Kian Farsany
# Chess
# Console/Main

import random
import game_logic
from ai import AI


def _run() -> None:
    """
    Large overhead run function that is essentially the same as __main__
    :return: None
    """
    is_ai_present, ai_color = _ai_setup()
    if not is_ai_present:
        _run_without_ai()
    else:
        if ai_color is None:
            _run_with_two_ais()
        else:
            _run_with_one_ai(ai_color)


def _run_with_one_ai(ai_color: int) -> None:
    """
    Runs the chess game for human vs. AI
    Handles executing moves and printing GameState info to the console
    Handles victories or stalemates
    :return: None
    """
    game_state = game_logic.GameState()
    ai = AI()
    while True:
        _print_board(game_state)
        if _is_endgame(game_state):
            break
        _print_turn(game_state)

        if game_state.turn is ai_color:
            move = ai.make_move(game_state)
        else:
            try:
                move = _retrieve_move_input(game_state)
            except NameError:
                print("I know not what that piece is...\n")
                continue
            except IndexError:
                print("I'm afraid that piece cannot move...\n")
                continue
            except ArithmeticError:
                print("It's ok, we all make mistakes...\n")
                continue

        game_state.execute_move(move)
        print()


def _run_with_two_ais() -> None:
    """
    Runs the chess game for obersvation of two AIs
    Handles executing moves and printing GameState info to the console
    Handles victories or stalemates
    :return: None
    """
    game_state = game_logic.GameState()
    ai_white = AI()
    ai_black = AI()
    while True:
        _print_board(game_state)
        if _is_endgame(game_state):
            break
        _print_turn(game_state)

        if game_state.turn is game_logic.WHITE:
            move = ai_white.make_move(game_state)
        else:
            move = ai_black.make_move(game_state)

        game_state.execute_move(move)
        print()


def _run_without_ai() -> None:
    """
    Runs the chess game for two human players
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
            move = _retrieve_move_input(game_state)
        except NameError:
            print("I know not what that piece is...\n")
            continue
        except IndexError:
            print("I'm afraid that piece cannot move...\n")
            continue
        except ArithmeticError:
            print("It's ok, we all make mistakes...\n")
            continue

        game_state.execute_move(move)
        print()


def _ai_setup() -> (bool, "int or None"):
    """
    Retrieves AI preferences from user.
    If ai_color is None, either there will be two humans or two AIs.
    If ai_color is not None, the user will play an AI, and the user will have specified a preferred color.
    :return: (will AI be used?, ai_color)
    """
    ai_choice = _get_user_ai_choice()
    ai_color = None
    if ai_choice:
        ai_color = _get_user_ai_prefs()
    return ai_choice, ai_color


def _get_user_ai_choice() -> bool:
    """
    Returns true if user wants to utilize AI
    :return: bool
    """
    while True:
        ai_choice = input("Use AI? (y/n): ").lower()
        if ai_choice == 'y':
            return True
        elif ai_choice == 'n':
            return False
        else:
            print("Pardon me? Try again, old chap!")


def _get_user_ai_prefs() -> "int or None":
    """
    Returns the color of the AI if there will be only one AI.
    If the user wishes to observe two AI play each other, return None.
    :return: int or None
    """
    while True:
        play_input = input("\nWould you like to (p)lay or (o)bserve?: ").lower()
        if play_input == 'p':
            return - _get_color_input()
        elif play_input == 'o':
            return None
        else:
            print("Speak the King's English, old bean!")


def _get_color_input() -> int:
    """
    Helper to get the user's color choice
    :return: int
    """
    while True:
        color_input = input("\nDo you want (b)lack or (w)hite?: ").lower()
        if color_input == 'b':
            return game_logic.BLACK
        elif color_input == 'w':
            return game_logic.WHITE
        else:
            print("Buck up, young one; you'll get it eventually!")


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
