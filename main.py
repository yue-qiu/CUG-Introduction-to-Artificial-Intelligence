from Queens.ChessBoard import ChessBoard
from Queens.RRClimbing import RandResetClimbing
from Queens.MinConflicts import MinConflicts

if __name__ == '__main__':
    chess_board = ChessBoard(8)

    rrclimb = RandResetClimbing(chess_board)
    print(rrclimb.solve())

    mConflicts = MinConflicts(chess_board)
    print(mConflicts.solve())



