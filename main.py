import boards
import consts
from input import Input
from soduko import Soduko
import argparse


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
    parser.add_argument("--input")
    parser.add_argument("--maxdepth")
    parser.add_argument("--maxcomps")
    args = parser.parse_args()
    print(ART)

    if args.input is None or args.input == "user":
        solved_board = Soduko.solve(Input.user_board(), int(args.maxdepth), int(args.maxcomps))
    else:
        # try:
        idx = int(args.input)
        if idx < len(boards.all_boards):
            solved_board = Soduko.solve(boards.all_boards[idx], int(args.maxdepth), int(args.maxcomps))
        # except ValueError:
        #     print("Couldn't understand input")
        #     return

    if solved_board is None:
        print("[*] Sorry! We could'nt find a solution this time")
    else:
        solved_board.show()


if __name__ == "__main__":
    main()