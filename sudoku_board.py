import copy
import hashlib

from board_checker import BoardChecker
from consts import *
from inlay import Inlay
from string_builder import StringBuilder


class SodukoBoard:
    def __init__(self, array=None):
        self.board = []
        self.rows = [dict.fromkeys(SQUARE_OPTIONS) for _ in BOARD_INDICES]
        self.cols = [dict.fromkeys(SQUARE_OPTIONS) for _ in BOARD_INDICES]
        self.areas = [dict.fromkeys(SQUARE_OPTIONS) for _ in BOARD_INDICES]

        for i in range(0, BOARD_SIZE):
            for j in SQUARE_OPTIONS:
                self.rows[i][j], self.cols[i][j], self.areas[i][j] = set([]), set([]), set([])

        self.lonely_options = set([])
        self.empty_inlays = set([])

        if array:
            self.board = copy.deepcopy(array)
            for i in range(0, BOARD_SIZE):
                for j in range(0, BOARD_SIZE):
                    self.set_inlay(i, j, array[i][j])
                    if self.get_inlay(i, j).is_empty():
                        self.empty_inlays.add(self.get_inlay(i, j))

            for i in range(0, BOARD_SIZE):
                for j in range(0, BOARD_SIZE):
                    self.get_inlay(i, j).set_options(self._init_options(i, j))
                    self._add_to_structures(self.get_inlay(i, j))

            self._get_lonely_options()
        pass

    def __deepcopy__(self, memodict={}):
        new = SodukoBoard()
        new.empty_inlays = set([])
        for i in range(0, BOARD_SIZE):
            new.board.append([])
            for j in range(0, BOARD_SIZE):
                new.board[i].append(copy.deepcopy(self.get_inlay(i, j)))

                if new.get_inlay(i, j).is_empty():
                    new.empty_inlays.add(new.get_inlay(i, j))

        for i in range(0, BOARD_SIZE):
            for j in range(0, BOARD_SIZE):
                new.get_inlay(i, j).set_options(new._init_options(i, j))
                new._add_to_structures(new.get_inlay(i, j))

        new._get_lonely_options()

        return new

    def _str_helper(self):
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
            if i % 3 == 0:
                sb += "=====================\n"
            for j in range(0, BOARD_SIZE):
                if j == 3 or j == 6:
                    sb += "| "
                sb += "{0}".format(self.get_inlay(i, j).get() if not self.get_inlay(i, j).is_empty() else " ",
                                   set_str(self.get_inlay(i, j).get_options()))
                sb += " "
            sb += "\n"

        return str(sb)

    def __str__(self):
        return self._str_helper()

    def __hash__(self):
        return hashlib.md5(str(self))

    def show(self):
        print(self._str_helper())

    def why_stuck(self):
        for inlay in copy.deepcopy(self.get_empty_inlays()):
            if len(inlay.get_options()) == 0:
                return inlay
        return None

    def is_stuck(self):
        for inlay in copy.deepcopy(self.get_empty_inlays()):
            if len(inlay.get_options()) == 0:
                return True
        return not BoardChecker(self).can_continue()

    def _update_area_options(self, inlay):
        for i in range(0, SQUARE_SIZE):
            for j in range(0, SQUARE_SIZE):
                self.get_inlay(int(inlay.x / SQUARE_SIZE) * SQUARE_SIZE + i,
                               int(inlay.y / SQUARE_SIZE) * SQUARE_SIZE + j).remove_option(inlay.get())

    def _update_row_options(self, inlay):
        for j in range(0, BOARD_SIZE):
            self.get_inlay(inlay.x, j).remove_option(inlay.get())

    def _update_col_options(self, inlay):
        for i in range(0, BOARD_SIZE):
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
                if not value:
                    self.empty_inlays.add(inlay)
                else:
                    self.empty_inlays.remove(inlay)
        except KeyError:
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
        return int(x / SQUARE_SIZE) * SQUARE_SIZE, int(y / SQUARE_SIZE) * SQUARE_SIZE

    def get_area(self, x, y):
        """
        0 0 => 0
        0 3 => 1
        0 6 => 2
        ...
        6 6 => 8
        """
        ax, ay = self._get_area_coordinates(x, y)
        return self.areas[ax + int(ay / SQUARE_SIZE)]

    def _init_options(self, x, y):
        all_values = set(SQUARE_OPTIONS)
        possible_values = set()
        if self.get_inlay(x, y).get():
            return set()

        for i in range(0, BOARD_SIZE):
            val = self.get_inlay(i, y).get()
            if not val:
                continue
            possible_values.add(val)

        for j in range(0, BOARD_SIZE):
            val = self.get_inlay(x, j).get()
            if not val:
                continue
            possible_values.add(val)

        for i in range(0, SQUARE_SIZE):
            for j in range(0, SQUARE_SIZE):
                val = self.get_inlay(int(x / SQUARE_SIZE) * SQUARE_SIZE + i,
                                     int(y / SQUARE_SIZE) * SQUARE_SIZE + j).get()
                if not val:
                    continue
                possible_values.add(val)

        return all_values.difference(possible_values)

    def _add_to_structures(self, inlay):
        if not inlay or inlay.value or not inlay.options:
            return

        for op in inlay.options:
            self.get_row(inlay.x)[op].add(inlay)
            self.get_col(inlay.y)[op].add(inlay)
            self.get_area(inlay.x, inlay.y)[op].add(inlay)

    def _remove_from_structures(self, inlay):
        if not inlay or not inlay.value:
            return

        row, col, area = self.get_row(inlay.x), self.get_col(inlay.y), self.get_area(inlay.x, inlay.y)

        row[inlay.value] = set()
        col[inlay.value] = set()
        area[inlay.value] = set()

        for op in inlay.options:
            try:
                row[op].remove(inlay)
            except KeyError:
                pass
            try:
                col[op].remove(inlay)
            except KeyError:
                pass
            try:
                area[op].remove(inlay)
            except KeyError:
                pass

            if len(row[op]) == 1:
                self.lonely_options.add((op, row[op].pop()))

            if len(col[op]) == 1:
                self.lonely_options.add((op, col[op].pop()))

            if len(area[op]) == 1:
                self.lonely_options.add((op, area[op].pop()))

        for i in range(0, BOARD_SIZE, int(BOARD_SIZE / SQUARE_SIZE)):
            for j in SQUARE_INDICES:
                try:
                    self.get_area(inlay.x, i)[inlay.value].remove(Inlay(inlay.x, i + j))
                    if len(self.get_area(inlay.x, i)[inlay.value]) == 1:
                        self.lonely_options.add((inlay.value, self.get_area(inlay.x, i)[inlay.value].pop()))
                except KeyError:
                    pass

                try:
                    self.get_area(i, inlay.y)[inlay.value].remove(Inlay(i + j, inlay.y))
                    if len(self.get_area(i, inlay.y)[inlay.value]) == 1:
                        self.lonely_options.add((inlay.value, self.get_area(i, inlay.y)[inlay.value].pop()))
                except KeyError:
                    pass

        for i in SQUARE_INDICES:
            for j in SQUARE_INDICES:
                affected_x_base, affected_y_base = self._get_area_coordinates(inlay.x, inlay.y)
                try:
                    self.get_row(affected_x_base + i)[inlay.value].remove(Inlay(affected_x_base + i, affected_y_base + j))
                except KeyError:
                    pass
                try:
                    self.get_col(affected_y_base + i)[inlay.value].remove(Inlay(affected_x_base + i, affected_y_base + j))
                    if len(self.get_col(affected_y_base + i)[inlay.value]) == 1:
                        self.lonely_options.add((inlay.value, self.get_col(affected_y_base + i)[inlay.value].pop()))
                except KeyError:
                    pass
        for i in SQUARE_INDICES:
            affected_x_base, affected_y_base = self._get_area_coordinates(inlay.x, inlay.y)
            if len(self.get_row(affected_x_base + i)[inlay.value]) == 1:
                self.lonely_options.add((inlay.value, self.get_row(affected_x_base + i)[inlay.value].pop()))
            if len(self.get_col(affected_y_base + i)[inlay.value]) == 1:
                self.lonely_options.add((inlay.value, self.get_col(affected_y_base + i)[inlay.value].pop()))

    def _get_lonely_options(self):
        for i in BOARD_INDICES:
            for j in SQUARE_OPTIONS:
                if len(self.rows[i][j]) == 1:
                    self.lonely_options.add((j, self.rows[i][j].pop()))

        for i in BOARD_INDICES:
            for j in SQUARE_OPTIONS:
                if len(self.cols[i][j]) == 1:
                    self.lonely_options.add((j, self.cols[i][j].pop()))

        for i in BOARD_INDICES:
            for j in SQUARE_OPTIONS:
                if len(self.areas[i][j]) == 1:
                    self.lonely_options.add((j, self.areas[i][j].pop()))

    def get_empty_inlays(self):
        return self.empty_inlays
