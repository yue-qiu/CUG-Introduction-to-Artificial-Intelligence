# Alpha-Beta 剪枝法实现井字棋游戏
# Q 表示先手方落子，X 表示后手方落子，* 表示可用位置
# 下面这个例子是先手方获胜
# Q  *  X
# *  Q  X
# *  *  Q
from TicTacToe.Game import Game

if __name__ == "__main__":
    game = Game()
    game.start()
