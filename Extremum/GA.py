# 遗传算法求解 f(x) = 15x - x^2 的极大值，其中 x 为整数。定义域为 [0, 15]
from random import randint
from math import pow


class Solution:
    def __init__(self):
        self.fitness = []
        self.population = []
        self.chromosome_length = 4  # 染色体初始长度
        self.min_domain_of_definition = 0
        self.max_domain_of_definition = 15
        self.num_of_individuals = 20  # 种群大小
        self.p_mutate = 0.2  # 变异概率
        self.p_crossover = 0.9  # 染色体交叉概率

    def decimal_to_binary_str(self, num):
        res = bin(num)[2:]
        l = list(res)
        while len(l) < self.chromosome_length:
            l.insert(0, '0')

        return "".join(l)

    def create_population(self):
        for i in range(0, self.num_of_individuals):
            num = randint(self.min_domain_of_definition, self.max_domain_of_definition)
            self.population.append(self.decimal_to_binary_str(num))

    # 计算种群中每个个体的适应度
    def get_fitness(self):
        for i in range(0, self.num_of_individuals):
            self.fitness.append(15 * int(self.population[i], base=2) - pow(int(self.population[i], base=2), 2))

    # 得到适应度最大值
    def get_maximum_value(self):
        res = self.fitness[0]
        for num in self.fitness:
            if num > res:
                res = num

        return int(res)

    # 得到适应度最小值
    def get_minimum_value(self):
        res = self.fitness[0]
        for num in self.fitness:
            if num < res:
                res = num

        return int(res)

    # 随机选择两个个体。使用轮盘赌算法
    def select(self):
        parents = []
        m = 0
        p1 = randint(self.get_minimum_value(), self.get_maximum_value()-1)
        p2 = randint(self.get_minimum_value(), self.get_maximum_value()-1)

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

    # 对两个个体进行杂交，双点+双侧杂交
    def crossover(self, x1, x2):
        son = []
        p1, p2 = 0, 0

        while p1 >= p2:
            p1 = randint(0, (1 << self.chromosome_length) - 1)
            p2 = randint(0, (1 << self.chromosome_length) - 1)

        for i in range(0, self.chromosome_length):
            if i < p1 or i > p2:
                son.append(x1[i])
            else:
                son.append(x2[i])

        return "".join(son)

    # 对杂交后代进行变异
    def mutate(self, son):
        i = randint(0, self.chromosome_length - 1)
        tmp = list(son)
        if tmp[i] == '1':
            tmp[i] = '0'
        else:
            tmp[i] = '1'

        return "".join(tmp)

    def solve(self, times):
        self.create_population()

        while times != 0:
            self.get_fitness()
            new_population = []
            while len(new_population) != len(self.population):
                # 选择父母
                parents = self.select()
                while True:
                    son = parents[0]
                    # 本次杂交的交叉概率
                    pc = randint(0, 99) / 100
                    if pc < self.p_crossover:
                        son = self.crossover(parents[0], parents[1])

                    # 本次杂交的变异概率
                    pm = randint(0, 99) / 100
                    if pm < self.p_mutate:
                        son = self.mutate(son)

                    # 如果孩子比父母更优秀，放入新种群中
                    if int(son, base=2) >= int(parents[0], base=2) and int(son, base=2) >= int(parents[1], base=2):
                        new_population.append(son)
                        break
                    else:
                        # 随着种群进化儿子应该越来越优秀，否则增加变异概率
                        if self.p_mutate <= 0.98:
                            self.p_mutate += 0.02

            # 用更优秀的新种群代替老种群
            self.population = new_population
            times -= 1

        # 进化结束，选择最好的一个个体
        return self.get_maximum_value()
