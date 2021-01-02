from Wumpus.FileParser import FileParser


# 根据文件生成 wumpus 世界地图
class World:
    def __init__(self):
        self.world = [[]]
        self.num_rows = 0
        self.num_cols = 0

        self.agent_row = 0
        self.agent_col = 0
        self.cave_entrance_row = 0
        self.cave_entrance_col = 0

    def generate_world(self, file_name):
        file_parser = FileParser(file_name)
        self.num_rows = int(file_parser.row_col[0])
        self.num_cols = int(file_parser.row_col[1])

        self.world = [[[] for i in range(self.num_cols)] for j in range(self.num_rows)]

        self.agent_row = int(file_parser.agent[1])
        self.agent_col = int(file_parser.agent[2])
        self.world[self.agent_row][self.agent_col].append(file_parser.agent[0])

        self.world[int(file_parser.wumpus[1])][int(file_parser.wumpus[2])].append(file_parser.wumpus[0])
        self.world[int(file_parser.gold[1])][int(file_parser.gold[2])].append(file_parser.gold[0])
        for pit in file_parser.pits:
            self.world[int(pit[1])][int(pit[2])].append(pit[0])

        self.populate_indicators()

    # 根据 wumpus 和 pits 坐标在相邻房间生成各自的指示
    def populate_indicators(self):
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                for i in range(len(self.world[row][col])):
                    if self.world[row][col][i] == 'W':
                        if row - 1 >= 0:
                            if 'S' not in self.world[row - 1][col]:
                                self.world[row - 1][col].append('S')

                        if row + 1 < self.num_rows:
                            if 'S' not in self.world[row + 1][col]:
                                self.world[row + 1][col].append('S')

                        if col + 1 < self.num_cols:
                            if 'S' not in self.world[row][col + 1]:
                                self.world[row][col + 1].append('S')

                        if col - 1 >= 0:
                            if 'S' not in self.world[row][col - 1]:
                                self.world[row][col - 1].append('S')

                    if self.world[row][col][i] == 'P':
                        if row - 1 >= 0:
                            if 'B' not in self.world[row - 1][col]:
                                self.world[row - 1][col].append('B')

                        if col + 1 < self.num_cols:
                            if 'B' not in self.world[row][col + 1]:
                                self.world[row][col + 1].append('B')

                        if row + 1 < self.num_rows:
                            if 'B' not in self.world[row + 1][col]:
                                self.world[row + 1][col].append('B')

                        if col - 1 >= 0:
                            if 'B' not in self.world[row][col - 1]:
                                self.world[row][col - 1].append('B')

