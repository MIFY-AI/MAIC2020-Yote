"""
Created on 17 sept. 12:52 2020

@author: HaroldKS
"""

from core import Player


class YotePlayer(Player):

    def __init__(self, name, color, player_position):

        super(YotePlayer, self).__init__(name, color)
        self._reset_player_info()

    def _reset_player_info(self):
        self.pieces_in_hand = 12
        self.reward = None

    def play(self, state):
        raise NotImplementedError