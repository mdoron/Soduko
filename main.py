import boards
from soduko import Soduko

if __name__ == "__main__":
    print("[*] Solving...")
    solved_board = Soduko.solve(boards.board4)
    if solved_board is None:
        print("[*] Sorry! We could'nt find a solution this time")
    else:
        solved_board.show()
