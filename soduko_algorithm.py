import copy
from random import randint

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

        self.loot_times += 1
        for inlay in copy.deepcopy(board.get_empty_inlays()):
            if len(inlay.get_options()) == 1:

                try:
                    board.set_inlay(inlay.x, inlay.y, inlay.get_options().pop())
                    if DEBUG: print("T: [{}, {}] = {}".format(inlay.x, inlay.y, board.get_inlay(inlay.x, inlay.y).value))
                    if DEBUG: print("")
                except KeyError:
                    continue
                board.update_diff_options(board.get_inlay(inlay.x, inlay.y))
                if board.is_stucked():
                    return None

        for op, inlay in copy.deepcopy(board.lonely_options):
            board.set_inlay(inlay.x, inlay.y, op)
            if DEBUG: print("M: [{}, {}] = {}".format(inlay.x+1, inlay.y+1, op))
            if DEBUG: print("")

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
            if DEBUG: print("S")
            return None
        while looted_board is not None and (board_empty_count > len(looted_board.get_empty_inlays()) or len(looted_board.lonely_options) != 0):
            board_empty_count = len(looted_board.get_empty_inlays())
            looted_board = self.loot(looted_board)

        return looted_board

    def aux_solve(self, board, x, y, depth):
        if DEBUG: print("[*] Depth is " + str(depth))
        if board.is_stucked():
            return None

        looted_board = self.loot_loop(board)
        if looted_board is None:
            if DEBUG: print("S")
            return None

        if looted_board.is_full():
            if DEBUG: looted_board.show(x, y)
            return looted_board

        if self.loot_times >= self.max_loot_times and self.guess_times >= self.max_guess_times:
            if DEBUG: print("S")
            raise TooManyComputationsException

        if depth <= 0:
            if DEBUG: print("S")
            return None

        # Prepare for guessing
        empty_inlays = list(looted_board.get_empty_inlays())
        empty_inlays.sort(key=lambda x: len(x.get_options()))

        # DFS loop
        for ei in range(len(empty_inlays)):
            inlay = empty_inlays[ei]
            new_board = copy.deepcopy(looted_board)
            options = copy.deepcopy(inlay.get_options())
            for op in options:
                self.guess_times += 1
                new_board.set_inlay(inlay.x, inlay.y, op)
                new_board.update_diff_options(new_board.get_inlay(inlay.x, inlay.y))
                if DEBUG: print("G: [{}, {}]{} = {}".format(inlay.x+1, inlay.y+1, inlay.options, op))
                if DEBUG: print("")
                res = self.aux_solve(new_board, inlay.x, inlay.y, depth - 1)
                if res is not None:
                    sb = StringBuilder()
                    if SOLUTION: sb += board._str_helper(inlay.x, inlay.y) # board.show(inlay.x, inlay.y)
                    if SOLUTION: sb += "\n" # board.show(inlay.x, inlay.y)
                    if SOLUTION: sb += ("[*]\tGuessed that [{}, {}] = {} // Options {}".format(inlay.x+1, inlay.y+1, op, inlay.options))
                    if SOLUTION and not self.found: print(
                        "[*]\tFound solution with {} guesses".format(self.max_depth - depth + 1))
                    self.steps = [str(sb)] + self.steps
                    self.found = True
                    return res
                if DEBUG: print("[*] Depth is " + str(depth))
                new_board.unset_inlay(inlay.x, inlay.y)
                new_board.get_inlay(inlay.x, inlay.y).remove_option(op)

        return res
