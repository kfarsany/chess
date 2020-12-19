# Kian Farsany
# Chess
# Game Logic and Piece Classes
import copy

WHITE = 1
BLACK = -1


class GameState:

    def __init__(self):
        self.turn = WHITE
        self.check = 0  # This color is under check. check = 0 means there is no check
        self.mate = False  # True if checkmate, False if not
        self.board = [[]]  # 2-D array of Pieces or None
        self.pieces = set()  # set of Pieces
        #############################################
        self.black_rook_count = 2
        self.black_knight_count = 2
        self.black_bishop_count = 2
        self.black_queen_count = 1
        self.white_rook_count = 2
        self.white_knight_count = 2
        self.white_bishop_count = 2
        self.white_queen_count = 1
        #############################################
        self.all_possible_moves = dict(dict())  # {Piece: {(row, col): Piece to capture}}
        self.lookahead = True   # Is this GameState allowed to look ahead?
        self._initialize_game()

    def execute_move(self, desired_move: ('Piece', int, int)) -> None:
        piece, new_row, new_col = desired_move
        captured_square = self.all_possible_moves[piece][(new_row, new_col)]
        if isinstance(captured_square, Piece):
            self.board[captured_square.row][captured_square.col] = None
            self.pieces.remove(captured_square)
        self.board[piece.row][piece.col] = None
        self.board[new_row][new_col] = piece
        piece.move(new_row, new_col)

        if isinstance(piece, King) and (new_col == 1 or new_col == 6):
            self._complete_castle(piece.row, new_col)
        if isinstance(piece, Pawn) and (new_row == 0 or new_row == 7):
            self._convert_pawn(piece)
        self._update_possible_moves()
        self._check_for_check()
        self._change_turn()

    def _convert_pawn(self, pawn: 'Pawn') -> None:
        self.pieces.remove(pawn)
        while True:
            print("(R)ook\nk(N)ight\n(B)ishop\n(Q)ueen")
            conversion = input("Finish Him: ")
            if conversion == "R":
                if pawn.color is BLACK:
                    self.black_rook_count += 1
                    conversion = Rook(pawn.row, pawn.col, pawn.color, "BR" + str(self.black_rook_count))
                else:
                    self.white_rook_count += 1
                    conversion = Rook(pawn.row, pawn.col, pawn.color, "WR" + str(self.white_rook_count))
                break
            elif conversion == "N":
                if pawn.color is BLACK:
                    self.black_knight_count += 1
                    conversion = Knight(pawn.row, pawn.col, pawn.color, "BN" + str(self.black_knight_count))
                else:
                    self.white_knight_count += 1
                    conversion = Knight(pawn.row, pawn.col, pawn.color, "WN" + str(self.white_knight_count))
                break
            elif conversion == "B":
                if pawn.color is BLACK:
                    self.black_bishop_count += 1
                    conversion = Bishop(pawn.row, pawn.col, pawn.color, "BB" + str(self.black_bishop_count))
                else:
                    self.white_bishop_count += 1
                    conversion = Bishop(pawn.row, pawn.col, pawn.color, "WB" + str(self.white_bishop_count))
                break
            elif conversion == "Q":
                if pawn.color is BLACK:
                    self.black_queen_count += 1
                    conversion = Queen(pawn.row, pawn.col, pawn.color, "BQ" + str(self.black_queen_count))
                else:
                    self.white_queen_count += 1
                    conversion = Queen(pawn.row, pawn.col, pawn.color, "WQ" + str(self.white_queen_count))
                break
            else:
                print("And I thought you were winning...")
                continue
        self.pieces.add(conversion)
        self.board[conversion.row][conversion.col] = conversion

    def _complete_castle(self, row: int, new_col: int) -> None:
        if new_col == 6:
            self.board[row][5] = self.board[row][7]
            self.board[row][7] = None
            self.board[row][5].col = 5
        else:
            self.board[row][3] = self.board[row][0]
            self.board[row][0] = None
            self.board[row][3].col = 3

    def _update_possible_moves(self) -> None:
        self.all_possible_moves.clear()
        for row in self.board:
            for square in row:
                if isinstance(square, Piece):
                    self.pieces.add(square)
                    square.calculate_possible_moves(self.board)
                    self.all_possible_moves[square] = square.possible_moves
        if self.lookahead:
            self._lookahead_for_check()

    def _lookahead_for_check(self) -> None:
        moves_copy = copy.deepcopy(self.all_possible_moves)
        for piece, moves in moves_copy.items():
            for row, col in moves.keys():
                next_state = copy.deepcopy(self)
                next_state.lookahead = False
                next_state.execute_move((_get_equivalent_piece(piece, next_state), row, col))
                if next_state.check == -self.turn:
                    self.all_possible_moves[_get_equivalent_piece(piece, self)].pop((row, col))

    def _check_for_check(self) -> None:
        for move_dict in self.all_possible_moves.values():
            for capture in move_dict.values():
                if isinstance(capture, King):
                    self.check = capture.color
                    self._check_for_mate()
                    return
        self.check = 0

    def _check_for_mate(self) -> None:
        for piece in self.pieces:
            if piece.color is self.check and len(piece.possible_moves) != 0:
                break
        self.mate = True

    def _change_turn(self) -> None:
        self.turn = -self.turn

    def _initialize_game(self) -> None:
        self.board = [[None for _ in range(8)] for _ in range(8)]

        for i in range(8):
            self.board[1][i], self.board[6][i] = Pawn(i, BLACK), Pawn(i, WHITE)

        self.board[0][0], self.board[0][7] = Rook(0, 0, BLACK, "BR2"), Rook(0, 7, BLACK, "BR1")
        self.board[0][1], self.board[0][6] = Knight(0, 1, BLACK, "BN2"), Knight(0, 6, BLACK, "BN1")
        self.board[0][2], self.board[0][5] = Bishop(0, 2, BLACK, "BB2"), Bishop(0, 5, BLACK, "BB1")
        self.board[0][3] = Queen(0, 3, BLACK, "BQ1")
        self.board[0][4] = King(BLACK)

        self.board[7][0], self.board[7][7] = Rook(7, 0, WHITE, "WR1"), Rook(7, 7, WHITE, "WR2")
        self.board[7][1], self.board[7][6] = Knight(7, 1, WHITE, "WN1"), Knight(7, 6, WHITE, "WN2")
        self.board[7][2], self.board[7][5] = Bishop(7, 2, WHITE, "WB1"), Bishop(7, 5, WHITE, "WB2")
        self.board[7][3] = Queen(7, 3, WHITE, "WQ1")
        self.board[7][4] = King(WHITE)
        self._update_possible_moves()


