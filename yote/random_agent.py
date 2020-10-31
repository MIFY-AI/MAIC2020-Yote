"""
Created on 18 sept. 15:55 2020

@author: HaroldKS
"""

from core import Player
from yote.yote_rules import YoteRules


class AI(Player):

    name = "War of Hearts"

    def __init__(self, color):
        super(AI, self).__init__(color)
        self.position = color.value

    def play(self, state):
        return YoteRules.random_play(state, self.position)
