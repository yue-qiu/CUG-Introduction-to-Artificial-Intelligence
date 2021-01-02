"""
Legend:
. = visited tile
A = agent
G = gold
W = wumpus
S = stench
w = potential wumpus
nw = no wumpus
P = pit
B = breeze
p = potential pit
np = no pit
"""
import time
import os


class Agent:
    def __init__(self, world):
        self.world = world
        self.world_knowledge = [[[] for i in range(self.world.num_cols)] for j in range(self.world.num_rows)]
        self.world_knowledge[self.world.agent_row][self.world.agent_col].append('A')
        self.num_stenches = 0
        self.path_out_of_cave = [[self.world.agent_row, self.world.agent_col]]
        self.mark_tile_visited()
        self.world.cave_entrance_row = self.world.agent_row
        self.world.cave_entrance_col = self.world.agent_col
        self.found_gold = False
        self.took_gold = False
        self.exited = False
        self.step = 0

        print(self)

    def __repr__(self):
        os.system("clear")
        res = ""
        for row in range(self.world.num_rows):
            res += "|"
            for col in range(self.world.num_cols):
                if len(self.world_knowledge[row][col]) == 0:
                    res += "{:8}".format("#")
                    continue
                res += "{:8}".format("".join(self.world_knowledge[row][col]))
            res += "|\n"

        res += "{}".format("-" * 34)
        return res

    # 按着来时路径回退一步
    def go_back_one_tile(self):
        if self.world.agent_row - 1 == self.path_out_of_cave[-1][0]:
            self.move('u')
        if self.world.agent_row + 1 == self.path_out_of_cave[-1][0]:
            self.move('d')
        if self.world.agent_col + 1 == self.path_out_of_cave[-1][1]:
            self.move('r')
        if self.world.agent_col - 1 == self.path_out_of_cave[-1][1]:
            self.move('l')

        del self.path_out_of_cave[-1]

    # 按着来时路径退出洞穴
    def leave_cave(self):
        for tile in reversed(self.path_out_of_cave):
            if self.world.agent_row - 1 == tile[0]:
                self.move('u')
            if self.world.agent_row + 1 == tile[0]:
                self.move('d')
            if self.world.agent_col + 1 == tile[1]:
                self.move('r')
            if self.world.agent_col - 1 == tile[1]:
                self.move('l')

            if self.world.cave_entrance_row == self.world.agent_row and \
                    self.world.cave_entrance_col == self.world.agent_col and self.found_gold:
                self.exited = True
                break

    # wumpus 开始移动，顺时针 bfs
    def explore(self):
        already_moved = False
        while not self.found_gold:

            if self.found_gold:
                break

            if self.is_safe_move(self.world.agent_row - 1, self.world.agent_col) and \
                    '.' not in self.world_knowledge[self.world.agent_row - 1][self.world.agent_col]:
                if not already_moved:
                    if self.move('u'):
                        already_moved = True

            if self.is_safe_move(self.world.agent_row, self.world.agent_col + 1) and \
                    '.' not in self.world_knowledge[self.world.agent_row][self.world.agent_col + 1]:
                if not already_moved:
                    if self.move('r'):
                        already_moved = True

            if self.is_safe_move(self.world.agent_row + 1, self.world.agent_col) and \
                    '.' not in self.world_knowledge[self.world.agent_row + 1][self.world.agent_col]:
                if not already_moved:
                    if self.move('d'):
                        already_moved = True

            if self.is_safe_move(self.world.agent_row, self.world.agent_col - 1) and \
                    '.' not in self.world_knowledge[self.world.agent_row][self.world.agent_col - 1]:
                if not already_moved:
                    if self.move('l'):
                        already_moved = True

            if not already_moved:
                self.go_back_one_tile()

            already_moved = False

    """
    尝试向 direction 移动一步，如果移动成功就更新 agent 的知识
    u: upper，向上走
    d: down，向下走
    l: left，向左走
    r: right，向右走
    """

    def move(self, direction):
        if self.found_gold and not self.took_gold:
            self.took_gold = True
            if 'G' in self.world_knowledge[self.world.agent_row][self.world.agent_col]:
                self.world_knowledge[self.world.agent_row][self.world.agent_col].remove('G')

        successful_move = False
        if direction == 'u':
            if self.is_safe_move(self.world.agent_row - 1, self.world.agent_col):
                successful_move = self.move_up()
        if direction == 'r':
            if self.is_safe_move(self.world.agent_row, self.world.agent_col + 1):
                successful_move = self.move_right()
        if direction == 'd':
            if self.is_safe_move(self.world.agent_row + 1, self.world.agent_col):
                successful_move = self.move_down()
        if direction == 'l':
            if self.is_safe_move(self.world.agent_row, self.world.agent_col - 1):
                successful_move = self.move_left()

        # 移动成功，更新 agent 的知识
        if successful_move:
            self.add_indicators_to_knowledge()
            self.mark_tile_visited()
            self.predict_wumpus()
            self.predict_pits()
            self.clean_predictions()
            self.confirm_wumpus_knowledge()

            if 'G' in self.world_knowledge[self.world.agent_row][self.world.agent_col]:
                self.found_gold = True

            self.step += 1
            # 没发现 gold 就记录下当前房间，退出洞穴的时候要原路返回
            if not self.found_gold:
                self.path_out_of_cave.append([self.world.agent_row, self.world.agent_col])

            time.sleep(3)

            print(self)
        return successful_move

    # 更新关于 agent 所在房间的记忆。包括该房间是否有 breeze、是否有 stench、是否发现 gold、是否有 pit、是否有 wumpus
    def add_indicators_to_knowledge(self):
        if 'B' in self.world.world[self.world.agent_row][self.world.agent_col] and \
                'B' not in self.world_knowledge[self.world.agent_row][self.world.agent_col]:
            self.world_knowledge[self.world.agent_row][self.world.agent_col].append('B')

        if 'S' in self.world.world[self.world.agent_row][self.world.agent_col] and \
                'S' not in self.world_knowledge[self.world.agent_row][self.world.agent_col]:
            self.world_knowledge[self.world.agent_row][self.world.agent_col].append('S')

        if 'G' in self.world.world[self.world.agent_row][self.world.agent_col] and \
                'G' not in self.world_knowledge[self.world.agent_row][self.world.agent_col]:
            self.world_knowledge[self.world.agent_row][self.world.agent_col].append('G')

        if 'P' in self.world.world[self.world.agent_row][self.world.agent_col] and \
                'P' not in self.world_knowledge[self.world.agent_row][self.world.agent_col]:
            self.world_knowledge[self.world.agent_row][self.world.agent_col].append('P')

        if 'W' in self.world.world[self.world.agent_row][self.world.agent_col] and \
                'W' not in self.world_knowledge[self.world.agent_row][self.world.agent_col]:
            self.world_knowledge[self.world.agent_row][self.world.agent_col].append('W')

    # 如果当前位置发现 breeze，更新 pits 的可能位置
    def predict_pits(self):
        if 'B' in self.world.world[self.world.agent_row][self.world.agent_col] and \
                self.world.agent_row - 1 >= 0:
            if '.' not in self.world.world[self.world.agent_row - 1][self.world.agent_col] and \
                    'p' not in self.world_knowledge[self.world.agent_row - 1][self.world.agent_col]:
                self.world_knowledge[self.world.agent_row - 1][self.world.agent_col].append('p')

        if 'B' in self.world.world[self.world.agent_row][self.world.agent_col] and \
                self.world.agent_col + 1 < self.world.num_cols:
            if '.' not in self.world.world[self.world.agent_row][self.world.agent_col + 1] and \
                    'p' not in self.world_knowledge[self.world.agent_row][self.world.agent_col + 1]:
                self.world_knowledge[self.world.agent_row][self.world.agent_col + 1].append('p')

        if 'B' in self.world.world[self.world.agent_row][self.world.agent_col] and \
                self.world.agent_row + 1 < self.world.num_rows:
            if '.' not in self.world.world[self.world.agent_row + 1][self.world.agent_col] and \
                    'p' not in self.world_knowledge[self.world.agent_row + 1][self.world.agent_col]:
                self.world_knowledge[self.world.agent_row + 1][self.world.agent_col].append('p')

        if 'B' in self.world.world[self.world.agent_row][self.world.agent_col] and \
                self.world.agent_col - 1 >= 0:
            if '.' not in self.world.world[self.world.agent_row][self.world.agent_col - 1] and \
                    'p' not in self.world_knowledge[self.world.agent_row][self.world.agent_col - 1]:
                self.world_knowledge[self.world.agent_row][self.world.agent_col - 1].append('p')

    # 如果当前位置发现 stench，更新潜在 wumpus 的位置
    def predict_wumpus(self):
        if 'S' in self.world.world[self.world.agent_row][self.world.agent_col] and \
                self.world.agent_row - 1 >= 0:
            if '.' not in self.world.world[self.world.agent_row - 1][self.world.agent_col] and \
                    'w' not in self.world_knowledge[self.world.agent_row - 1][self.world.agent_col]:
                self.world_knowledge[self.world.agent_row - 1][self.world.agent_col].append('w')

        if 'S' in self.world.world[self.world.agent_row][self.world.agent_col] and \
                self.world.agent_col + 1 < self.world.num_cols:
            if '.' not in self.world.world[self.world.agent_row][self.world.agent_col + 1] and \
                    'w' not in self.world_knowledge[self.world.agent_row][self.world.agent_col + 1]:
                self.world_knowledge[self.world.agent_row][self.world.agent_col + 1].append('w')

        if 'S' in self.world.world[self.world.agent_row][self.world.agent_col] and \
                self.world.agent_row + 1 < self.world.num_rows:
            if '.' not in self.world.world[self.world.agent_row + 1][self.world.agent_col] and \
                    'w' not in self.world_knowledge[self.world.agent_row + 1][self.world.agent_col]:
                self.world_knowledge[self.world.agent_row + 1][self.world.agent_col].append('w')

        if 'S' in self.world.world[self.world.agent_row][self.world.agent_col] and \
                self.world.agent_col - 1 >= 0:
            if '.' not in self.world.world[self.world.agent_row][self.world.agent_col - 1] and \
                    'w' not in self.world_knowledge[self.world.agent_row][self.world.agent_col - 1]:
                self.world_knowledge[self.world.agent_row][self.world.agent_col - 1].append('w')

    # 基于记忆清除不合理的假设，同时统计记忆中所有 stench 数量
    def clean_predictions(self):
        self.num_stenches = 0

        for i in range(self.world.num_rows):
            for j in range(self.world.num_cols):
                if 'S' in self.world_knowledge[i][j]:
                    self.num_stenches += 1

                # 记忆中一个潜在 wumpus 身边有不存在 stench 的房间，那这就不可能是一个真的 wumpus
                if 'w' in self.world_knowledge[i][j]:
                    if i - 1 >= 0 and '.' in self.world_knowledge[i - 1][j] and 'S' not in self.world_knowledge[i - 1][j]:
                        self.world_knowledge[i][j].remove('w')
                        self.world_knowledge[i][j].append('nw')

                    if j + 1 < self.world.num_cols and '.' in self.world_knowledge[i][j + 1] and 'S' not in self.world_knowledge[i][j + 1]:
                        self.world_knowledge[i][j].remove('w')
                        self.world_knowledge[i][j].append('nw')

                    if i + 1 < self.world.num_rows and '.' in self.world_knowledge[i + 1][j] and 'S' not in self.world_knowledge[i + 1][j]:
                        self.world_knowledge[i][j].remove('w')
                        self.world_knowledge[i][j].append('nw')

                    if j - 1 >= 0 and '.' in self.world_knowledge[i][j - 1] and 'S' not in self.world_knowledge[i][j - 1]:
                        self.world_knowledge[i][j].remove('w')
                        self.world_knowledge[i][j].append('nw')

                # 记忆中一个潜在 pit 身边有不存在 breeze 的房间，那这就不可能是一个真的 pit
                if 'p' in self.world_knowledge[i][j]:
                    if i - 1 >= 0 and '.' in self.world_knowledge[i - 1][j] and 'B' not in self.world_knowledge[i - 1][j]:
                        self.world_knowledge[i][j].remove('p')
                        self.world_knowledge[i][j].append('np')

                    if j + 1 < self.world.num_cols and '.' in self.world_knowledge[i][j + 1] and 'B' not in self.world_knowledge[i][j + 1]:
                        self.world_knowledge[i][j].remove('p')
                        self.world_knowledge[i][j].append('np')

                    if i + 1 < self.world.num_rows and '.' in self.world_knowledge[i + 1][j] and 'B' not in self.world_knowledge[i + 1][j]:
                        self.world_knowledge[i][j].remove('p')
                        self.world_knowledge[i][j].append('np')

                    if j - 1 >= 0 and '.' in self.world_knowledge[i][j - 1] and 'B' not in self.world_knowledge[i][j - 1]:
                        self.world_knowledge[i][j].remove('p')
                        self.world_knowledge[i][j].append('np')

    # 判断一个潜在的 wumpus 是否为假
    # 任何情况下知识中所有的 stench 都应该出自一个真实存在的 wumpus
    # 所以当潜在 wumpus 身边的 stench 数量小于记忆中所有 stench 数量时可以确定这不是一个 wumpus
    def confirm_wumpus_knowledge(self):
        for i in range(self.world.num_rows):
            for j in range(self.world.num_cols):
                if 'w' in self.world_knowledge[i][j]:
                    stenches_around = 0

                    if i - 1 >= 0:
                        if 'S' in self.world_knowledge[i - 1][j]:
                            stenches_around += 1

                    if j + 1 < self.world.num_cols:
                        if 'S' in self.world_knowledge[i][j + 1]:
                            stenches_around += 1

                    if i + 1 < self.world.num_rows:
                        if 'S' in self.world_knowledge[i + 1][j]:
                            stenches_around += 1

                    if j - 1 >= 0:
                        if 'S' in self.world_knowledge[i][j - 1]:
                            stenches_around += 1

                    # 某个潜在 wumpus 身边的 stench 数量小于记忆中所以 stench 数量
                    if stenches_around < self.num_stenches:
                        self.world_knowledge[i][j].remove('w')
                        self.world_knowledge[i][j].append('nw')

    def move_up(self):
        if self.world.agent_row - 1 >= 0:
            self.remove_agent()
            self.world.agent_row -= 1
            self.add_agent()
            return True
        else:
            return False

    def move_right(self):
        if self.world.agent_col + 1 < self.world.num_cols:
            self.remove_agent()
            self.world.agent_col += 1
            self.add_agent()
            return True
        else:
            return False

    def move_down(self):
        if self.world.agent_row + 1 < self.world.num_rows:
            self.remove_agent()
            self.world.agent_row += 1
            self.add_agent()
            return True
        else:
            return False

    def move_left(self):
        if self.world.agent_col - 1 >= 0:
            self.remove_agent()
            self.world.agent_col -= 1
            self.add_agent()
            return True
        else:
            return False

    def remove_agent(self):
        self.world.world[self.world.agent_row][self.world.agent_col].remove('A')
        self.world_knowledge[self.world.agent_row][self.world.agent_col].remove('A')

    def add_agent(self):
        self.world.world[self.world.agent_row][self.world.agent_col].append('A')
        self.world_knowledge[self.world.agent_row][self.world.agent_col].append('A')

    # 标记 agent 当前房间为已走过
    def mark_tile_visited(self):
        if '.' not in self.world_knowledge[self.world.agent_row][self.world.agent_col]:
            self.world.world[self.world.agent_row][self.world.agent_col].append('.')
            self.world_knowledge[self.world.agent_row][self.world.agent_col].append('.')

    def is_dead(self):
        if 'W' in self.world.world[self.world.agent_row][self.world.agent_col]:
            print("You have been slain by the Wumpus!")
            return True
        elif 'P' in self.world.world[self.world.agent_row][self.world.agent_col]:
            print("You have fallen in a pit!")
            return True
        else:
            return False

    # 判断 [row, col] 房间是否安全。只有在房间合法且一定安全的时候返回 True
    def is_safe_move(self, row, col):
        if row < 0 or col < 0 or row >= self.world.num_rows or col >= self.world.num_cols:
            return False

        if 'w' in self.world_knowledge[row][col]:
            return False

        if 'p' in self.world_knowledge[row][col]:
            return False

        if 'W' in self.world_knowledge[row][col]:
            return False

        if 'P' in self.world_knowledge[row][col]:
            return False

        return True

    def cal_score(self):
        score = 0
        if self.took_gold:
            score += 1000
        score -= self.step

        return score