class Piece:
    def __init__(self, row: int, col: int, color: int, name: str):
        self.row = row
        self.col = col
        self.color = color
        self.name = name
        self.possible_moves = dict()  # {(row, col): Piece to capture}

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def add_move_to_possibles(self, board: [['Piece']], row: int, col: int) -> None:
        self.possible_moves[(row, col)] = board[row][col]

    def explore_upper_right_diagonal(self, board: [['Piece']]) -> None:
        row, col = self.row - 1, self.col + 1
        while row >= 0 and col <= 7:
            if _is_space_occupied(board, row, col):
                if board[row][col].color is not self.color:
                    self.add_move_to_possibles(board, row, col)
                break
            else:
                self.add_move_to_possibles(board, row, col)
            row -= 1
            col += 1

    def explore_upper_left_diagonal(self, board: [['Piece']]) -> None:
        row, col = self.row - 1, self.col - 1
        while row >= 0 and col >= 0:
            if _is_space_occupied(board, row, col):
                if board[row][col].color is not self.color:
                    self.add_move_to_possibles(board, row, col)
                break
            else:
                self.add_move_to_possibles(board, row, col)
            row -= 1
            col -= 1

    def explore_lower_right_diagonal(self, board: [['Piece']]) -> None:
        row, col = self.row + 1, self.col + 1
        while row <= 7 and col <= 7:
            if _is_space_occupied(board, row, col):
                if board[row][col].color is not self.color:
                    self.add_move_to_possibles(board, row, col)
                break
            else:
                self.add_move_to_possibles(board, row, col)
            row += 1
            col += 1

    def explore_lower_left_diagonal(self, board: [['Piece']]) -> None:
        row, col = self.row + 1, self.col - 1
        while row <= 7 and col >= 0:
            if _is_space_occupied(board, row, col):
                if board[row][col].color is not self.color:
                    self.add_move_to_possibles(board, row, col)
                break
            else:
                self.add_move_to_possibles(board, row, col)
            row += 1
            col -= 1

    def explore_up(self, board: [['Piece']]) -> None:
        row = self.row - 1
        while row >= 0:
            if _is_space_occupied(board, row, self.col):
                if board[row][self.col].color is not self.color:
                    self.add_move_to_possibles(board, row, self.col)
                break
            else:
                self.add_move_to_possibles(board, row, self.col)
            row -= 1

    def explore_down(self, board: [['Piece']]) -> None:
        row = self.row + 1
        while row <= 7:
            if _is_space_occupied(board, row, self.col):
                if board[row][self.col].color is not self.color:
                    self.add_move_to_possibles(board, row, self.col)
                break
            else:
                self.add_move_to_possibles(board, row, self.col)
            row += 1

    def explore_right(self, board: [['Piece']]) -> None:
        col = self.col + 1
        while col <= 7:
            if _is_space_occupied(board, self.row, col):
                if board[self.row][col].color is not self.color:
                    self.add_move_to_possibles(board, self.row, col)
                break
            else:
                self.add_move_to_possibles(board, self.row, col)
            col += 1

    def explore_left(self, board: [['Piece']]) -> None:
        col = self.col - 1
        while col >= 0:
            if _is_space_occupied(board, self.row, col):
                if board[self.row][col].color is not self.color:
                    self.add_move_to_possibles(board, self.row, col)
                break
            else:
                self.add_move_to_possibles(board, self.row, col)
            col -= 1

    def calculate_possible_moves(self, board: [['Piece']]) -> None:
        pass


