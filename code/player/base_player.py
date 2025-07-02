# player/base_player.py
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Tuple, List
from core.config import PlayerID
from core.board import Board, IllegalMove
from core.piece import Position

class BasePlayer(ABC):
    def __init__(self, pid: PlayerID):
        self.pid = pid            # SOUTH or NORTH

    @abstractmethod
    def decide(self, board: Board) -> Tuple[Position, str]:
        """
        回傳 (棋子座標, 方向字串)，方向字串必須是 core.config.DIRECTIONS 裡的 key
        例如 ((5,0), "w")
        """
        raise NotImplementedError
