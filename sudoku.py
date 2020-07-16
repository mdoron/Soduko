import copy

from board_checker import BoardChecker
from input import Input
from sudoku_algorithm import SodukoAlgorithm
from sudoku_board import SodukoBoard
import config


class Sudoku:
    @staticmethod
    def solve(array):
        inp = SodukoBoard(Input.parse(array))
        print("[*] Input board")
        print(str(inp))
        print("[*] Solving...")

        if not BoardChecker(inp).can_continue():
            print("[*]\tThis board has no solution")
            return None

        alg = SodukoAlgorithm()
        solution = alg.aux_solve(copy.deepcopy(inp), -1, -1, config.MAX_DEPTH)

        if solution:
            print("[+] Done")
        else:
            if config.LOG: print("[*] No solution for max_depth={}".format(config.MAX_DEPTH))

        if config.SOLUTION:
            [print(step) for step in ["[*] Steps"] + alg.steps]

        if solution and not BoardChecker(solution).can_continue():
            print(solution)
            print("[*] This board has no solution")
            return None

        return solution
