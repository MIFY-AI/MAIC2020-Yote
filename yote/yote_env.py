"""
Created on 16 sept. 15:55 2020

@author: HaroldKS
"""

from core import BoardEnv
from core import Board
from yote.yote_rules import YoteRules
from yote.yote_action import YoteAction
from yote.yote_state import YoteState

import logging


class YoteEnv(BoardEnv):

    def __init__(self, board_shape, players, allowed_time, game_phases=None, first_player=-1, boring_limit=200): # TODO: Remove player object
        assert isinstance(game_phases, int) or game_phases is None, "Game phases has to be None or an integer"
        self.players = players
        self.board_shape = board_shape
        self.allowed_time = allowed_time
        self.game_phases = game_phases
        self.rewarding_move = False
        self.done = False
        self.first_player = first_player
        self.just_stop = boring_limit
        self._reset()

    def reset(self):
        self._reset()

    def _reset(self):
        self.board = Board(self.board_shape, max_per_cell=1)
        self.state = YoteState(board=self.board, next_player=self.first_player, boring_limit=self.just_stop)
        self.current_player = self.first_player

    def step(self, action):
        """Plays one step of the game. Takes an action and perform in the environment.

        Args:
            action (Action): An action containing the move from a player.

        Returns:
            bool: Dependent on the validity of the action will return True if the was was performed False if not.
        """
        assert isinstance(action, YoteAction), "action has to be an Action class object"
        result = YoteRules.act(self.state, action, self.current_player, self.rewarding_move)
        if isinstance(result, bool):
            return False
        else:
            self.state, self.done, self.rewarding_move = result
            self.current_player = self.state.get_next_player()
            self.rewarding_move = self.state.rewarding_move
            return True

    def render(self):
        """Gives the current state of the environnement

        Returns:
            (state, done): The state and the game status
        """
        return self.state, self.done

    def get_player_info(self, player):
        return self.state.get_player_info(player)

    def get_state(self):
        return self.state

    def is_end_game(self):
        return self.done