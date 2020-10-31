"""
Created on 16 sept. 15:01 2020

@author: HaroldKS
"""

from enum import Enum


class Color(Enum):
    black = -1
    empty = 0
    green = 1


class Player(object):
    reward = None
    name = "Dark"
    in_hand = 12
    score = 0

    def __init__(self, color):
        self.color = color

    def get_name(self):
        return self.name

    def play(self, state):
        """The main fonction that has to be implemented. Given a state it has to return a legal action for the player

        Args:
            state (YoteState): A state object from the yote game.

        Raises:
            NotImplementedError: [description]
        
        Returns:
            action (YoteAction): An Yote action.
        """
        raise NotImplementedError

    def set_score(self, new_score):
        self.score = new_score

    def update_player_infos(self, infos):
        self.in_hand = infos['in_hand']
        self.score = infos['score']

    def reset_player_informations(self):
        self.in_hand = 12
        self.score = 0
