class Board:
    def __init__(self, size: int, grid_data: list):
        self.size = size  # Grid side length
        # self.grid = [[0] * size for _ in range(size)]  # Init grid with 0s
        self.grid = grid_data

    def __str__(self):  # Text representation of board cells.
        return '\n'.join([' '.join(map(str, row)) for row in self.grid])

    def row(self, y):  # Get row
        return self.grid[y]

    def column(self, x):  # Get column
        return [self.grid[row][x] for row in range(self.size)]

    def sector(self, x, y):  # Get 3х3 sector, which includes provided coords
        sect_x_left = x - x % 3  # Left edge
        sect_y_top = y - y % 3  # Top edge
        result = []
        for y in range(sect_y_top, sect_y_top + 3):  # Iterate rows of the sector
            result += self.grid[y][sect_x_left:sect_x_left + 3]  # concatenate sub-lists of each row
        return result

    def coords_are_valid(self, y, x):  # Are this coordinates within the board?
        return (y in range(self.size)) and (x in range(self.size))

    def next_cell(self, y, x):  # traverse board row-by-row
        index = (y * self.size) + x  # Absolute index of current y, x coords
        return divmod(index + 1, self.size)  # y, x coords of the next (+1) index


class SudokuSolver:
    def __init__(self, board: Board):
        self.board = board
        self.status = None  # None/True/False, see self.status_repr for description

    @property
    def status_repr(self):  # Text representation of solver status
        if self.status is None:
            return 'Board is not solved yet.'
        elif self.status is False:
            return 'Board cannot be solved.'
        elif self.status is True:
            return 'Board solved successfully.'

    def is_valid_to_place(self, y, x, val):  # True if value not in current row/column/sector and thus can be placed in the cell
        return val not in self.board.row(y) \
               and val not in self.board.column(x) \
               and val not in self.board.sector(x, y)

    def solve(self):  # Solve board and update solution status
        self.status = self.solve_backtracking()

    def solve_backtracking(self, y=0, x=0):  # https://en.wikipedia.org/wiki/Sudoku_solving_algorithms#Backtracking
        if not self.board.coords_are_valid(y, x):  # Exit case. We're out of bounds, e.g. all the cells are processed successfully
            return True  # Success! Decision found.

        if self.board.grid[y][x] != 0:  # If current cell is occupied...
            return self.solve_backtracking(*self.board.next_cell(y, x))  # skip it and process next cell

        for num in range(1, 10):  # Try each number for current empty cell
            if self.is_valid_to_place(y, x, num):  # If number is eligible...
                self.board.grid[y][x] = num  # place it in current cell and...
                if self.solve_backtracking(*self.board.next_cell(y, x)):  # try to resolve subsequent cells. If we managed to solve all of them...
                    return True  # then we're done. Success.
            self.board.grid[y][x] = 0  # Otherwise, the board cannot be solved with current number - clear the cell (and pick next number in "for" loop)
        return False  # If we tried each number for current cell and still have no decision return to previous cell (or ultimately exit recursion with False result).
