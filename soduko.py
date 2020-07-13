from input import Input
from soduko_algorithm import SodukoAlgorithm
from soduko_board import SodukoBoard


class Soduko:
    @staticmethod
    def solve(array):
        return SodukoAlgorithm(SodukoBoard(Input.parse(array))).solve()