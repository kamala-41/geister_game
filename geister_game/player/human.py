from typing import Tuple
from core.config import PlayerID, DIRECTIONS, INPUT_ALIASES   # ← 1. 多匯入 INPUT_ALIASES
from core.board import Board, IllegalMove
from core.piece import Position
from .base_player import BasePlayer


class HumanPlayer(BasePlayer):
    def decide(self, board: Board) -> Tuple[Position, str]:
        print("\n=== 你的視角 ===")
        print(board.ascii_art(self.pid))
        print("----------------")

        while True:
            try:
                raw = input("輸入『row col dir』(ex: '5 0 w' 或 '5 0 N'): ").strip()
                if raw.lower() in ("q", "quit", "exit"):
                    raise SystemExit

                r_s, c_s, d_raw = raw.split()
                r, c = int(r_s), int(c_s)

                # 2. 轉換使用者輸入 → 真正方向鍵值 ("N/E/S/W")
                dir_key = INPUT_ALIASES.get(d_raw.lower())
                if dir_key is None:
                    print("方向必須是 w/a/s/d 或 N/E/S/W")
                    continue

                # 3. 確認這步在棋盤上是合法的
                if dir_key not in board.legal_moves((r, c)):
                    print("⚠️  該棋子往此方向非法，請再試一次")
                    continue

                return (r, c), dir_key       # ← 回傳標準方向字串

            except ValueError:
                print("格式錯誤，再試一次。")
