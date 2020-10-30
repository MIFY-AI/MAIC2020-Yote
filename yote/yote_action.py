"""
Created on 17 sept. 13:22 2020

@author: HaroldKS
"""

from core import Action

from enum import Enum


class YoteActionType(Enum):

    MOVE = 1
    ADD = 2
    STEAL_FROM_BOARD = 3
    STEAL_FROM_HAND = 4




class YoteAction(Action):

    def __init__(self, action_type, **kwargs):
        """This is the format that every action must have. Dependending of the action type additional parameters can be asked.
            Example : a move from (0, 1) to (0, 2) is equivalent to YoteAction(action_type=YoteActionType.MOVE, at=(0, 1), to=(0, 2))

        Args:
            action_type (YoteActionType): The type of the performed action.
        """
        assert isinstance(action_type, YoteActionType), "Not a good action type format"
        self.action_type = action_type

        if action_type == YoteActionType.ADD:
            assert ((len(kwargs) == 1) and ('to' in kwargs.keys())), "Need you to add only argument 'to'"
            assert isinstance(kwargs['to'], tuple), "to has to be a tuple"

        elif action_type == YoteActionType.MOVE:
            assert ((len(kwargs) == 2) and ('to' in kwargs.keys()) and ('at' in kwargs.keys())),\
                "Need you to add argument 'at' and 'to'"
            assert isinstance(kwargs['to'], tuple) and isinstance(kwargs['at'], tuple),\
                "to and from has to be a tuple"

        elif action_type == YoteActionType.STEAL_FROM_BOARD:
            assert ((len(kwargs) == 1) and ('at' in kwargs.keys())), "Need you from add only argument 'at'"
            assert isinstance(kwargs['at'], tuple), "at has to be a tuple"
        elif action_type == YoteActionType.STEAL_FROM_HAND:
            assert len(kwargs) == 0, "Don't need more arguments"

        self.action = kwargs

    def __repr__(self):
        return str(self.get_action_as_dict())

    def get_action_as_dict(self):
        return {'action_type': self.action_type,
                'action': self.action}

    def get_json_action(self):
        return {'action_type': self.action_type.name,
                'action': self.action}
