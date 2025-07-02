from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple, Optional

from .config import PieceColor, PlayerID, DIRECTIONS, BOARD_ROWS, BOARD_COLS, EXIT_CELLS


Position = Tuple[int, int]  # (row, col)


@dataclass
class Piece:
    """幽灵棋子本身"""
    color: PieceColor
    owner: PlayerID
    pos: Position

    # ---------- 基本信息 ----------
    def __str__(self) -> str:
        """调试/显示：若自己的视角 -> 返回颜色；敌方视角 -> 返回'?'"""
        return f"{self.color.value}"

    # ---------- 位移判定 ----------
    def legal_moves(self) -> list[str]:
        """返回棋子在当前 pos 的合法方向键列表（不考虑吃子逻辑，只在盘内）"""
        moves = []
        row, col = self.pos
        for dir_key, (dx, dy) in DIRECTIONS.items():
            new_r, new_c = row + dx, col + dy
            if 0 <= new_r < BOARD_ROWS and 0 <= new_c < BOARD_COLS:
                moves.append(dir_key)
        return moves

    def next_pos(self, direction: str) -> Optional[Position]:
        """给定方向，返回新坐标；若越界则返回 None"""
        if direction not in DIRECTIONS:
            raise ValueError(f"未知方向 {direction}")
        dr, dc = DIRECTIONS[direction]
        nr, nc = self.pos[0] + dr, self.pos[1] + dc
        if 0 <= nr < BOARD_ROWS and 0 <= nc < BOARD_COLS:
            return nr, nc
        return None

    # ---------- 胜负相关 ----------
    def can_escape(self) -> bool:
        """若此棋子位于自己可逃脱的出口，且本身是蓝棋，则可直接逃脱"""
        return (
            self.color == PieceColor.BLUE
            and self.pos in EXIT_CELLS[self.owner]
        )