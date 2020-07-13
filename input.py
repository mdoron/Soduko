class Input:
    @staticmethod
    def user_board():
        """
        Write Sudoku board as lines of numbers without spaces. Use '0' for empty inlay.
        [*] Line 1: 530070000
        [*] Line 2: 600195000
        [*] Line 3: 098000060
        [*] Line 4: 800060003
        [*] Line 5: 400803001
        [*] Line 6: 700020006
        [*] Line 7: 060000280
        [*] Line 8: 000419005
        [*] Line 9: 000080079
        :return:
        """
        print("Write Sudoku board as lines of numbers without spaces. Use '0' for empty inlay.")
        b = []
        for i in range(0, 9):
            b.append(input("[*] Line {}: ".format((i+1))))

        return Input.parse(b)

    @staticmethod
    def _split(word):
        """
        Example:
            Input:
                "608904007"
            Output:
                ["6", "0", "8", "9", "0", "4", "0", "0", "7"]
        :param word:
        :return: list of chars
        """
        return [char for char in word]

    @staticmethod
    def parse(boardNumList):
        """
        Example:
            Input:
                ["608904007",
                "030087506",
                "207065000",
                "003009400",
                "740602080",
                "006840700",
                "084506071",
                "975420600",
                "100308000"]
            Output:
                [[6, None, 8, 9, None, 4, None, None, 7],
                [None, 3, None, None, 8, 7, 5, None, 6],
                [2, None, 7, None, 6, 5, None, None, None],
                [None, None, 3, None, None, 9, 4, None, None],
                [7, 4, None, 6, None, 2, None, 8, None],
                [None, None, 6, 8, 4, None, 7, None, None],
                [None, 8, 4, 5, None, 6, None, 7, 1],
                [9, 7, 5, 4, 2, None, 6, None, None],
                [1, None, None, 3, None, 8, None, None, None]]
        :param boardNumList:
        :return: parsed for Board(board=)

        """
        return [[int(x) if x != '0' else None for x in Input._split(e)] for e in boardNumList]
