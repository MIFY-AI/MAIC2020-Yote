"""
Created on 18 sept. 15:55 2020

@author: HaroldKS
"""

from core import Player
from yote.yote_rules import YoteRules


class AI(Player):

    in_hand = 12
    score = 0

    def __init__(self, name, color):
        super(AI, self).__init__(name, color)
        self.position = color.value

    def play(self, state):
        #print(f"Player {self.position} is playing and reward is {state.rewarding_move}")
        return YoteRules.random_play(state, self.position)

    def set_score(self, new_score):
        self.score = new_score

    def update_player_infos(self, infos):
        self.in_hand = infos['in_hand']
        self.score = infos['score']

    def reset_player_informations(self):
        self.in_hand = 12
        self.score = 0
