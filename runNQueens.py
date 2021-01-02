from Queens.ChessBoard import ChessBoard
from Queens.RRClimbing import RandResetClimbing
from Queens.MinConflicts import MinConflicts
from Queens.GA import GeneticAlgorithm

if __name__ == '__main__':
    # 想要几个皇后初始化 ChessBoard 时指定，这里取 8
    chess_board = ChessBoard(8)
    rrclimb = RandResetClimbing(chess_board)
    print(rrclimb.solve())
    #
    chess_board = ChessBoard(8)
    mConflicts = MinConflicts(chess_board)
    print(mConflicts.solve())

    chess_board = ChessBoard(8)
    ga = GeneticAlgorithm(chess_board)
    print(ga.solve())



