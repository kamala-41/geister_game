"""
棋盤 (Board) 與所有行動邏輯：
    - 放子 / 移動 / 吃子 / 逃脫
    - 勝負條件判定
"""

from __future__ import annotations
from typing import List, Optional, Dict

from .config import (
    BOARD_ROWS,
    BOARD_COLS,
    PieceColor,
    PlayerID,
    DIRECTIONS,
    EXIT_CELLS,
)
from .piece import Piece, Position


# ------------------------------------------------------------
# 例外
# ------------------------------------------------------------
class IllegalMove(Exception):
    """丟出：嘗試非法行動時"""


# ------------------------------------------------------------
# 棋盤
# ------------------------------------------------------------
class Board:
    """標準 6*6 幽靈棋棋盤"""

    # --------------------------------------------------------
    # 初始化
    # --------------------------------------------------------
    def __init__(self) -> None:
        # 2D 盤面：沒有棋子則為 None
        self.grid: List[List[Optional[Piece]]] = [
            [None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)
        ]

        # 被吃掉的棋子統計：{player: {color: count}}
        self.captured: Dict[PlayerID, Dict[PieceColor, int]] = {
            PlayerID.SOUTH: {PieceColor.RED: 0, PieceColor.BLUE: 0},
            PlayerID.NORTH: {PieceColor.RED: 0, PieceColor.BLUE: 0},
        }

        self.winner: Optional[PlayerID] = None  # None 表示未結束

    # --------------------------------------------------------
    # 放置與查詢
    # --------------------------------------------------------
    def place_piece(self, piece: Piece) -> None:
        """僅開局階段使用：把棋子放到指定座標。"""
        r, c = piece.pos
        if self.grid[r][c] is not None:
            raise IllegalMove("此格已有棋子")
        self.grid[r][c] = piece

    def at(self, pos: Position) -> Optional[Piece]:
        """回傳指定位置的棋子（或 None）。"""
        r, c = pos
        return self.grid[r][c]

    # --------------------------------------------------------
    # 行動：移動 / 吃子 / 逃脫
    # --------------------------------------------------------
    def move(self, pos: Position, direction: str, player: PlayerID) -> None:
        """
        執行單一步行動：
            1. 檢查合法
            2. 處理吃子
            3. 更新棋子座標
            4. 檢查逃脫 / 吃光條件
        """
        piece = self.at(pos)
        if piece is None:
            raise IllegalMove("該位置無棋子")
        if piece.owner != player:
            raise IllegalMove("不能移動對手的棋子")

        # 計算目標座標
        dx, dy = DIRECTIONS[direction]
        nr, nc = piece.pos[0] + dx, piece.pos[1] + dy
        if not (0 <= nr < BOARD_ROWS and 0 <= nc < BOARD_COLS):
            raise IllegalMove("超出棋盤邊界")

        target_piece = self.grid[nr][nc]

        # ---------- 處理吃子 ----------
        if target_piece:
            if target_piece.owner == piece.owner:
                raise IllegalMove("不能吃自己人")
            self._capture(piece.owner, target_piece)
            self.grid[nr][nc] = None  # 清空，待會兒放入新位置

        # ---------- 移動棋子 ----------
        self.grid[piece.pos[0]][piece.pos[1]] = None
        piece.pos = (nr, nc)
        self.grid[nr][nc] = piece

        # ---------- 判斷藍棋逃脫 ----------
        if piece.can_escape():
            self.winner = piece.owner
            return

        # ---------- 判斷吃光 / 被吃光 ----------
        self._check_capture_victory()

    # --------------------------------------------------------
    # 內部：吃子後更新統計
    # --------------------------------------------------------
    def _capture(self, attacker: PlayerID, target: Piece) -> None:
        victim_owner = target.owner
        self.captured[attacker][target.color] += 1

        # 吃光對手藍：攻擊方勝
        if (
            target.color == PieceColor.BLUE
            and self.captured[attacker][PieceColor.BLUE] == 4
        ):
            self.winner = attacker

        # 自己紅子被吃光：自己勝
        if (
            target.color == PieceColor.RED
            and self.captured[attacker][PieceColor.RED] == 4
        ):
            self.winner = victim_owner

    # --------------------------------------------------------
    # 內部：整盤檢查藍/紅數量勝負
    # --------------------------------------------------------
    def _check_capture_victory(self) -> None:
        # 一口氣檢查兩邊
        if self.captured[PlayerID.SOUTH][PieceColor.BLUE] == 4:
            self.winner = PlayerID.NORTH
        if self.captured[PlayerID.NORTH][PieceColor.BLUE] == 4:
            self.winner = PlayerID.SOUTH

        for pid in (PlayerID.SOUTH, PlayerID.NORTH):
            if self.captured[pid][PieceColor.RED] == 4:
                self.winner = pid

    # --------------------------------------------------------
    # 取得合法方向
    # --------------------------------------------------------
    def legal_moves(self, pos: Position) -> List[str]:
        piece = self.at(pos)
        if piece is None:
            return []

        dirs: List[str] = []
        for dir_key in piece.legal_moves():
            nr, nc = piece.next_pos(dir_key)
            if nr is None:
                continue
            target = self.grid[nr][nc]
            # 不能吃自己人
            if target and target.owner == piece.owner:
                continue
            dirs.append(dir_key)
        return dirs

    # --------------------------------------------------------
    # 文字化棋盤（偵錯用）
    # --------------------------------------------------------
    def ascii_art(self, perspective: PlayerID | None = None) -> str:
        """
        若指定 perspective,只顯示該玩家可見顏色；
        沒指定則全盤公開。
        """
        rows: List[str] = []
        for r in range(BOARD_ROWS):
            line: List[str] = []
            for c in range(BOARD_COLS):
                p = self.grid[r][c]
                if p is None:
                    line.append(".")
                elif perspective is not None and p.owner != perspective:
                    line.append("?")
                else:
                    line.append(p.color.value)
            rows.append(" ".join(line))
        return "\n".join(rows)

    # 方便直接 print(board) 調試
    def __str__(self) -> str:
        return self.ascii_art()
