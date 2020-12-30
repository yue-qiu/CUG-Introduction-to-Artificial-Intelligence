from random import randint


class ChessBoard:
    def __init__(self, n=8, chess_board=None):
        if chess_board is None:
            self.chess_board = []
            self.N = n

            for i in range(0, n):
                self.chess_board.append(i)

            # 原地洗牌算法打乱棋盘
            for row1 in range(0, n-1):
                row2 = randint(row1+1, n-1)
                tmp = self.chess_board[row1]
                self.chess_board[row1] = self.chess_board[row2]
                self.chess_board[row2] = tmp

        else:
            self.chess_board = chess_board
            self.N = len(chess_board)

    def __repr__(self):
        res = ""
        for row in range(0, len(self.chess_board)):
            for col in range(0, len(self.chess_board)):
                if self.chess_board[row] == col:
                    res += "{:3}".format("Q")
                    continue
                res += "{:3}".format("*")
            res += "\n"

        return res

    def __len__(self):
        return len(self.chess_board)

    def __getitem__(self, item):
        return self.chess_board[item]

    def __setitem__(self, key, value):
        self.chess_board[key] = value
