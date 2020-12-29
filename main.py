from Queens.ChessBoard import ChessBoard
from Queens.RRClimbing import RandResetClimbing

if __name__ == '__main__':
    chess_board = ChessBoard(8)

    rrclimb = RandResetClimbing(chess_board)

    print(rrclimb.solve())




