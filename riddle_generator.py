import copy

import boards
import config
from board_checker import BoardChecker
from input import Input
from sudoku_algorithm import SodukoAlgorithm
from sudoku_board import SodukoBoard


class RiddleGenerator:
    @staticmethod
    def generate(empty_inlays, depth):

        solution = None
        alg = None
        while not solution:
            inp = SodukoBoard(Input.parse(boards.empty))
            print("[*] Generating, it might take a while...")

            alg = SodukoAlgorithm()
            solution = alg.aux_solve(copy.deepcopy(inp), -1, -1, 81)

            if solution and not BoardChecker(solution).can_continue():
                solution = None

        solution_riddle = None
        i = 0
        while not solution_riddle:
            if config.LOG > 0: print("[*] Iteration #{}".format(i))
            peb = boards.partially_empty(solution.to_array(), empty_inlays)
            # BFS
            for j in range(depth + 1):
                if config.LOG > 0: print("[*] Trying to find a solution in depth {}".format(j))
                inp_riddle = SodukoBoard(Input.parse(peb))
                alg_riddle = SodukoAlgorithm()
                solution_riddle = alg_riddle.aux_solve(copy.deepcopy(inp_riddle), -1, -1, j)
                if j < depth and solution_riddle:
                    if config.LOG > 0: print("[*] Theres is a solution in depth {}. Continuing...".format(j))
                    break
            i += 1

        return [print(step) for step in
                ["[*] Riddle level {}".format(config.GENERATE),
                 "[*]\tNumber of empty inlays is {}".format(empty_inlays),
                 "[*]\tYou have to guess {} times to solve the riddle".format(depth), str(inp_riddle),
                 "[*] Steps"] + alg_riddle.steps + [str(solution_riddle)]]
