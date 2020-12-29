from random import randint


class ChessBoard:
    def __init__(self, N):
        self.chess_board = []

        for i in range(0, N):
            self.chess_board.append(i)

        for row1 in range(0, N):
            row2 = randint(0, N-1)
            tmp = self.chess_board[row1]
            self.chess_board[row1] = self.chess_board[row2]
            self.chess_board[row2] = tmp

    def __repr__(self):
        res = '-{}\n'.format("--" * 8)

        for row in range(0, len(self.chess_board)):
            res += "|"
            for col in range(0, len(self.chess_board)):
                if self.chess_board[row] == col:
                    res += "*|"
                    continue
                res += " |"
            res += '\n{}-\n'.format("--" * 8)

        return res

    def __len__(self):
        return len(self.chess_board)

    def __getitem__(self, item):
        return self.chess_board[item]

    def __setitem__(self, key, value):
        self.chess_board[key] = value
