# Kian Farsany
# Chess
# Game Logic and Piece Classes

WHITE = 1
BLACK = 0


class InvalidPositionError(Exception):
    pass


class GameState:

    def __init__(self):
        self.turn = WHITE
        self.board = [[]]   # 2-D array of Pieces or None
        self.pieces = set()     # set of Pieces
        self.all_possible_moves = dict(dict())     # {Piece: {(row, col): Piece to capture}}
        self._initialize_game()

    def execute_move(self, desired_move: ('Piece', int, int)) -> None:
        piece, new_row, new_col = desired_move
        old_row, old_col = int(piece.row), int(piece.col)
        piece.move(new_row, new_col)
        captured_square = self.all_possible_moves[piece][(new_row, new_col)]
        if isinstance(captured_square, Piece):
            self.board[captured_square.row][captured_square.col] = None
            self.pieces.remove(captured_square)
        self.board[old_row][old_col] = None
        self.board[new_row][new_col] = piece
        self._update_moves()
        self._change_turn()

    def _update_moves(self) -> None:
        self.all_possible_moves.clear()
        for row in self.board:
            for square in row:
                if isinstance(square, Piece):
                    self.pieces.add(square)
                    square.calculate_possible_moves(self.board)
                    self.all_possible_moves[square] = square.possible_moves

    def _change_turn(self) -> None:
        self.turn = abs(self.turn - 1)

    def _initialize_game(self) -> None:
        self.board = [[None for _ in range(8)] for _ in range(8)]

        for i in range(8):
            self.board[1][i], self.board[6][i] = Pawn(i, BLACK), Pawn(i, WHITE)

        self.board[0][0], self.board[0][7] = Rook(0, BLACK), Rook(7, BLACK)
        self.board[0][1], self.board[0][6] = Knight(1, BLACK), Knight(6, BLACK)
        self.board[0][2], self.board[0][5] = Bishop(2, BLACK), Bishop(5, BLACK)
        self.board[0][3], self.board[0][4] = Queen(BLACK), King(BLACK)

        self.board[7][0], self.board[7][7] = Rook(0, WHITE), Rook(7, WHITE)
        self.board[7][1], self.board[7][6] = Knight(1, WHITE), Knight(6, WHITE)
        self.board[7][2], self.board[7][5] = Bishop(2, WHITE), Bishop(5, WHITE)
        self.board[7][3], self.board[7][4] = Queen(WHITE), King(WHITE)
        self._update_moves()


class Piece:
    def __init__(self, row: int, col: int, color: int, name: str):
        self.row = row
        self.col = col
        self.color = color
        self.name = name
        self.possible_moves = dict()    # {(row, col): Piece to capture}

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def move(self, new_row: int, new_col: int) -> None:
        _check_bounds(new_row, new_col)
        if (new_row, new_col) not in self.possible_moves.keys():
            raise InvalidPositionError()

    def add_move_to_possibles(self, board: [['Piece']], row: int, col: int) -> None:
        self.possible_moves[(row, col)] = board[row][col]

    def calculate_possible_moves(self, board: [['Piece']]) -> None:
        self.possible_moves.clear()

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


