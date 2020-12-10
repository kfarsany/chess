# Kian Farsany
# Chess
# Classes for Pieces

WHITE = 1
BLACK = 0


class InvalidPositionError(Exception):
    pass


class Piece:
    def __init__(self, row: int, col: int, color: int, name: str):
        self.row = row
        self.col = col
        self.color = color
        self.name = name
        self.alive = True

    def die(self):
        self.alive = False
        self.row = -1
        self.col = -1


class Pawn(Piece):
    def __init__(self, col: int, color: int):
        if color is WHITE:
            row = 6
            name = 'Wp{}'.format(col+1)
        else:
            row = 1
            name = 'Bp{}'.format(8-col)

        Piece.__init__(self, row, col, color, name)
        self.en_passant = False  # Can this piece taken by en passant?

    def move(self, new_row: int, new_col: int) -> None:
        _check_bounds(new_row, new_col)

        if new_col - self.col not in {-1, 0, 1}:
            raise InvalidPositionError()

        row_change = new_row - self.row
        if self.color is WHITE:
            if row_change not in {-1, -2}:
                raise InvalidPositionError()
            if row_change == -2:
                if self.row != 6:
                    raise InvalidPositionError()
                self.en_passant = True
        else:
            if row_change not in {1, 2}:
                raise InvalidPositionError()
            if row_change == 2:
                if self.row != 1:
                    raise InvalidPositionError()
                self.en_passant = True

        self.row = new_row
        self.col = new_col


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
        _check_bounds(new_row, new_col)

        row_change, col_change = _calc_row_col_changes(self, new_row, new_col)
        if abs(row_change) not in {1, 2} or abs(col_change) not in {1, 2}:
            raise InvalidPositionError()
        if abs(row_change) == abs(col_change):
            raise InvalidPositionError()

        self.row = new_row
        self.col = new_col


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
        _check_bounds(new_row, new_col)

        row_change, col_change = _calc_row_col_changes(self, new_row, new_col)
        if row_change == 0 or col_change == 0:
            raise InvalidPositionError()
        if abs(row_change) != abs(col_change):
            raise InvalidPositionError()

        self.row = new_row
        self.col = new_col


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

    def move(self, new_row: int, new_col: int) -> None:
        _check_bounds(new_row, new_col)

        row_change, col_change = _calc_row_col_changes(self, new_row, new_col)
        if row_change == 0 and col_change == 0:
            raise InvalidPositionError()
        if row_change != 0 and col_change != 0:
            raise InvalidPositionError()

        self.row = new_row
        self.col = new_col


class Queen(Piece):
    def __init__(self, color: int):
        if color is WHITE:
            row = 7
            name = 'W-Q'
        else:
            row = 0
            name = 'B-Q'

        Piece.__init__(self, row, 4, color, name)

    def move(self, new_row: int, new_col: int) -> None:
        _check_bounds(new_row, new_col)

        row_change, col_change = _calc_row_col_changes(self, new_row, new_col)
        if row_change == 0 and col_change == 0:
            raise InvalidPositionError()
        if (abs(row_change) != abs(col_change)) and (row_change != 0 and col_change != 0):
            raise InvalidPositionError()


class King(Piece):
    def __init__(self, color: int):
        if color is WHITE:
            row = 7
            name = 'W-K'
        else:
            row = 0
            name = 'B-K'

        Piece.__init__(self, row, 4, color, name)

    def move(self, new_row: int, new_col: int) -> None:
        _check_bounds(new_row, new_col)

        row_change, col_change = _calc_row_col_changes(self, new_row, new_col)
        if row_change == 0 and col_change == 0:
            raise InvalidPositionError()
        if abs(row_change) > 1 or abs(col_change) > 1:
            raise InvalidPositionError()

        self.row = new_row
        self.col = new_col


def _calc_row_col_changes(piece: Piece, new_row: int, new_col: int) -> (int, int):
    return new_row - piece.row, new_col - piece.col


def _check_bounds(row: int, col: int):
    if row not in range(8) or col not in range(8):
        raise InvalidPositionError()
