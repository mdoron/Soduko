import copy
import hashlib

from consts import *
from inlay import Inlay
from string_builder import StringBuilder


class SodukoBoard:
    def __init__(self, array=None):
        self.board = []
        self.empty_inlays = set([])

        if array is not None:
            self.board = copy.deepcopy(array)
            for i in range(0, BOARD_SIZE):
                for j in range(0, BOARD_SIZE):
                    self.set_inlay(i, j, array[i][j])
                    if self.get_inlay(i, j).is_empty():
                        self.empty_inlays.add(self.get_inlay(i, j))

            for i in range(0, BOARD_SIZE):
                for j in range(0, BOARD_SIZE):
                    self.get_inlay(i, j).set_options(self._init_options(i, j))

    def __deepcopy__(self, memodict={}):
        new = SodukoBoard()
        new.empty_inlays = set([])
        for i in range(0, BOARD_SIZE):
            new.board.append([])
            for j in range(0, BOARD_SIZE):
                new.board[i].append(copy.deepcopy(self.get_inlay(i, j)))

                if new.get_inlay(i, j).is_empty():
                    new.empty_inlays.add(new.get_inlay(i, j))
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
        for i in range(0, BOARD_SIZE):
            for j in range(0, BOARD_SIZE):
                if i == x and j == y:
                    sb += "[*{0}*] {1}".format(
                        self.get_inlay(i, j).get() if not self.get_inlay(i, j).is_empty() else "",
                        set_str(self.get_inlay(i, j).get_options()))
                else:
                    sb += "[{0}] {1}".format(self.get_inlay(i, j).get() if not self.get_inlay(i, j).is_empty() else "",
                                             set_str(self.get_inlay(i, j).get_options()))
                    sb += "\t\t\t"

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

    def update_area(self, inlay):
        for i in range(0, SQUARE_SIZE):
            for j in range(0, SQUARE_SIZE):
                self.get_inlay(int(inlay.x / SQUARE_SIZE) * SQUARE_SIZE + i,
                               int(inlay.y / SQUARE_SIZE) * SQUARE_SIZE + j).remove_option(inlay.get())

    def update_row(self, inlay):
        for j in range(0, BOARD_SIZE):
            self.get_inlay(inlay.x, j).remove_option(inlay.get())

    def update_col(self, inlay):
        for i in range(0, BOARD_SIZE):
            self.get_inlay(i, inlay.y).remove_option(inlay.get())

    def update_inlay(self, inlay):
        self.get_inlay(inlay.x, inlay.y).set_options_empty()

    def update_diff(self, inlay):
        self.update_inlay(inlay)
        self.update_col(inlay)
        self.update_row(inlay)
        self.update_area(inlay)

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

    def _init_options(self, x, y):
        all_values = set(range(1, 10))
        possible_values = set()
        if self.get_inlay(x, y).get() is not None:
            return set()

        for i in range(0, BOARD_SIZE):
            val = self.get_inlay(i, y).get()
            if val is None:
                continue
            possible_values.add(val)

        for j in range(0, BOARD_SIZE):
            val = self.get_inlay(x, j).get()
            if val is None:
                continue
            possible_values.add(val)

        for i in range(0, SQUARE_SIZE):
            for j in range(0, SQUARE_SIZE):
                val = self.get_inlay(int(x / SQUARE_SIZE) * SQUARE_SIZE + i,
                                     int(y / SQUARE_SIZE) * SQUARE_SIZE + j).get()
                if val is None:
                    continue
                possible_values.add(val)

        return all_values.difference(possible_values)

    def get_empty_inlays(self):
        return self.empty_inlays
