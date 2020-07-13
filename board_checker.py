from functools import reduce

from consts import *


class BoardChecker:
    def __init__(self, board):
        self.board = board

    def check_square(self, x, y):
        hist = [0] * SQUARE_SIZE * SQUARE_SIZE
        for i in range(0, SQUARE_SIZE):
            for j in range(0, SQUARE_SIZE):
                val = self.board.get_inlay(x + i, y + j)
                if val.is_empty():
                    continue
                hist[val.get() - 1] = hist[val.get() - 1] + 1
                if hist[val.get() - 1] > 1:
                    return False
        return True

    def check_all_inlays(self):
        return reduce(lambda x, y: x and y,
                      map(self.check_square, [0, 0, 0, SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE, 6, 6, 6],
                          [0, SQUARE_SIZE, 6, 0, SQUARE_SIZE, 6, 0, SQUARE_SIZE, 6]))

    def check_row(self, r):
        hist = [0] * BOARD_SIZE
        for j in range(0, SQUARE_SIZE):
            val = self.board.get_inlay(r, j)
            if val.is_empty():
                continue
            hist[val.get() - 1] = hist[val.get() - 1] + 1
            if hist[val.get() - 1] > 1:
                return False
        return True

    def check_all_rows(self):
        return reduce(lambda x, y: x and y, map(self.check_row, range(0, BOARD_SIZE)))

    def check_col(self, c):
        hist = [0] * BOARD_SIZE
        for i in range(0, BOARD_SIZE):
            val = self.board.get_inlay(i, c)
            if val.is_empty():
                continue
            hist[val.get() - 1] = hist[val.get() - 1] + 1
            if hist[val.get() - 1] > 1:
                return False

        return True

    def check_diff(self, x, y):
        # TODO: Check if no more options and inlay is empty
        return self.check_col(y) and self.check_row(x) and self.check_square(int(x / SQUARE_SIZE) * SQUARE_SIZE,
                                                                             int(y / SQUARE_SIZE) * SQUARE_SIZE)

    def check_all_cols(self):
        return reduce(lambda x, y: x and y, map(self.check_col, range(0, BOARD_SIZE)))

    def can_continue(self):
        return self.check_all_cols() and self.check_all_rows() and self.check_all_inlays()
