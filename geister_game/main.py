# geister_game/main.py
from core.config import PlayerID
from core.game import Game
from player.human import HumanPlayer

south = HumanPlayer(PlayerID.SOUTH)
north = HumanPlayer(PlayerID.NORTH)

g = Game({PlayerID.SOUTH: south, PlayerID.NORTH: north})
g.run()
