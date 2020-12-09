# Kian Farsany
# Chess
# Game Logic

import pieces
WHITE = 1
BLACK = 0
ROWS = 8
COLS = 8


class GameState:

    def __init__(self):
        self.turn = WHITE
        self._initialize_board()

    def _initialize_board(self) -> [[pieces.Piece]]:
        self.board = [[None for _ in range(8)] for _ in range(8)]

        for i in range(8):
            self.board[1][i], self.board[6][i] = pieces.Pawn(i, BLACK), pieces.Pawn(i, WHITE)

        self.board[0][0], self.board[0][7] = pieces.Rook(0, BLACK), pieces.Rook(7, BLACK)
        self.board[0][1], self.board[0][6] = pieces.Knight(1, BLACK), pieces.Knight(6, BLACK)
        self.board[0][2], self.board[0][5] = pieces.Bishop(2, BLACK), pieces.Bishop(5, BLACK)
        self.board[0][3], self.board[0][4] = pieces.Queen(BLACK), pieces.King(BLACK)

        self.board[7][0], self.board[7][7] = pieces.Rook(0, WHITE), pieces.Rook(7, WHITE)
        self.board[7][1], self.board[7][6] = pieces.Knight(1, WHITE), pieces.Knight(6, WHITE)
        self.board[7][2], self.board[7][5] = pieces.Bishop(2, WHITE), pieces.Bishop(5, WHITE)
        self.board[7][3], self.board[7][4] = pieces.Queen(WHITE), pieces.King(WHITE)