class Pawn(Piece):
    def __init__(self, col: int, color: int):
        if color is WHITE:
            row = 6
            name = 'WP{}'.format(col + 1)
        else:
            row = 1
            name = 'BP{}'.format(8 - col)

        Piece.__init__(self, row, col, color, name)
        self.en_passant = False  # Can this piece taken by en passant?

    def move(self, new_row: int, new_col: int) -> None:
        if abs(new_row - self.row) == 2:
            self.en_passant = True
        else:
            self.en_passant = False

        self.row = new_row
        self.col = new_col

    def calculate_possible_moves(self, board: [[Piece]]) -> None:
        self.possible_moves.clear()
        if self.color is WHITE:
            self._calculate_white_moves(board)
        else:
            self._calculate_black_moves(board)

    def _calculate_white_moves(self, board: [[Piece]]) -> None:
        if self.row == 6:  # Jumps
            if _is_space_empty(board, self.row - 1, self.col) and \
                    _is_space_empty(board, self.row - 2, self.col):
                self.add_move_to_possibles(board, self.row - 2, self.col)
        if 0 < self.row < 7:
            if _is_space_empty(board, self.row - 1, self.col):  # Pushes
                self.add_move_to_possibles(board, self.row - 1, self.col)
            if self.col != 7:  # Right Captures and En Passants
                if _is_space_occupied(board, self.row - 1, self.col + 1) and \
                        board[self.row - 1][self.col + 1].color is BLACK:  # Capture
                    self.add_move_to_possibles(board, self.row - 1, self.col + 1)
                if _is_space_occupied(board, self.row, self.col + 1) and \
                        _is_space_empty(board, self.row - 1, self.col + 1) and \
                        isinstance(board[self.row][self.col + 1], Pawn) and \
                        board[self.row][self.col + 1].color is BLACK and \
                        board[self.row][self.col + 1].en_passant:  # En Passant
                    self.possible_moves[(self.row - 1, self.col + 1)] = board[self.row][self.col + 1]
            if self.col != 0:  # Left Captures and En Passants
                if _is_space_occupied(board, self.row - 1, self.col - 1) and \
                        board[self.row - 1][self.col - 1].color is BLACK:  # Capture
                    self.add_move_to_possibles(board, self.row - 1, self.col - 1)
                if _is_space_occupied(board, self.row, self.col - 1) and \
                        _is_space_empty(board, self.row - 1, self.col - 1) and \
                        isinstance(board[self.row][self.col - 1], Pawn) and \
                        board[self.row][self.col - 1].color is BLACK and \
                        board[self.row][self.col - 1].en_passant:  # En Passant
                    self.possible_moves[(self.row - 1, self.col - 1)] = board[self.row][self.col - 1]

    def _calculate_black_moves(self, board: [[Piece]]) -> None:
        if self.row == 1:  # Jumps
            if _is_space_empty(board, self.row + 1, self.col) and \
                    _is_space_empty(board, self.row + 2, self.col):
                self.add_move_to_possibles(board, self.row + 2, self.col)
        if 0 < self.row < 7:
            if _is_space_empty(board, self.row + 1, self.col):  # Pushes
                self.add_move_to_possibles(board, self.row + 1, self.col)
            if self.col != 7:  # Right Captures and En Passants
                if _is_space_occupied(board, self.row + 1, self.col + 1) and \
                        board[self.row + 1][self.col + 1].color is WHITE:  # Capture
                    self.add_move_to_possibles(board, self.row + 1, self.col + 1)
                if _is_space_occupied(board, self.row, self.col + 1) and \
                        _is_space_empty(board, self.row + 1, self.col + 1) and \
                        isinstance(board[self.row][self.col + 1], Pawn) and \
                        board[self.row][self.col + 1].color is WHITE and \
                        board[self.row][self.col + 1].en_passant:  # En Passant
                    self.possible_moves[(self.row + 1, self.col + 1)] = board[self.row][self.col + 1]
            if self.col != 0:  # Left Captures and En Passants
                if _is_space_occupied(board, self.row + 1, self.col - 1) and \
                        board[self.row + 1][self.col - 1].color is WHITE:  # Capture
                    self.add_move_to_possibles(board, self.row + 1, self.col - 1)
                if _is_space_occupied(board, self.row, self.col - 1) and \
                        _is_space_empty(board, self.row + 1, self.col - 1) and \
                        isinstance(board[self.row][self.col - 1], Pawn) and \
                        board[self.row][self.col - 1].color is WHITE and \
                        board[self.row][self.col - 1].en_passant:  # En Passant
                    self.possible_moves[(self.row + 1, self.col - 1)] = board[self.row][self.col - 1]


