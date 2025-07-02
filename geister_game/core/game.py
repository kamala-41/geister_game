# core/game.py
from __future__ import annotations
from typing import Dict

from core.board import Board, IllegalMove
from core.config import PlayerID, PieceColor


from player.base_player import BasePlayer


class Game:
    def __init__(self, players: Dict[PlayerID, BasePlayer]) -> None:
        self.board = Board()
        self.players = players
        self.turn = 0  # 回合計數（偶數 SOUTH，下 NORTH）

    # ------------------------------------------------------------
    # 初始擺放（暫時以固定位置示範）
    # ------------------------------------------------------------
    def setup_demo(self):
        """
        示範擺兩顆棋子：(5,0) 藍 SOUTH；(4,0) 紅 SOUTH
                   (0,0) 藍 NORTH；(1,0) 紅 NORTH
        之後你可以改成隨機或讀取玩家輸入。
        """
        from core.piece import Piece  # 避免頂端循環 import

        # South
        self.board.place_piece(Piece(color=PieceColor.BLUE, owner=PlayerID.SOUTH, pos=(5, 0)))
        self.board.place_piece(Piece(color=PieceColor.RED, owner=PlayerID.SOUTH, pos=(4, 0)))

        # North
        self.board.place_piece(Piece(color=PieceColor.BLUE, owner=PlayerID.NORTH, pos=(0, 0)))
        self.board.place_piece(Piece(color=PieceColor.RED, owner=PlayerID.NORTH, pos=(1, 0)))

    # ------------------------------------------------------------
    # 主迴圈
    # ------------------------------------------------------------
    def run(self):
        self.setup_demo()

        while self.board.winner is None:
            pid = PlayerID.SOUTH if self.turn % 2 == 0 else PlayerID.NORTH
            player = self.players[pid]

            try:
                pos, direction = player.decide(self.board)
                self.board.move(pos, direction,pid)
            except IllegalMove as e:
                print(f"[{pid.name}] 非法行動：{e}，請重新輸入。")
                continue  # 讓同一玩家重新下

            self.turn += 1

        # 遊戲結束
        print("\n== 遊戲結束 ==")
        print(self.board.ascii_art())          # 全盤公開
        print("Winner:", self.board.winner.name)