class Pawn(Piece):
    def __init__(self, col: int, color: int):
        if color is WHITE:
            row = 6
            name = 'Wp{}'.format(col + 1)
        else:
            row = 1
            name = 'Bp{}'.format(8 - col)

        Piece.__init__(self, row, col, color, name)
        self.en_passant = False  # Can this piece taken by en passant?

    def move(self, new_row: int, new_col: int) -> None:
        Piece.move(self, new_row, new_col)

        if abs(new_row - self.row) == 2:
            self.en_passant = True
        else:
            self.en_passant = False

        self.row = new_row
        self.col = new_col

    def calculate_possible_moves(self, board: [[Piece]]) -> None:
        Piece.calculate_possible_moves(self, board)
        if self.color is WHITE:
            self._calculate_white_moves(board)
        else:
            self._calculate_black_moves(board)

    def _calculate_white_moves(self, board: [[Piece]]) -> None:
        if self.row == 6:   # Jumps
            if _is_space_empty(board, self.row - 1, self.col) and _is_space_empty(board, self.row - 2, self.col):
                self.add_move_to_possibles(board, self.row - 2, self.col)
        if 0 < self.row < 7:
            if _is_space_empty(board, self.row - 1, self.col):  # Pushes
                self.add_move_to_possibles(board, self.row - 1, self.col)
            if self.col != 7:   # Right Captures and En Passants
                if _is_space_occupied(board, self.row - 1, self.col + 1) and \
                        board[self.row - 1][self.col + 1].color is BLACK:   # Capture
                    self.add_move_to_possibles(board, self.row - 1, self.col + 1)
                if _is_space_occupied(board, self.row, self.col + 1) and \
                        _is_space_empty(board, self.row - 1, self.col + 1) and \
                        isinstance(board[self.row][self.col + 1], Pawn) and \
                        board[self.row][self.col + 1].color is BLACK and board[self.row][self.col + 1].en_passant:
                    self.possible_moves[(self.row - 1, self.col + 1)] = board[self.row][self.col + 1]  # En Passant
            if self.col != 0:   # Left Captures and En Passants
                if _is_space_occupied(board, self.row - 1, self.col - 1) and \
                        board[self.row - 1][self.col - 1].color is BLACK:   # Capture
                    self.add_move_to_possibles(board, self.row - 1, self.col - 1)
                if _is_space_occupied(board, self.row, self.col - 1) and \
                        _is_space_empty(board, self.row - 1, self.col - 1) and \
                        isinstance(board[self.row][self.col - 1], Pawn) and \
                        board[self.row][self.col - 1].color is BLACK and board[self.row][self.col - 1].en_passant:
                    self.possible_moves[(self.row - 1, self.col - 1)] = board[self.row][self.col - 1]  # En Passant

    def _calculate_black_moves(self, board: [[Piece]]) -> None:
        if self.row == 1:  # Jumps
            if _is_space_empty(board, self.row + 1, self.col) and _is_space_empty(board, self.row + 2, self.col):
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
                        board[self.row][self.col + 1].color is WHITE and board[self.row][self.col + 1].en_passant:
                    self.possible_moves[(self.row + 1, self.col + 1)] = board[self.row][self.col + 1]  # En Passant
            if self.col != 0:  # Left Captures and En Passants
                if _is_space_occupied(board, self.row + 1, self.col - 1) and \
                        board[self.row + 1][self.col - 1].color is WHITE:  # Capture
                    self.add_move_to_possibles(board, self.row + 1, self.col - 1)
                if _is_space_occupied(board, self.row, self.col - 1) and \
                        _is_space_empty(board, self.row + 1, self.col - 1) and \
                        isinstance(board[self.row][self.col - 1], Pawn) and \
                        board[self.row][self.col - 1].color is WHITE and board[self.row][self.col - 1].en_passant:
                    self.possible_moves[(self.row + 1, self.col - 1)] = board[self.row][self.col - 1]  # En Passant


class Knight(Piece):
    def __init__(self, col: int, color: int):
        name = ''
        if color is WHITE:
            row = 7
            if col == 1:
                name = 'Wn1'
            elif col == 6:
                name = 'Wn2'
        else:
            row = 0
            if col == 1:
                name = 'Bn2'
            elif col == 6:
                name = 'Bn1'

        Piece.__init__(self, row, col, color, name)

    def move(self, new_row: int, new_col: int) -> None:
        Piece.move(self, new_row, new_col)

        self.row = new_row
        self.col = new_col

    def calculate_possible_moves(self, board: [['Piece']]) -> None:
        Piece.calculate_possible_moves(self, board)
        possibles = {(self.row + 1, self.col - 2), (self.row - 1, self.col - 2),
                     (self.row + 1, self.col + 2), (self.row - 1, self.col + 2),
                     (self.row + 2, self.col - 1), (self.row + 2, self.col + 1),
                     (self.row - 2, self.col - 1), (self.row - 2, self.col + 1)}
        usables = set()
        for row, col in possibles:
            try:
                _check_bounds(row, col)
                if _is_space_occupied(board, row, col) and board[row][col].color == self.color:
                    raise InvalidPositionError()
            except InvalidPositionError:
                pass
            else:
                usables.add((row, col))

        for row, col in usables:
            self.add_move_to_possibles(board, row, col)


