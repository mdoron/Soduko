from input import Input
from soduko_algorithm import SodukoAlgorithm
from soduko_board import SodukoBoard
from consts import *


class Soduko:
    @staticmethod
    def solve(array, maxdepth, maxcomps):
        inp = SodukoBoard(Input.parse(array))
        print("[*] Input board")
        print(str(inp))
        print("[*] Solving...")
        alg = SodukoAlgorithm(inp, maxdepth, maxcomps)
        sol = alg.solve()
        if SOLUTION: [print(step) for step in ["[*] Steps"] + alg.steps]
        return sol
