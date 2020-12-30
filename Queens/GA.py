from random import randint
from math import fabs
from .ChessBoard import ChessBoard
from datetime import datetime


class GeneticAlgorithm:
    def __init__(self, chess_board):
        self.chess_board = []
        self.N = len(chess_board)  # 皇后数目
        self.num_of_individuals = self.N << 2  # 种群中个体的数量
        self.max_num_of_not_conflict = 0  # 个体最大不冲突数
        self.fitness = []  # 种群个体适应度比例列表
        self.population = []  # 种群

        # 计算个体最大不冲突数
        for i in range(1, self.N):
            self.max_num_of_not_conflict += i

    # 适应度函数，检查个体不冲突的皇后数
    @staticmethod
    def get_no_conflict_nums(chess_board):
        sum_of_not_conflict_individual = 0
        for row1 in range(0, len(chess_board)):
            for row2 in range(row1 + 1, len(chess_board)):
                # 皇后不位于同一列且不位于同一对角线
                if fabs(row2 - row1) != fabs(chess_board[row2] - chess_board[row1]) and chess_board[row2] != \
                        chess_board[row1]:
                    sum_of_not_conflict_individual += 1

        return sum_of_not_conflict_individual

    # 返回种群（棋盘集合）中不存在冲突的个体的位置，若这样的个体不存在返回 -1
    def position_of_no_conflict(self):
        for i in range(0, self.num_of_individuals):
            if self.get_no_conflict_nums(self.population[i]) == self.max_num_of_not_conflict:
                return i

        return -1

    # 计算种群中每个个体的适应度并将比例保存在 fitness 中
    def get_fitness(self):
        self.fitness = []
        sum_of_no_conflicts = 0
        no_conflicts = []

        for i in range(0, self.num_of_individuals):
            n = GeneticAlgorithm.get_no_conflict_nums(self.population[i])
            sum_of_no_conflicts += n
            no_conflicts.append(n)

        for i in range(0, self.num_of_individuals):
            self.fitness.append(no_conflicts[i] / sum_of_no_conflicts)

    # 形成一个种群，有 num_of_individuals 个个体
    def create_population(self):
        self.population = []
        for i in range(0, self.num_of_individuals):
            chess_board = ChessBoard(self.N)
            self.population.append(chess_board)

    # 随机选择两个个体。轮盘赌算法产生 0-1 的随机数，按适应度比例挑选个体
    def select(self):
        m = 0
        parents = []
        p1 = randint(0, 99) / 100
        p2 = randint(0, 99) / 100

        # p 在 [m, m+fitness[i]] 之间认为选择了 i
        for i in range(0, self.num_of_individuals):
            m += self.fitness[i]
            if p1 <= m:
                parents.append(self.population[i])
                break

        for i in range(0, self.num_of_individuals):
            m += self.fitness[i]
            if p2 <= m:
                parents.append(self.population[i])
                break

        return parents

    # 对两个个体进行杂交产生一个后代
    def crossover(self, chess_board1, chess_board2):
        son = []
        p1, p2 = 0, 0

        while p1 >= p2:
            p1 = randint(0, self.N - 1)
            p2 = randint(0, self.N - 1)

        # [0, p1) 与 (p2, N) 之间选择 chess_board1
        # [p1, p2] 之间选择 chess_board2
        for i in range(0, self.N):
            if i < p1 or i > p2:
                son.append(chess_board1[i])
            else:
                son.append(chess_board2[i])

        return ChessBoard(chess_board=son)

    # 对杂交后代进行变异
    def mutate(self, chess_board):
        row = randint(0, self.N-1)
        col = randint(0, self.N-1)
        chess_board[row] = col

        return chess_board

    def solve(self):
        tic = datetime.now()
        p_mutate = 0.2  # 变异概率
        p_crossover = 0.9  # 交叉概率
        self.create_population()
        num_of_generation = 0  # 进化代数

        # 没有不冲突的个体，开始进化
        while self.position_of_no_conflict() == -1:
            # 计算种群中每个个体的适应度
            self.get_fitness()
            new_population = []
            # 一直杂交产生更优秀的后代放入新种群，直到新种群和原种群一样大
            while len(new_population) != self.num_of_individuals:
                # 随机选择父母
                parents = self.select()
                while True:
                    son = parents[0]
                    # 本次杂交的交叉概率
                    pc = randint(0, 99) / 100
                    if pc < p_crossover:
                        son = self.crossover(parents[0], parents[1])

                    # 本次杂交的变异概率
                    pm = randint(0, 99) / 100
                    if pm < p_mutate:
                        son = self.mutate(son)

                    # 若儿子优于父母，添加到新种群中
                    nums_of_no_conflicts_of_son = self.get_no_conflict_nums(son)
                    nums_of_no_conflicts_of_parents0 = self.get_no_conflict_nums(parents[0])
                    nums_of_no_conflicts_of_parents1 = self.get_no_conflict_nums(parents[1])
                    if nums_of_no_conflicts_of_son >= nums_of_no_conflicts_of_parents0 and nums_of_no_conflicts_of_son >= nums_of_no_conflicts_of_parents1:
                        new_population.append(son)
                        break
                    else:
                        # 随着种群进化儿子应该越来越优秀，否则增加变异概率
                        if p_mutate <= 0.98:
                            p_mutate += 0.02

            # 用更优秀的新种群代替老种群
            self.population = new_population
            num_of_generation += 1

        # 进化结束，得到不冲突的个体
        self.chess_board = self.population[self.position_of_no_conflict()]
        tok = (datetime.now() - tic).seconds
        print(f'Genetic Algorithm solved, total generation: {num_of_generation}, cast {tok} s')
        return self.chess_board
