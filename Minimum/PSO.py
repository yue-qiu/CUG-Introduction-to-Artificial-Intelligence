# 粒子群算法求解 f(x1, x2) = (x1)^2 - (x2)^2 的最小值，其中 -10 <= x1, x2 <= 10
from math import pow
from random import randint, random
from datetime import datetime


# 粒子个体
class Particle:
    def __init__(self, x1, x2):
        self.posi = [x1, x2]  # 当前位置
        self.speed = [0, 0]
        self.fitness = 0  # 当前适应度
        self.perfect_posi = [x1, x2]  # 最佳位置


class Solution:
    def __init__(self):
        self.w = 0.5  # 惯性因子
        self.c1 = 1  # 自我认知学习因子
        self.c2 = 1  # 社会认知学习因子
        self.global_perfect_posi = [0, 0]  # 个体当前最好位置
        self.num_of_individuals = 20  # 个体数量
        self.population = []  # 种群
        self.min_domain_of_definition = -10
        self.max_domain_of_definition = 10

    # 计算个体适应度
    @staticmethod
    def cal_fitness(particle=None, posi=None):
        if particle is not None:
            return pow(particle.posi[0], 2) - pow(particle.posi[1], 2)
        elif posi is not None:
            return pow(posi[0], 2) - pow(posi[1], 2)
        else:
            return 0.0

    # 初始化种群
    def create_population(self):
        self.population = []
        for i in range(0, self.num_of_individuals):
            x1 = randint(self.min_domain_of_definition, self.max_domain_of_definition)
            x2 = randint(self.min_domain_of_definition, self.max_domain_of_definition)
            self.population.append(Particle(x1, x2))

    # 寻找最优个体
    def set_global_perfect_posi(self):
        for i in range(0, self.num_of_individuals):
            if self.population[i].fitness < self.cal_fitness(posi=self.global_perfect_posi):
                self.global_perfect_posi = self.population[i].posi

    # 更新个体的速度和位置
    def update(self):
        for i in range(0, self.num_of_individuals):
            particle = self.population[i]
            speed0 = self.w * particle.speed[0] \
                     + self.c1 * random() * (particle.perfect_posi[0] - particle.posi[0]) \
                     + self.c2 * random() * (self.global_perfect_posi[0] - particle.posi[0])
            speed1 = self.w * particle.speed[1] \
                     + self.c1 * random() * (particle.perfect_posi[1] - particle.posi[1]) \
                     + self.c2 * random() * (self.global_perfect_posi[1] - particle.posi[1])

            posi0 = particle.posi[0] + speed0
            posi1 = particle.posi[1] + speed1

            # 更新位与定义域内的粒子
            if self.min_domain_of_definition <= posi0 <= self.max_domain_of_definition and self.min_domain_of_definition <= posi1 <= self.max_domain_of_definition:
                particle.posi = [posi0, posi1]
                particle.speed = [speed0, speed1]
                particle.fitness = self.cal_fitness(particle)

            # 粒子是否到达一个历史最优位置
            if particle.fitness > self.cal_fitness(posi=particle.perfect_posi):
                particle.perfect_posi = particle.posi

    def solve(self, times):
        tic = datetime.now()
        self.create_population()

        # 开始迭代寻找最优位置
        for i in range(0, times):
            self.update()
            self.set_global_perfect_posi()

        tok = (datetime.now() - tic).microseconds / 1000
        res = round(self.cal_fitness(Particle(self.global_perfect_posi[0], self.global_perfect_posi[1])), 2)
        print(f"Particle swarm optimization to find minimum value has done, total {times} iterations, cast {tok} ms")
        return res
