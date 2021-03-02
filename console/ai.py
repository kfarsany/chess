# Kian Farsany
# Chess
# Artificial Intelligence for Chess (console version)

import game_logic


class AI:
    def __init__(self, game_state: game_logic.GameState, color: int):
        self.game_state = game_state
        self.color = color

    def make_move(self, game_state: game_logic.GameState) -> (game_logic, int, int):
        # for now just make random moves
        piece = game_state.pieces.pop()
        game_state.pieces.add(piece)
        for coords in game_state.all_possible_moves[piece]:
            return piece, coords[0], coords[1]
