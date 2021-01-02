"""
4 5     # 行列数
A 4 0   # agent 起始坐标
W 1 0   # wumpus 坐标
G 1 1   # gold 坐标
P 0 3   # 陷阱 1 坐标
P 1 2   # 陷阱 2 坐标
P 3 2   # 陷阱 3 坐标
"""


# 解析保存了地图信息的文件
class FileParser:
    def __init__(self, world_file):
        self.row_col = []
        self.agent = []
        self.wumpus = []
        self.gold = []
        self.pits = [[]]

        file = open(world_file, 'r')

        self.row_col = file.readline()
        self.row_col = self.row_col.rstrip('\r\n')
        self.row_col = self.row_col.split(" ")

        self.agent = file.readline()
        self.agent = self.agent.rstrip('\r\n')
        self.agent = self.agent.split(" ")

        self.wumpus = file.readline()
        self.wumpus = self.wumpus.rstrip('\r\n')
        self.wumpus = self.wumpus.split(" ")

        self.gold = file.readline()
        self.gold = self.gold.rstrip('\r\n')
        self.gold = self.gold.split(" ")

        self.pits = []

        while True:
            pit = file.readline()
            if len(pit) == 0:
                break
            pit = pit.rstrip('\r\n')
            pit = pit.split(" ")

            self.pits.append(pit)
