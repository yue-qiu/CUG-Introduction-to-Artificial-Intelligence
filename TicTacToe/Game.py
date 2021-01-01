from .ChessBoard import Chess, ChessBoard


class Game:
    def __init__(self):
        self.chess_board = None

    def start(self):
        player_choice = input("玩家选择先后手，Q 先手，X 后手: ")
        self.chess_board = ChessBoard(player_chess_type=Chess.DEFENSIVE_CHESS, ai_chess_type=Chess.OFFENSIVE_CHESS)
        if player_choice.upper() == "Q":
            self.chess_board = ChessBoard(player_chess_type=Chess.OFFENSIVE_CHESS, ai_chess_type=Chess.DEFENSIVE_CHESS)
            self.chess_board.display_chess_board()

        while self.chess_board.has_idle_slot():
            if player_choice.upper() == "Q":  # 玩家先手
                posi = input("选择落子位置(行列以空格分隔): ")
                row, col = posi.split(" ")
                self.chess_board.player_move(int(row), int(col))
                self.chess_board.display_chess_board()
                if self.chess_board.has_won(self.chess_board.player_chess):
                    print("恭喜你获得胜利！")
                    return

                if not self.chess_board.has_idle_slot():
                    break

                self.chess_board.ai_move()
                self.chess_board.display_chess_board()
                if self.chess_board.has_won(self.chess_board.ai_chess):
                    print("很遗憾你输给了 AI")
                    return

            else:  # ai 先手
                self.chess_board.ai_move()
                self.chess_board.display_chess_board()
                if self.chess_board.has_won(self.chess_board.ai_chess):
                    print("很遗憾你输给了 AI")
                    return

                if not self.chess_board.has_idle_slot():
                    break

                posi = input("选择落子位置(行列以空格分隔):  ")
                row, col = posi.split(" ")
                self.chess_board.player_move(int(row), int(col))
                self.chess_board.display_chess_board()
                if self.chess_board.has_won(self.chess_board.player_chess):
                    print("恭喜你获得胜利！")
                    return

        print("平局，真是一场精彩的对弈！")
