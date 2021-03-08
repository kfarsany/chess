# Kian Farsany
# Chess
# Artificial Intelligence for Chess (console version)

import game_logic
import time
import random

BEGINNER = 0
INTERMEDIATE = 1
HARD = 2


class AI:
    def __init__(self):
        # self._set_difficulty()
        self.thinking_time = 3
        self.thinking_phrases = ["Thinking...", "Hey, what's that behind you?", "My turn? That was fast...",
                                 "Just give me a second!", "How do you play this game again..."]

    def make_move(self, game_state: game_logic.GameState) -> (game_logic.Piece, int, int):
        """
        Top level function that returns the AI's best decision
        :param game_state: GameState
        :return: (Piece, row, col)
        """
        self._print_thinking()
        time.sleep(self.thinking_time)
        return _get_random_move(game_state)

    def _print_thinking(self) -> None:
        """
        Shhhhh, AI is thinking...
        :return: None
        """
        print(self.thinking_phrases[random.randint(0, len(self.thinking_phrases) - 1)])

    # def _set_difficulty(self) -> None:
    #     while True:
    #         user_input = input("\n(b)eginner\n(i)ntermediate\n(h)ard\nAI Difficulty?: ").lower()
    #         if user_input == 'b':
    #             self.difficulty = BEGINNER
    #         elif user_input == 'i':
    #             self.difficulty = INTERMEDIATE
    #         elif user_input == 'h':
    #             self.difficulty = HARD
    #         else:
    #             print("I say, good man! Please use proper language!")


def _get_random_move(game_state: game_logic.GameState) -> (game_logic.Piece, int, int):
    """
    The AI simply makes a random-ish move.  Good for beginners.
    :param game_state: GameState
    :return: (Piece, row, col)
    """
    for piece in game_state.all_possible_moves:
        if piece.color is game_state.turn and len(game_state.all_possible_moves[piece]) > 0:
            for coords in game_state.all_possible_moves[piece]:
                return piece, coords[0], coords[1]


def _heuristic(game_state: game_logic.GameState) -> int:
    """
    This is where the AI traverses the tree of moves and decides which is best.
    Returns an eval value that is then compared to many other eval values through recursive traversal.
    :param game_state: GameState
    :return: int
    """
    return _simple_eval(game_state)


def _simple_eval(game_state: game_logic.GameState) -> int:
    """
    Returns an arbitrary point value that judges the current state of the game.
    Note: evals like this don't care about checkmate or check; that's the heuristic's job.
    Current point system used: Fischer valuation
    :param game_state: GameState
    :return: int
    """
    points = 0
    for piece in game_state.pieces:
        piece_value = 1
        if isinstance(piece, game_logic.Knight):
            piece_value = 3
        elif isinstance(piece, game_logic.Bishop):
            piece_value = 3.25
        elif isinstance(piece, game_logic.Rook):
            piece_value = 5
        elif isinstance(piece, game_logic.Queen):
            piece_value = 9

        if piece.color is not game_state.turn:
            piece_value = -piece_value
        points += piece_value
    return points
