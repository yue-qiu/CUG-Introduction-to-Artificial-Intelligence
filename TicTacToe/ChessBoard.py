import os
from random import choice


class Chess:
    OFFENSIVE_CHESS = "Q"  # 先手方棋子
    DEFENSIVE_CHESS = "x"  # 后手方棋子


class ChessBoard:
    SIZE = 3  # 棋盘大小，这里是井字棋所以是 3
    IDLE_SLOT = "."  # 空余位置

    def __init__(self, player_chess_type, ai_chess_type):
        self.chess_board = []
        self.player_chess = player_chess_type
        self.ai_chess = ai_chess_type

        for i in range(0, ChessBoard.SIZE * ChessBoard.SIZE):
            self.chess_board.append(ChessBoard.IDLE_SLOT)

    def __getitem__(self, item):
        return self.chess_board[item]

    def __setitem__(self, key, value):
        self.chess_board[key] = value

    def __repr__(self):
        res = ' '

        for i in range(0, ChessBoard.SIZE):
            res += "{:3}".format(i)

        res += "\n"

        for row in range(0, ChessBoard.SIZE):
            res += "{:<3}".format(row)
            for col in range(0, ChessBoard.SIZE):
                res += "{:3}".format(self.chess_board[ChessBoard.SIZE * row + col])

            res += "\n"

        return res

    # 棋子数量
    def num_of_chess(self):
        num = 0
        for i in range(0, len(self.chess_board)):
            if self.chess_board[i] != ChessBoard.IDLE_SLOT:
                num += 1

        return num

    # 判断棋盘是否还有空余位置
    def has_idle_slot(self):
        return self.num_of_chess() != len(self.chess_board)

    # 玩家落子
    def player_move(self, row, col):
        self.chess_board[row * ChessBoard.SIZE + col] = self.player_chess

    # ai 落子
    def ai_move(self):
        # 井字棋游戏的评估值只有 -1, 0, 1 三种，所以用 -2、2 分别表示负无穷与正无穷
        best_val = -2  # ai 评估值用负无穷初始化，记录在不同位置进行 alpha-beta 剪枝可以得到的最大评估值，即对 ai 最有利的落子点
        moves = []
        for i in range(0, len(self.chess_board)):
            if self.chess_board[i] == ChessBoard.IDLE_SLOT:
                self.chess_board[i] = self.ai_chess
                val = self.alpha_beta_valuation(self.player_chess, self.ai_chess, -2, 2)
                self.chess_board[i] = ChessBoard.IDLE_SLOT

                # 在 self.chess_board[i] 落子比在当前最好位置落子更好，重置 ai 的落子范围
                if val > best_val:
                    best_val = val
                    moves = [i]
                # 在 self.chess_board[i] 落子与当前最好位置一样好，扩大 ai 可落子范围
                if val == best_val:
                    moves.append(i)

        self.chess_board[choice(moves)] = self.ai_chess

    def display_chess_board(self):
        os.system("clear")
        print(self)

    # 判断某方获胜
    def has_won(self, chess_type):
        for i in range(0, len(self.chess_board)):
            if self.chess_board[i] == chess_type:
                # 横连线
                if i % ChessBoard.SIZE == 0:
                    if self.chess_board[i + 1] == chess_type and self.chess_board[i + 2] == chess_type:
                        return True

                # 竖连线
                if i < ChessBoard.SIZE:
                    if self.chess_board[i + ChessBoard.SIZE] == chess_type and \
                            self.chess_board[i + ChessBoard.SIZE * 2] == chess_type:
                        return True

                # 主对角线连线
                if i == 0:
                    if self.chess_board[4] == chess_type and self.chess_board[8] == chess_type:
                        return True

                # 副对角线连线
                if i == 2:
                    if self.chess_board[4] == chess_type and self.chess_board[6] == chess_type:
                        return True

        return False

    # Alpha-Beta 剪枝法计算当前局面的分值
    def alpha_beta_valuation(self, chess_type, next_chess_type, alpha, beta):
        # -1 表示玩家胜利，1 表示ai胜利，0 表示平局
        if self.has_won(self.player_chess):
            return -1
        elif self.has_won(self.ai_chess):
            return 1
        elif not self.has_idle_slot():
            return 0

        # 游戏继续进行
        # 搜索当前棋子所有可落子点
        for i in range(0, len(self.chess_board)):
            if self.chess_board[i] == ChessBoard.IDLE_SLOT:
                self.chess_board[i] = chess_type
                # 落子之后交换玩家
                val = self.alpha_beta_valuation(next_chess_type, chess_type, alpha, beta)
                # 回溯
                self.chess_board[i] = ChessBoard.IDLE_SLOT
                if chess_type == Chess.OFFENSIVE_CHESS:  # 当前处于 max 层
                    if val > alpha:
                        alpha = val
                    if alpha >= beta:
                        return alpha  # 返回最大可能 alpha 进行 beta 剪枝
                else:  # 当前处于 min 层
                    if val < beta:
                        beta = val
                    if alpha >= beta:
                        return beta  # 返回最大可能 beta 进行 alpha 剪枝

        if chess_type == Chess.OFFENSIVE_CHESS:
            ret = alpha
        else:
            ret = beta

        return ret
