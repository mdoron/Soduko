import copy
from random import shuffle

import config
from consts import *
from inlay import Inlay
from string_builder import StringBuilder


class SodukoAlgorithm:
    """
    Implementation of the algorithm to solve a Soduko board
    """

    def __init__(self):
        self.steps = []

    def loot(self, board):
        if config.LOG: print("[*]\t\tLooting...")
        if board.is_stuck():
            return None

        for area in board.areas:
            for i in SQUARE_OPTIONS:
                if len(area[i]) != 2:
                    continue
                for j in range(i + 1, BOARD_SIZE + 1):
                    if area[i] == area[j]:
                        for inlay in area[i]:
                            for op in inlay.options.difference({i, j}):
                                try:
                                    if config.LOG: print(
                                         "[*]\t\t\tTwo squares same options. Removing option {} from [{}, {}]".format(op, inlay.x, inlay.y))
                                    area[op].remove(inlay)
                                    inlay.remove_option(op)
                                    if len(area[op]) == 1:
                                        board.lonely_options.add((op, area[op].pop()))
                                except KeyError:
                                    if config.LOG: print("[*]\t\t\tNo options to remove")
        for row in board.rows:
            for i in SQUARE_OPTIONS:
                if len(row[i]) != 2:
                    continue
                for j in range(i + 1, BOARD_SIZE + 1):
                    if row[i] == row[j]:
                        for inlay in row[i]:
                            for op in inlay.options.difference({i, j}):
                                try:
                                    if config.LOG: print(
                                        "[*]\t\t\tTwo squares same options. Removing option {} from [{}, {}]".format(op, inlay.x, inlay.y))
                                    row[op].remove(inlay)
                                    inlay.remove_option(op)
                                    if len(row[op]) == 1:
                                        board.lonely_options.add((op, row[op].pop()))
                                except KeyError:
                                    if config.LOG: print("[*]\t\t\tNo options to remove")

        for col in board.cols:
            for i in SQUARE_OPTIONS:
                if len(col[i]) != 2:
                    continue
                for j in range(i + 1, BOARD_SIZE + 1):
                    if col[i] == col[j]:
                        for inlay in col[i]:
                            for op in inlay.options.difference({i, j}):
                                try:
                                    if config.LOG: print(
                                        "[*]\t\t\tTwo squares same options. Removing option {} from [{}, {}]".format(op, inlay.x, inlay.y))
                                    col[op].remove(inlay)
                                    inlay.remove_option(op)
                                    inlay.remove_option(op)
                                    if len(col[op]) == 1:
                                        board.lonely_options.add((op, col[op].pop()))
                                except KeyError:
                                    if config.LOG: print("[*]\t\t\tNo options to remove")

        for area in board.areas:
            for i in SQUARE_OPTIONS:
                if len(area[i]) != 3:
                    continue
                for j in range(i + 1, BOARD_SIZE + 1):
                    if area[i] == area[j]:
                        for l in range(j + 1, BOARD_SIZE + 1):
                            if area[i] == area[l]:
                                for inlay in area[i]:
                                    for op in inlay.options.difference({i, j, l}):
                                        try:
                                            if config.LOG: print(
                                                "[*]\t\t\tThree squares same options. Removing option {} from [{}, {}]".format(op, inlay.x,
                                                                                                   inlay.y))
                                            area[op].remove(inlay)
                                            inlay.remove_option(op)
                                            if len(area[op]) == 1:
                                                board.lonely_options.add((op, area[op].pop()))
                                        except KeyError:
                                            if config.LOG: print("[*]\t\t\tNo options to remove")

        for inlay in copy.deepcopy(board.get_empty_inlays()):
            for op, inlay in copy.deepcopy(board.lonely_options):
                board.set_inlay(inlay.x, inlay.y, op)
                if config.LOG: print("[*]\t\t\tLonely option, [{}, {}] = {}".format(inlay.x + 1, inlay.y + 1, op))

                board.update_diff_options(board.get_inlay(inlay.x, inlay.y))
                if config.LOG == 2: board.show()
                board.lonely_options.remove((op, inlay))
                if board.is_stuck():
                    return None
            if len(inlay.get_options()) == 1:
                try:
                    board.set_inlay(inlay.x, inlay.y, inlay.get_options().pop())
                    if config.LOG: print(
                        "[*]\t\t\tIsolated option, [{}, {}] = {}".format(inlay.x + 1, inlay.y + 1, board.get_inlay(inlay.x, inlay.y).value))
                except KeyError:
                    continue
                board.update_diff_options(board.get_inlay(inlay.x, inlay.y))
                if config.LOG == 2: board.show()
                if board.is_stuck():
                    return None
        if config.LOG: print("[*]\t\tFinished")
        return board

    def loot_loop(self, board):
        if config.LOG: print("[*]\tLoot loop")
        if board.is_stuck():
            return None
        # BFS loop
        board_empty_count = len(board.get_empty_inlays())
        looted_board = self.loot(board)
        if not looted_board:
            return None
        while looted_board and (
                not board.is_full() and board_empty_count > len(looted_board.get_empty_inlays()) or
                len(looted_board.lonely_options) != 0):
            board_empty_count = len(looted_board.get_empty_inlays())
            looted_board = self.loot(looted_board)

        if config.LOG: print("[*]\tFinished")

        return looted_board

    def aux_solve(self, board, x, y, depth):
        if config.LOG: print("[*]\tDepth is " + str(config.MAX_DEPTH - depth))
        if board.is_stuck():
            if config.LOG: print("[-]\tStuck. Wrong option.")
            return None

        looted_board = self.loot_loop(board)
        if not looted_board:
            if config.LOG: print("[-]\tStuck. Wrong option.")
            return None

        if looted_board.is_full():
            return looted_board

        if depth <= 0:
            if config.LOG: print("[-]\tStuck. Max depth reached.")
            return None

        # Prepare for guessing
        empty_inlays = list(looted_board.get_empty_inlays())
        empty_inlays.sort(key=lambda x: len(x.get_options()))

        # DFS loop
        eis = list(range(len(empty_inlays)))
        if config.RANDOMIZE:
            shuffle(eis)

        for ei in eis:
            inlay = empty_inlays[ei]
            new_board = copy.deepcopy(looted_board)
            options = list(copy.deepcopy(inlay.get_options()))
            if config.RANDOMIZE:
                shuffle(options)

            for op in options:
                new_board.set_inlay(inlay.x, inlay.y, op)

                new_board.update_diff_options(new_board.get_inlay(inlay.x, inlay.y))
                if config.LOG: print(
                    "[*]\tGussing that [{}, {}]{} = {}".format(inlay.x + 1, inlay.y + 1, inlay.options, op))
                if config.LOG == 2: board.show()

                res = self.aux_solve(new_board, inlay.x, inlay.y, depth - 1)
                if res:
                    sb = StringBuilder()
                    if config.SOLUTION:
                        sb += str(board)
                        sb += "\n"
                        sb += ("[*]\tGuessed that [{}, {}] = {} // Options {}".format(inlay.x + 1, inlay.y + 1, op,
                                                                                      inlay.options))

                        self.steps = [str(sb)] + self.steps
                    return res
                new_board.unset_inlay(inlay.x, inlay.y)
                new_board.get_inlay(inlay.x, inlay.y).remove_option(op)

        return res
