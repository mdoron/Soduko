from input import Input
from sudoku import Sudoku
import argparse
import config

ART = r'''
         ___,   _,  _,  ____,    ____,   _,  _,  _,  _,
        ///=\\ /|| /|| /||=\\\  ///=\\\ /|| /// /|| /||
        \\\_,  ||| ||| |||  ||| ||| ||| |||///  ||| |||
        _`"\\\ ||| ||| |||  ||| ||| ||| |||\\\  ||| |||
        \\=/// \\\=/// |||=///  \\\=/// ||| \\\ \\\=///
         `""`   `"""`  `"""""`   `"""`  `"`  `"` `"""` 
                          @mdoron
                          '''


def main():
    parser = argparse.ArgumentParser(description="Solves a sudoku")
    parser.add_argument("--input", help="input method. Fixed board or user input")
    parser.add_argument("--random-board",
                        help="generate partially empty board from fixed board with RANDOM_BOARD empty inlays")
    parser.add_argument("--max-depth", help="limit depth of guessing")
    parser.add_argument("--randomize", action='store_true', help="shuffle options when algorithm needs to choose")
    parser.add_argument("--show", action='store_true', help="show solution steps")
    parser.add_argument("--log", help="show log")

    args = parser.parse_args()
    print(ART)

    config.MAX_DEPTH = int(args.max_depth) if args.max_depth else config.MAX_DEPTH
    config.EMPTY_INLAYS = int(args.random_board) if args.random_board else config.EMPTY_INLAYS
    config.LOG = int(args.log) if args.log else 0
    config.SOLUTION = True if args.show else False
    config.RANDOMIZE = True if args.randomize else False

    import boards

    solved_board = None
    if args.random_board:
        solved_board = Sudoku.solve(boards.random_board)
    elif not args.input or args.input == "user":
        solved_board = Sudoku.solve(Input.user_board())
    else:
        idx = int(args.input)
        if len(boards.all_boards) > idx:
            solved_board = Sudoku.solve(boards.all_boards[idx])

    if not solved_board:
        print("[*] Could not understand input or no solution")
    else:
        solved_board.show()


if __name__ == "__main__":
    main()