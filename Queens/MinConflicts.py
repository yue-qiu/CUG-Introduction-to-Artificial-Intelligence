from datetime import datetime


class MinConflicts:
    def __init__(self, chess_board):
        self.chess_board = chess_board
        self.N = len(chess_board)
        self.bias = self.N - 1
        self.cols = []  # 记录第 i 列上的皇后数量
        # 从左上到右下的对角线上 row-col 值是相同的，但是这个值有可能是负值，最小为 -(N-1)
        # 所以可以做个偏移，统一加上 N-1，这样这个值就在 [0, 2*N-2]范围内，将这个值作为该对角线的编号
        # pdiag[i] 表示当前摆放方式下编号为 i 的对角线上的皇后数
        self.pdiag = []  # principal diagonal,主对角线，左上到右下（表示和主对角线平行的2N-1条对角线）
        # 从右上到左下的对角线 row+col 的值相同，取值范围为[0, 2*N-2]，作为对角线编号
        # cdiag[i] 表示编号为 i 的副对角线上的皇后数
        self.cdiag = []  # counter diagonal，副对角线

        for i in range(0, self.N):
            self.cols.append(1)  # 每列一个皇后

        for i in range(0, 2 * self.N - 1):
            self.pdiag.append(0)
            self.cdiag.append(0)

        for row in range(0, self.N):
            self.pdiag[MinConflicts.get_pdiag(row, chess_board[row], self.bias)] += 1  # 统计该皇后从左上到右下那条对角线上有几个皇后
            self.cdiag[MinConflicts.get_cdiag(row, chess_board[row])] += 1  # 统计该皇后从右上到左下那条对角线上有几个皇后

    # 给定棋盘上一个点，返回其从左上到右下的对角线
    @staticmethod
    def get_pdiag(row, col, bias):
        return row - col + bias

    # 给定棋盘上一个点，返回起从右上到左下的对角线
    @staticmethod
    def get_cdiag(row, col):
        return row + col

    # 适应度函数
    def check_status(self):
        for row in range(0, self.N):
            if self.cols[self.chess_board[row]] != 1 or self.pdiag[
                MinConflicts.get_pdiag(row, self.chess_board[row], self.bias)] != 1 or self.cdiag[
                MinConflicts.get_cdiag(row, self.chess_board[row])] != 1:
                return False

        return True

    # 最小冲突法调整第 row 行皇后的位置
    def set_perfect_position(self, row):
        cur_col = self.chess_board[row]
        perfect_posi = cur_col  # 最佳位置
        less_conflict_nums = self.cols[perfect_posi] + self.pdiag[MinConflicts.get_pdiag(row, perfect_posi, self.bias)] - 1 + self.cdiag[MinConflicts.get_cdiag(row, perfect_posi)] - 1

        # 检查第 row 行的每一列
        for col in range(0, self.N):
            if col == cur_col:
                continue

            # 计算如果把皇后移动至此的冲突数
            conflict_nums = self.cols[col] + self.pdiag[MinConflicts.get_pdiag(row, col, self.bias)] + self.cdiag[MinConflicts.get_cdiag(row, col)]
            if conflict_nums < less_conflict_nums:
                less_conflict_nums = conflict_nums
                perfect_posi = col

        # 发现了比现在更好的位置，移动皇后并更新列及对角线记录
        # 移动之后检查是否存在冲突
        if perfect_posi != cur_col:
            self.cols[cur_col] -= 1
            self.cols[perfect_posi] += 1
            self.pdiag[MinConflicts.get_pdiag(row, cur_col, self.bias)] -= 1
            self.pdiag[MinConflicts.get_pdiag(row, perfect_posi, self.bias)] += 1
            self.cdiag[MinConflicts.get_cdiag(row, cur_col)] -= 1
            self.cdiag[MinConflicts.get_cdiag(row, perfect_posi)] += 1

            self.chess_board[row] = perfect_posi

        return self.check_status()

    def solve(self):
        tic = datetime.now()
        ok = False
        row_pointer = 0
        num_of_generations = 0

        while not ok:
            num_of_generations += 1
            # 逐行调整最佳位置
            if self.set_perfect_position(row_pointer):
                ok = True
            if row_pointer+1 >= self.N:
                row_pointer = (row_pointer+1) % self.N
            else:
                row_pointer += 1

        tok = (datetime.now() - tic).microseconds / 1000
        print(f'Minimum Conflicts Algorithm Solved, totally {num_of_generations} generations, cast {tok} ms')

        return self.chess_board
