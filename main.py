import boards
from input import Input
from soduko import Soduko

if __name__ == "__main__":
    print(r'''
 ___,   ____,   ____,    _,  _,  _,  _,  ____, 
///=\\ ///=\\\ /||=\\\  /|| /|| /|| /// ///=\\\
\\\_,  ||| ||| |||  ||| ||| ||| |||///  ||| |||
_`"\\\ ||| ||| |||  ||| ||| ||| |||\\\  ||| |||
\\=/// \\\=/// |||=///  \\\=/// ||| \\\ \\\=///
 `""`   `"""`  `"""""`   `"""`  `"`  `"` `"""` 
                  @mdoron''')
    solved_board = Soduko.solve(boards.board3)
    if solved_board is None:
        print("[*] Sorry! We could'nt find a solution this time")
    else:
        solved_board.show()
