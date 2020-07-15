import copy
import hashlib

from consts import *
from inlay import Inlay
from string_builder import StringBuilder


class SodukoBoard:
    def __init__(self, array=None, square_size=SQUARE_SIZE, board_size=BOARD_SIZE):
        self.square_size = square_size
        self.board_size = board_size
        self.board = []
        self.rows = [dict.fromkeys(range(1, 10)) for _ in range(self.board_size)]
        self.cols = [dict.fromkeys(range(1, 10)) for _ in range(self.board_size)]
        self.areas = [dict.fromkeys(range(1, 10)) for _ in range(self.board_size)]

        for i in range(0, 9):
            for j in range(1, 10):
                self.rows[i][j], self.cols[i][j], self.areas[i][j] = [], [], []

        self.lonely_options = set([])
        self.empty_inlays = set([])

        if array is not None:
            self.board = copy.deepcopy(array)
            for i in range(0, self.board_size):
                for j in range(0, self.board_size):
                    self.set_inlay(i, j, array[i][j])
                    if self.get_inlay(i, j).is_empty():
                        self.empty_inlays.add(self.get_inlay(i, j))

            for i in range(0, self.board_size):
                for j in range(0, self.board_size):
                    self.get_inlay(i, j).set_options(self._init_options(i, j))
                    self._add_to_structures(self.get_inlay(i, j))

            self._get_lonely_options()
        pass

    def __deepcopy__(self, memodict={}):
        new = SodukoBoard()
        new.empty_inlays = set([])
        for i in range(0, self.board_size):
            new.board.append([])
            for j in range(0, self.board_size):
                new.board[i].append(copy.deepcopy(self.get_inlay(i, j)))

                if new.get_inlay(i, j).is_empty():
                    new.empty_inlays.add(new.get_inlay(i, j))

        new.rows = copy.deepcopy(self.rows)
        new.cols = copy.deepcopy(self.cols)
        new.areas = copy.deepcopy(self.areas)
        new.lonely_options = copy.deepcopy(self.lonely_options)

        return new

    def _str_helper(self, x, y):
        def set_str(s):
            ops = list(s)
            sb = StringBuilder("{")
            for i in range(0, len(ops) - 1):
                sb += str(ops[i])
                sb += ", "
            if len(ops) > 0:
                sb += str(ops[-1])
            sb += "}"
            return str(sb)

        sb = StringBuilder()
        if False:  # DEBUG:
            for i in range(0, self.board_size):
                for k in range(2):
                    for j in range(0, self.board_size):
                            if k == 0:
                                if i == x and j == y:
                                    sb += "[*{0}*]".format(
                                        self.get_inlay(i, j).get() if not self.get_inlay(i, j).is_empty() else "")
                                else:
                                    sb += "[{0}]".format(
                                        self.get_inlay(i, j).get() if not self.get_inlay(i, j).is_empty() else "")
                                    sb += "\t"
                            if k == 1:
                                sb += "{0}".format(set_str(self.get_inlay(i, j).get_options()))
                                sb += "\t"
                    sb += "\n"
        else:
            for i in range(0, self.board_size):
                if i % 3 == 0:
                    sb += "=====================\n"
                for j in range(0, self.board_size):
                    if j == 3 or j == 6:
                        sb += "| "
                    sb += "{0}".format(self.get_inlay(i, j).get() if not self.get_inlay(i, j).is_empty() else " ",
                                             set_str(self.get_inlay(i, j).get_options()))
                    sb += " "
                sb += "\n"

        return str(sb)

    def __str__(self):
        return self._str_helper(-1, -1)

    def __hash__(self):
        return hashlib.md5(str(self))

    def show(self, x=-1, y=-1):
        print(self._str_helper(x, y))

    def is_stucked(self):
        for inlay in copy.deepcopy(self.get_empty_inlays()):
            if len(inlay.get_options()) == 0:
                return True
        return False

    def _update_area_options(self, inlay):
        for i in range(0, self.square_size):
            for j in range(0, self.square_size):
                self.get_inlay(int(inlay.x / self.square_size) * self.square_size + i,
                               int(inlay.y / self.square_size) * self.square_size + j).remove_option(inlay.get())

    def _update_row_options(self, inlay):
        for j in range(0, self.board_size):
            self.get_inlay(inlay.x, j).remove_option(inlay.get())

    def _update_col_options(self, inlay):
        for i in range(0, self.board_size):
            self.get_inlay(i, inlay.y).remove_option(inlay.get())

    def _update_inlay_options(self, inlay):
        self.get_inlay(inlay.x, inlay.y).set_options_empty()

    def update_diff_options(self, inlay):
        self._remove_from_structures(inlay)
        self._update_inlay_options(inlay)
        self._update_col_options(inlay)
        self._update_row_options(inlay)
        self._update_area_options(inlay)

    def unset_inlay(self, x, y):
        self.get_inlay(x, y).unset()
        self.set_inlay(x, y, None)

    def set_inlay(self, x, y, value):
        try:
            inlay = self.get_inlay(x, y)
            if type(inlay) is not Inlay:
                self.board[x][y] = Inlay(x, y, value)
            else:
                inlay.set(value)
                if value is None:
                    self.empty_inlays.add(inlay)
                else:
                    self.empty_inlays.remove(inlay)
        except KeyError:  # TODO: Why do we even get here?
            pass

    def get_inlay(self, x, y):
        return self.board[x][y]

    def is_full(self):
        return len(self.get_empty_inlays()) == 0

    def get_row(self, x):
        return self.rows[x]

    def get_col(self, y):
        return self.cols[y]

    def _get_area_coordinates(self, x, y):
        return int(x / self.square_size) * self.square_size, int(y / self.square_size) * self.square_size

    def get_area(self, x, y):
        """
        0 0 => 0
        0 3 => 1
        0 6 => 2
        ...
        6 6 => 8
        """
        ax, ay = self._get_area_coordinates(x, y)
        return self.areas[ax + int(ay / self.square_size)]

    def _init_options(self, x, y):
        all_values = set(range(1, 10))
        possible_values = set()
        if self.get_inlay(x, y).get() is not None:
            return set()

        for i in range(0, self.board_size):
            val = self.get_inlay(i, y).get()
            if val is None:
                continue
            possible_values.add(val)

        for j in range(0, self.board_size):
            val = self.get_inlay(x, j).get()
            if val is None:
                continue
            possible_values.add(val)

        for i in range(0, self.square_size):
            for j in range(0, self.square_size):
                val = self.get_inlay(int(x / self.square_size) * self.square_size + i,
                                     int(y / self.square_size) * self.square_size + j).get()
                if val is None:
                    continue
                possible_values.add(val)

        return all_values.difference(possible_values)

    def _add_to_structures(self, inlay):
        if inlay is None or inlay.value is not None or inlay.options is None:
            return

        for op in inlay.options:
            self.get_row(inlay.x)[op].append(inlay)
            self.get_col(inlay.y)[op].append(inlay)
            self.get_area(inlay.x, inlay.y)[op].append(inlay)

    def _remove_from_structures(self, inlay):
        if inlay is None:
            return

        row, col, area = self.get_row(inlay.x), self.get_col(inlay.y), self.get_area(inlay.x, inlay.y)

        for op in inlay.options:
            try:
                row[op].remove(inlay)
                col[op].remove(inlay)
                area[op].remove(inlay)
            except ValueError:
                pass

            if inlay.value == op:
                row[op] = []
                col[op] = []
                area[op] = []

            if len(row[op]) == 1:
                self.lonely_options.add((op, row[op][0]))

            if len(col[op]) == 1:
                self.lonely_options.add((op, col[op][0]))

            if len(area[op]) == 1:
                self.lonely_options.add((op, area[op][0]))

    def _get_lonely_options(self):
        for i in range(self.board_size):
            for j in range(1, 10):
                if len(self.rows[i][j]) == 1:
                    self.lonely_options.add((j, self.rows[i][j][0]))

        for i in range(self.board_size):
            for j in range(1, 10):
                if len(self.cols[i][j]) == 1:
                    self.lonely_options.add((j, self.cols[i][j][0]))

        for i in range(self.board_size):
            for j in range(1, 10):
                if len(self.areas[i][j]) == 1:
                    self.lonely_options.add((j, self.areas[i][j][0]))

    def get_empty_inlays(self):
        return self.empty_inlays
