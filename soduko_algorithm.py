import copy
from random import shuffle

from consts import *
from string_builder import StringBuilder


class TooManyComputationsException(Exception):
    pass


class SodukoAlgorithm:
    """
    Implementation of the algorithm to solve a Soduko board
    """

    def __init__(self, initial_board, maxdepth, maxcomps):
        self.found = False
        self.max_depth = None
        self.loot_times = 0
        self.guess_times = 0
        self.iterations = 0
        self.max_loot_times = maxcomps
        self.max_guess_times = maxcomps
        self.max_iterations = 10
        self.max_comps = maxcomps
        self.max_depth = maxdepth
        self.initial_board = initial_board
        self.working_board = None
        self.steps = []

    def solve(self):
        res_board = None
        iterations = 0
        while True:
            try:
                if LOG: print("[*] Iteration # {}".format(iterations))
                iterations += 1
                # self.max_depth = randint(1, 20)
                # if iterations % 1 == 0:
                #     self.max_loot_times += 1000
                #     self.max_guess_times += 1000
                self.loot_times = 0
                self.guess_times = 0
                if LOG: print("[*]\tNew max depth is {}".format(self.max_depth))
                if LOG: print("[*]\tNew max_loot_times={}, max_guess_times={}".format(self.max_loot_times,
                                                                                      self.max_guess_times))
                res_board = self.aux_solve(copy.deepcopy(self.initial_board), -1, -1, self.max_depth)
            except TooManyComputationsException:
                if LOG: print("[*]\tToo many computations with max_depth={}".format(self.max_depth))

            if res_board is not None:
                print("[*]\tDone")
                break
            else:
                if LOG: print(
                    "[*]\tNo solution with max_depth={}, max_loot_times={}, max_guess_times={}".format(self.max_depth,
                                                                                                       self.max_loot_times,
                                                                                                       self.max_guess_times))
        return res_board

    def loot(self, board):
        if board.is_stucked():
            return None

        self.x = 1
        for area in board.areas:
            for i in range(1, board.board_size + 1):
                if len(area[i]) != 2:
                    continue
                for j in range(i + 1, board.board_size + 1):
                    if area[i] == area[j]:
                        for inlay in area[i]:
                            binlay = board.get_inlay(inlay.x, inlay.y)
                            for op in binlay.options.difference({i, j}):
                                try:
                                    if LOG: print("[*]\tRemoving option {} from [{}, {}]".format(op, binlay.x, binlay.y))
                                    area[op].remove(binlay)
                                    binlay.remove_option(op)
                                    inlay.remove_option(op)
                                    if len(area[op]) == 1:
                                        board.lonely_options.add((op, area[op].pop()))
                                except KeyError:
                                    if LOG: print("[*]\tNo options to remove")
        for row in board.rows:
            for i in range(1, board.board_size + 1):
                if len(row[i]) != 2:
                    continue
                for j in range(i + 1, board.board_size + 1):
                    if row[i] == row[j]:
                        for inlay in row[i]:
                            binlay = board.get_inlay(inlay.x, inlay.y)
                            for op in binlay.options.difference({i, j}):
                                try:
                                    if LOG: print("[*]\tRemoving option {} from [{}, {}]".format(op, binlay.x, binlay.y))
                                    row[op].remove(binlay)
                                    binlay.remove_option(op)
                                    inlay.remove_option(op)
                                    if len(row[op]) == 1:
                                        board.lonely_options.add((op, row[op].pop()))
                                except KeyError:
                                    if LOG: print("[*]\tNo options to remove")

        for col in board.cols:
            for i in range(1, board.board_size + 1):
                if len(col[i]) != 2:
                    continue
                for j in range(i + 1, board.board_size + 1):
                    if col[i] == col[j]:
                        for inlay in col[i]:
                            binlay = board.get_inlay(inlay.x, inlay.y)
                            for op in binlay.options.difference({i, j}):
                                try:
                                    if LOG: print("[*]\tRemoving option {} from [{}, {}]".format(op, binlay.x, binlay.y))
                                    col[op].remove(binlay)
                                    binlay.remove_option(op)
                                    inlay.remove_option(op)
                                    if len(col[op]) == 1:
                                        board.lonely_options.add((op, col[op].pop()))
                                except KeyError:
                                    if LOG: print("[*]\tNo options to remove")

        self.x = 1
        for area in board.areas:
            for i in range(1, board.board_size + 1):
                if len(area[i]) != 3:
                    continue
                for j in range(i + 1, board.board_size + 1):
                    if area[i] == area[j]:
                        for l in range(j + 1, board.board_size + 1):
                            if area[i] == area[l]:
                                for inlay in area[i]:
                                    binlay = board.get_inlay(inlay.x, inlay.y)
                                    for op in binlay.options.difference({i, j, l}):
                                        try:
                                            if LOG: print("[*]\t\t\tRemoving option {} from [{}, {}]".format(op, binlay.x, binlay.y))
                                            area[op].remove(binlay)
                                            binlay.remove_option(op)
                                            inlay.remove_option(op)
                                            if len(area[op]) == 1:
                                                board.lonely_options.add((op, area[op].pop()))
                                        except KeyError:
                                            if LOG: print("[*]\t\tNo options to remove")


        self.loot_times += 1
        for inlay in copy.deepcopy(board.get_empty_inlays()):
            if len(inlay.get_options()) == 1:

                try:
                    board.set_inlay(inlay.x, inlay.y, inlay.get_options().pop())
                    if DEBUG: print(
                        "[*] T: [{}, {}] = {}".format(inlay.x, inlay.y, board.get_inlay(inlay.x, inlay.y).value))
                except KeyError:
                    continue
                board.update_diff_options(board.get_inlay(inlay.x, inlay.y))
                if board.is_stucked():
                    return None
        self.x = 1
        for op, inlay in copy.deepcopy(board.lonely_options):
            board.set_inlay(inlay.x, inlay.y, op)
            if DEBUG: print("[*] M: [{}, {}] = {}".format(inlay.x + 1, inlay.y + 1, op))

            board.update_diff_options(board.get_inlay(inlay.x, inlay.y))
            board.lonely_options.remove((op, inlay))
            if board.is_stucked():
                return None

        return board

    def loot_loop(self, board):
        if board.is_stucked():
            return None
        # BFS loop
        board_empty_count = len(board.get_empty_inlays())
        looted_board = self.loot(board)
        if looted_board is None:
            if DEBUG: print("[*] S")
            return None
        while looted_board is not None and (not board.is_full() and
                board_empty_count > len(looted_board.get_empty_inlays()) or len(looted_board.lonely_options) != 0):
            board_empty_count = len(looted_board.get_empty_inlays())
            looted_board = self.loot(looted_board)

        return looted_board

    def aux_solve(self, board, x, y, depth):
        if board.is_stucked():
            if DEBUG: print("[*] S")
            return None

        looted_board = self.loot_loop(board)
        if looted_board is None:
            if DEBUG: print("[*] S")
            return None

        if looted_board.is_full():
            if DEBUG: looted_board.show(x, y)
            return looted_board

        if self.loot_times >= self.max_loot_times and self.guess_times >= self.max_guess_times:
            if DEBUG: print("[*] S")
            raise TooManyComputationsException

        if depth <= 0:
            if DEBUG: print("[*] S")
            return None

        # Prepare for guessing
        empty_inlays = list(looted_board.get_empty_inlays())
        empty_inlays.sort(key=lambda x: len(x.get_options()))

        # DFS loop
        eis = list(range(len(empty_inlays)))
        if RANDOMIZE:
            shuffle(eis)

        for ei in eis:
            inlay = empty_inlays[ei]
            new_board = copy.deepcopy(looted_board)
            options = list(copy.deepcopy(inlay.get_options()))
            if RANDOMIZE:
                shuffle(options)

            for op in options:
                self.guess_times += 1
                new_board.set_inlay(inlay.x, inlay.y, op)
                new_board.update_diff_options(new_board.get_inlay(inlay.x, inlay.y))
                if DEBUG: print("[*] G: [{}, {}]{} = {}".format(inlay.x + 1, inlay.y + 1, inlay.options, op))
                if LOG: print("[*]\tDepth is " + str(depth - 1))
                res = self.aux_solve(new_board, inlay.x, inlay.y, depth - 1)
                if res is not None:
                    sb = StringBuilder()
                    if SOLUTION: sb += board._str_helper(inlay.x, inlay.y)  # board.show(inlay.x, inlay.y)
                    if SOLUTION: sb += "\n"  # board.show(inlay.x, inlay.y)
                    if SOLUTION: sb += (
                        "[*]\tGuessed that [{}, {}] = {} // Options {}".format(inlay.x + 1, inlay.y + 1, op,
                                                                               inlay.options))
                    if SOLUTION and not self.found: print(
                        "[*]\tFound solution with {} guesses".format(self.max_depth - depth + 1))
                    self.steps = [str(sb)] + self.steps
                    self.found = True
                    return res
                if DEBUG: print("[*] Depth is " + str(depth))
                new_board.unset_inlay(inlay.x, inlay.y)
                new_board.get_inlay(inlay.x, inlay.y).remove_option(op)

        return res
