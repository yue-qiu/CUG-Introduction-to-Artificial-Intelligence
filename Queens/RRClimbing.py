from random import randint
from math import fabs
from datetime import datetime


# 随机重启爬山法
class RandResetClimbing:
    def __init__(self, chess_board):
        self.chess_board = chess_board
        self.step = 0
        self.N = len(self.chess_board)  # 棋盘大小
        self.MAX_STEP = (self.N * self.N) << 1

    # 达到最大步数，打乱棋盘以随机重启爬山
    def reset_chess_board(self):
        # 皇后先落在对角线，保证同一列上不会有两个皇后
        for i in range(0, self.N):
            self.chess_board[i] = i

        # 交换行，打乱棋盘
        for row1 in range(0, self.N):
            row2 = randint(0, self.N-1)
            tmp = self.chess_board[row1]
            self.chess_board[row1] = self.chess_board[row2]
            self.chess_board[row2] = tmp

    # 适应度函数，评价每次爬山的效率。这里用棋盘上冲突皇后数表示
    def get_conflict_nums(self):
        conflict_nums = 0

        for row1 in range(0, self.N):
            for row2 in range(row1 + 1, self.N):
                # 有一个以上的皇后位于同一列，冲突
                if self.chess_board[row1] == self.chess_board[row2]:
                    conflict_nums += 1
                # 有一个以上的皇后位于对角线，冲突
                if fabs(row2 - row1) == fabs(self.chess_board[row2] - self.chess_board[row1]):
                    conflict_nums += 1

        return conflict_nums

    # 计算某行的最优位置，该行的皇后移动到此可使局部冲突数最小
    # 最优位置可能有多个
    def get_perfect_position(self, row):
        perfect_posi = []
        less_conflict_nums = (1 << 31) - 1

        for i in range(0, self.N):
            self.chess_board[row] = i
            conflict_nums = self.get_conflict_nums()
            # 把改行皇后移动到该列，冲突数局部最小则更新最优位置
            if conflict_nums < less_conflict_nums:
                less_conflict_nums = conflict_nums
                perfect_posi = [i]
            elif conflict_nums == less_conflict_nums:
                perfect_posi.append(i)

        # 随机返回一个该行的最佳位置
        return perfect_posi[randint(0, len(perfect_posi)-1)]

    # 某行皇后随机移动到一个最佳位置
    def set_perfect_position(self, row):
        self.chess_board[row] = self.get_perfect_position(row)

    def solve(self):
        tic = datetime.now()
        reset_count = 0  # 重启次数
        step = 0        # 爬山步长
        row_pointer = 0

        # 冲突度为 0 就可以退出迭代了
        while self.get_conflict_nums() != 0:
            # 步长超过阈值，重启爬山
            if step == self.MAX_STEP:
                reset_count += 1
                step = 0
                self.reset_chess_board()
                continue

            # 随机移动皇后到该行最佳位置，降低全局冲突度
            self.set_perfect_position(row_pointer)
            # 防止越界
            if row_pointer+1 >= self.N:
                row_pointer = (row_pointer+1) % self.N
            else:
                row_pointer += 1
            step += 1

        tok = (datetime.now() - tic).microseconds
        print(f'Random Reset Climbing Algorithm solved!, totally {step} steps and {reset_count} reset times, cast {tok} ms')

        return self.chess_board