class Knight(Piece):
    def __init__(self, row: int, col: int, color: int, name: str):
        Piece.__init__(self, row, col, color, name)

    def move(self, new_row: int, new_col: int) -> None:
        self.row = new_row
        self.col = new_col

    def calculate_possible_moves(self, board: [[Piece]]) -> None:
        self.possible_moves.clear()
        possibles = {(self.row + 1, self.col - 2), (self.row - 1, self.col - 2),
                     (self.row + 1, self.col + 2), (self.row - 1, self.col + 2),
                     (self.row + 2, self.col - 1), (self.row + 2, self.col + 1),
                     (self.row - 2, self.col - 1), (self.row - 2, self.col + 1)}
        for row, col in possibles:
            if _in_bounds(row, col):
                if _is_space_empty(board, row, col) or board[row][col].color is not self.color:
                    self.add_move_to_possibles(board, row, col)


class Bishop(Piece):
    def __init__(self, row: int, col: int, color: int, name: str):
        Piece.__init__(self, row, col, color, name)

    def move(self, new_row: int, new_col: int) -> None:
        self.row = new_row
        self.col = new_col

    def calculate_possible_moves(self, board: [[Piece]]) -> None:
        self.possible_moves.clear()

        if self.row > 0 and self.col < 7:
            Piece.explore_upper_right_diagonal(self, board)
        if self.row > 0 and self.col > 0:
            Piece.explore_upper_left_diagonal(self, board)
        if self.row < 7 and self.col < 7:
            Piece.explore_lower_right_diagonal(self, board)
        if self.row < 7 and self.col > 0:
            Piece.explore_lower_left_diagonal(self, board)


