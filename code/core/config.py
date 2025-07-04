# core/config.py
"""全局常数与枚举设定"""

from enum import Enum

# --- 棋盘尺寸 ----------------------------------------------------
BOARD_ROWS: int = 6
BOARD_COLS: int = 6

# --- 逃脱出口 (row, col) ----------------------------------------
#   下方玩家（Player 0）要走到 (0,0) 与 (0, BOARD_COLS-1)
#   上方玩家（Player 1）要走到 (BOARD_ROWS-1, 0 / -1)
EXIT_CELLS = {
    0: {(0, 0), (0, BOARD_COLS - 1)},                    # 上边两角
    1: {(BOARD_ROWS - 1, 0), (BOARD_ROWS - 1, BOARD_COLS - 1)},  # 下边两角
}

# --- 棋子颜色 / 类型 --------------------------------------------
class PieceColor(str, Enum):
    BLUE = "B"   # 好鬼
    RED  = "R"   # 坏鬼

# --- 玩家编号 ----------------------------------------------------
class PlayerID(int, Enum):
    SOUTH = 0    # 在屏幕下方那一方（习惯叫先手）
    NORTH = 1    # 在屏幕上方那一方（后手）

# --- 方向向量 ----------------------------------------------------
# 方便移动时统一索引
DIRECTIONS = {
    "N": (-1,  0),
    "S": ( 1,  0),
    "W": ( 0, -1),
    "E": ( 0,  1),
}

# 按鍵定位
INPUT_ALIASES = {
    "w": "N",   # 上
    "s": "S",   # 下
    "a": "W",   # 左
    "d": "E",   # 右
    "n": "N",
    "e": "E",
}
