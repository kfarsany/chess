# Kian Farsany
# Chess
# Artificial Intelligence for Chess (console version)

import game_logic
import time
import random


class AI:
    def __init__(self):
        self.thinking_time = 3
        self.thinking_phrases = ["Thinking...", "Hey, what's that behind you?", "I see mate in 50...",
                                 "Just give me a second!", "What's en passant mean again?"]

    def make_move(self, game_state: game_logic.GameState) -> (game_logic, int, int):
        # for now just make random moves
        self._print_thinking()
        time.sleep(self.thinking_time)
        for piece in game_state.all_possible_moves:
            if piece.color is game_state.turn and len(game_state.all_possible_moves[piece]) > 0:
                for coords in game_state.all_possible_moves[piece]:
                    return piece, coords[0], coords[1]

    def _print_thinking(self) -> None:
        """
        Shhhhh, AI is thinking...
        :return: None
        """
        print(self.thinking_phrases[random.randint(0, len(self.thinking_phrases) - 1)])