class Rook(Piece):
    def __init__(self, row: int, col: int, color: int, name: str):
        Piece.__init__(self, row, col, color, name)
        self.can_castle = True

    def move(self, new_row: int, new_col: int) -> None:
        self.row = new_row
        self.col = new_col
        self.can_castle = False

    def calculate_possible_moves(self, board: [[Piece]]) -> None:
        self.possible_moves.clear()

        if self.row > 0:
            Piece.explore_up(self, board)
        if self.row < 7:
            Piece.explore_down(self, board)
        if self.col < 7:
            Piece.explore_right(self, board)
        if self.col > 0:
            Piece.explore_left(self, board)


class Queen(Piece):
    def __init__(self, row: int, col: int, color: int, name: str):
        Piece.__init__(self, row, col, color, name)

    def move(self, new_row: int, new_col: int) -> None:
        self.row = new_row
        self.col = new_col

    def calculate_possible_moves(self, board: [[Piece]]) -> None:
        self.possible_moves.clear()

        if self.row > 0 and self.col < 7:
            Piece.explore_upper_right_diagonal(self, board)
        if self.row > 0 and self.col > 0:
            Piece.explore_upper_left_diagonal(self, board)
        if self.row < 7 and self.col < 7:
            Piece.explore_lower_right_diagonal(self, board)
        if self.row < 7 and self.col > 0:
            Piece.explore_lower_left_diagonal(self, board)

        if self.row > 0:
            Piece.explore_up(self, board)
        if self.row < 7:
            Piece.explore_down(self, board)
        if self.col < 7:
            Piece.explore_right(self, board)
        if self.col > 0:
            Piece.explore_left(self, board)


class King(Piece):
    def __init__(self, color: int):
        if color is WHITE:
            row = 7
            name = 'WKG'
        else:
            row = 0
            name = 'BKG'

        Piece.__init__(self, row, 4, color, name)
        self.can_castle = True

    def move(self, new_row: int, new_col: int) -> None:
        self.row = new_row
        self.col = new_col
        self.can_castle = False

    def calculate_possible_moves(self, board: [[Piece]]) -> None:
        self.possible_moves.clear()
        possibles = {(self.row + 1, self.col - 1), (self.row - 1, self.col - 1),
                     (self.row + 1, self.col + 1), (self.row - 1, self.col + 1),
                     (self.row, self.col - 1), (self.row, self.col + 1),
                     (self.row - 1, self.col), (self.row + 1, self.col)}
        for row, col in possibles:
            if _in_bounds(row, col):
                if _is_space_empty(board, row, col) or board[row][col].color is not self.color:
                    self.add_move_to_possibles(board, row, col)

        if self.can_castle:
            self._explore_castles(board)

    def _explore_castles(self, board: [[Piece]]) -> None:
        if isinstance(board[self.row][7], Rook) and board[self.row][7].can_castle:
            if _is_space_empty(board, self.row, 5) and _is_space_empty(board, self.row, 6):
                self.add_move_to_possibles(board, self.row, 6)

        if isinstance(board[self.row][0], Rook) and board[self.row][0].can_castle:
            if _is_space_empty(board, self.row, 1) and _is_space_empty(board, self.row, 2) \
                    and _is_space_empty(board, self.row, 3):
                self.add_move_to_possibles(board, self.row, 2)


def _in_bounds(row: int, col: int) -> bool:
    return row in range(8) and col in range(8)


def _is_space_occupied(board: [[Piece]], row: int, col: int) -> bool:
    return isinstance(board[row][col], Piece)


def _is_space_empty(board: [[Piece]], row: int, col: int) -> bool:
    return not _is_space_occupied(board, row, col)


def _get_equivalent_piece(piece: Piece, game_state: GameState) -> Piece:
    for bizarro_piece in game_state.pieces:
        if piece.name == bizarro_piece.name:
            return bizarro_piece
