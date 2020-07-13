import copy
from random import randint

DEBUG = False
SOLUTION = False
LOG = False


class TooManyComputationsException(Exception):
    pass


class SodukoAlgorithm:
    """
    Implementation of the algorithm to solve a Soduko board
    """

    def __init__(self, initial_board):
        self.found = False
        self.max_depth = None
        self.loot_times = 0
        self.guess_times = 0
        self.iterations = 0
        self.max_loot_times = 20
        self.max_guess_times = 20
        self.max_iterations = 10
        self.max_depth = 16
        self.initial_board = initial_board
        self.working_board = None

    def solve(self):
        res_board = None
        iterations = 0
        while True:
            try:
                if LOG: print("[*] Iteration # {}".format(iterations))
                iterations += 1
                self.max_depth = randint(1, 20)
                if iterations % 1 == 0:
                    self.max_loot_times += 20
                    self.max_guess_times += 20
                self.loot_times = 0
                self.guess_times = 0
                if LOG: print("[*]\t\tNew max depth is {} ({} guesses)".format(self.max_depth, self.max_depth + 1))
                if LOG: print(
                    "[*]\t\tNew max_loot_times={}, max_guess_times={}".format(self.max_loot_times, self.max_guess_times))
                res_board = self.aux_solve(copy.deepcopy(self.initial_board), -1, -1, self.max_depth)
            except TooManyComputationsException:
                if LOG: print("[*]\t\tToo many computations with max_depth={}".format(self.max_depth))

            if res_board is not None:
                print("[*] Done")
                break
            else:
                if LOG: print(
                    "[*]\t\tNo solution with max_depth={}, max_loot_times={}, max_guess_times={}".format(self.max_depth,
                                                                                                      self.max_loot_times,
                                                                                                      self.max_guess_times))
        return res_board

    def loot(self, board):
        if board.is_stucked():
            return None

        self.loot_times += 1
        new_board = board
        for inlay in copy.deepcopy(board.get_empty_inlays()):
            if len(inlay.get_options()) == 1:
                try:
                    new_inlay = new_board.get_inlay(inlay.x, inlay.y)
                    new_board.set_inlay(new_inlay.x, new_inlay.y, new_inlay.get_options().pop())
                    if DEBUG: print("T: [{}, {}] = {}".format(new_inlay.x, new_inlay.y, new_inlay.value))
                    if DEBUG: print("")
                except KeyError:
                    continue
                new_board.update_diff(new_inlay)
                if new_board.is_stucked():
                    return None

        return new_board

    def loot_loop(self, board):
        if board.is_stucked():
            return None
        # BFS loop
        board_empty_count = len(board.get_empty_inlays())
        looted_board = self.loot(board)
        if looted_board is None:
            if DEBUG: print("S")
            return None
        while looted_board is not None and board_empty_count > len(looted_board.get_empty_inlays()):
            board_empty_count = len(looted_board.get_empty_inlays())
            looted_board = self.loot(looted_board)

        return looted_board

    def aux_solve(self, board, x, y, max_depth):
        if DEBUG: print("[*] Depth is " + str(max_depth))
        if board.is_stucked():
            return None

        looted_board = self.loot_loop(board)
        if looted_board is None:
            if DEBUG: print("S")
            return None

        if looted_board.is_full():
            if SOLUTION: looted_board.show(x, y)
            return looted_board

        if self.loot_times >= self.max_loot_times and self.guess_times >= self.max_guess_times:
            if DEBUG: print("S")
            raise TooManyComputationsException

        if max_depth <= 0:
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
                new_board.update_diff(new_board.get_inlay(inlay.x, inlay.y))
                if DEBUG: print("G: [{}, {}]{} = {}".format(inlay.x, inlay.y, inlay.options, op))
                if DEBUG: print("")
                res = self.aux_solve(new_board, inlay.x, inlay.y, max_depth - 1)
                if res is not None:
                    if SOLUTION: print("G: [{}, {}] = {}".format(inlay.x, inlay.y, op))
                    if SOLUTION: board.show(inlay.x, inlay.y)
                    if SOLUTION: print("")
                    if LOG and not self.found: print(
                        "[*]\t\tFound solution with {} guesses".format(self.max_depth - max_depth))
                    self.found = True
                    return res
                if DEBUG: print("[*] Depth is " + str(max_depth))
                new_board.unset_inlay(inlay.x, inlay.y)
                new_board.get_inlay(inlay.x, inlay.y).remove_option(op)
            looted_board.unset_inlay(inlay.x, inlay.y)

        return res