class Bishop(Piece):
    def __init__(self, col: int, color: int):
        name = ''
        if color is WHITE:
            row = 7
            if col == 2:
                name = 'Wb1'
            elif col == 5:
                name = 'Wb2'
        else:
            row = 0
            if col == 2:
                name = 'Bb2'
            elif col == 5:
                name = 'Bb1'

        Piece.__init__(self, row, col, color, name)

    def move(self, new_row: int, new_col: int) -> None:
        Piece.move(self, new_row, new_col)

        self.row = new_row
        self.col = new_col

    def calculate_possible_moves(self, board: [['Piece']]) -> None:
        Piece.calculate_possible_moves(self, board)

        if self.row > 0 and self.col < 7:
            Piece.explore_upper_right_diagonal(self, board)
        if self.row > 0 and self.col > 0:
            Piece.explore_upper_left_diagonal(self, board)
        if self.row < 7 and self.col < 7:
            Piece.explore_lower_right_diagonal(self, board)
        if self.row < 7 and self.col > 0:
            Piece.explore_lower_left_diagonal(self, board)


class Rook(Piece):
    def __init__(self, col: int, color: int):
        name = ''
        if color is WHITE:
            row = 7
            if col == 0:
                name = 'Wr1'
            elif col == 7:
                name = 'Wr2'
        else:
            row = 0
            if col == 0:
                name = 'Br2'
            elif col == 7:
                name = 'Br1'

        Piece.__init__(self, row, col, color, name)
        self.can_castle = True

    def move(self, new_row: int, new_col: int) -> None:
        Piece.move(self, new_row, new_col)

        self.row = new_row
        self.col = new_col
        self.can_castle = False

    def calculate_possible_moves(self, board: [['Piece']]) -> None:
        Piece.calculate_possible_moves(self, board)

        if self.row > 0:
            Piece.explore_up(self, board)
        if self.row < 7:
            Piece.explore_down(self, board)
        if self.col < 7:
            Piece.explore_right(self, board)
        if self.col > 0:
            Piece.explore_left(self, board)


class Queen(Piece):
    def __init__(self, color: int):
        if color is WHITE:
            row = 7
            name = 'WQu'
        else:
            row = 0
            name = 'BQu'

        Piece.__init__(self, row, 3, color, name)

    def move(self, new_row: int, new_col: int) -> None:
        Piece.move(self, new_row, new_col)

        self.row = new_row
        self.col = new_col

    def calculate_possible_moves(self, board: [['Piece']]) -> None:
        Piece.calculate_possible_moves(self, board)

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
            name = 'WKi'
        else:
            row = 0
            name = 'BKi'

        Piece.__init__(self, row, 4, color, name)
        self.can_castle = True

    def move(self, new_row: int, new_col: int) -> None:
        Piece.move(self, new_row, new_col)

        self.row = new_row
        self.col = new_col
        self.can_castle = False

    def calculate_possible_moves(self, board: [['Piece']]) -> None:
        Piece.calculate_possible_moves(self, board)
        possibles = {(self.row + 1, self.col - 1), (self.row - 1, self.col - 1),
                     (self.row + 1, self.col + 1), (self.row - 1, self.col + 1),
                     (self.row, self.col - 1), (self.row, self.col + 1),
                     (self.row - 1, self.col), (self.row + 1, self.col)}
        usables = set()
        for row, col in possibles:
            try:
                _check_bounds(row, col)
                if _is_space_occupied(board, row, col) and board[row][col].color == self.color:
                    raise InvalidPositionError()
            except InvalidPositionError:
                pass
            else:
                usables.add((row, col))

        for row, col in usables:
            self.add_move_to_possibles(board, row, col)


def _check_bounds(row: int, col: int) -> None:
    if row not in range(8) or col not in range(8):
        raise InvalidPositionError()


def _is_space_occupied(board: [[Piece]], row: int, col: int) -> bool:
    return isinstance(board[row][col], Piece)


def _is_space_empty(board: [[Piece]], row: int, col: int) -> bool:
    return not _is_space_occupied(board, row, col)
