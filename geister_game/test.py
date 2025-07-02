if __name__ == "__main__":

    print("run")

    from core.board import Board
    from core.piece import Piece
    from core.config import PieceColor, PlayerID

    b = Board()

    # 放測試棋
    b.place_piece(Piece(PieceColor.BLUE, PlayerID.SOUTH, (5, 0)))
    b.place_piece(Piece(PieceColor.RED,  PlayerID.NORTH, (4, 0)))

    print("== 初始盤 ==")
    print(b.ascii_art())

    # 移動吃掉
    b.move((5, 0), "U")

    print("\n== 吃子後 ==")
    print(b.ascii_art())

    print("Winner:", b.winner)
