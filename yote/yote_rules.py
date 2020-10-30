"""
Created on 16 sept. 17:33 2020

@author: HaroldKS
"""

from core.rules import Rule
from core import Color
from yote.yote_action import YoteActionType, YoteAction
MAX_SCORE = 12

class YoteRules(Rule):



    def __init__(self, players):
        self.players = players
        self.current_player = -1

    @staticmethod
    def is_legal_move(state, action, player, rewarding_move=False):  # TODO: Update this function to an more
        # optimized one.
        """Check if an action is a legal move.

        Args:
            state (YoteState): A state object from the yote game.
            action (Action): An action object containing the move.
            player (int): The number of the player making the move.
            rewarding_move (bool, optional): True if the move is a stealing move. Defaults to False.

        Returns:
            bool: True is the move is a legal one and False if else.
        """
        action = action.get_action_as_dict()
        if rewarding_move:
            if player == state.get_next_player() == state.get_latest_player():
                if action['action_type'] == YoteActionType.STEAL_FROM_HAND and state.in_hand[player * -1] > 0:
                    return True
                elif action['action_type'] == YoteActionType.STEAL_FROM_BOARD:
                    opponent_piece = state.get_board().get_player_pieces_on_board(Color(player * -1))
                    if opponent_piece and action['action']['at'] in opponent_piece:
                        return True
            return False
        else:
            if state.get_next_player() == player:
                if action['action_type'] == YoteActionType.ADD and state.in_hand[player] > 0:
                    empty_cells = state.get_board().get_all_empty_cells()
                    if empty_cells and action['action']['to'] in empty_cells:
                        return True
                elif action['action_type'] == YoteActionType.MOVE:
                    if state.get_board().get_cell_color(action['action']['at']) == Color(player):
                        effective_moves = YoteRules.get_effective_cell_moves(state, action['action']['at'], player)
                        if effective_moves and action['action']['to'] in effective_moves:
                            return True
                return False
            return False

    @staticmethod
    def get_effective_cell_moves(state, cell, player):
        """Give the effective(Only the possible ones) moves a player can make regarding a piece on the board.

        Args:
            state (YoteState): The current game state.
            cell ((int, int)): The coordinates of the piece on the board.
            player (int): The number of the player making the move.

        Returns:
            List: A list containing all the coordinates where the piece can go.
        """
        board = state.get_board()
        if board.is_cell_on_board(cell):
            possibles_moves = YoteRules._get_rules_possibles_moves(cell, board.board_shape)
            effective_moves = []
            i, j = cell
            for move in possibles_moves:
                if board.is_empty_cell(move):
                    effective_moves.append(move)
                elif board.get_cell_color(move) == Color(player * -1):
                    k, l = move
                    if i == k and j < l and board.is_empty_cell((i, j + 2)):
                        effective_moves.append((i, j + 2))
                    elif i == k and l < j and board.is_empty_cell((i, j - 2)):
                        effective_moves.append((i, j - 2))
                    elif j == l and i < k and board.is_empty_cell((i + 2, j)):
                        effective_moves.append((i + 2, j))
                    elif j == l and k < i and board.is_empty_cell((i - 2, j)):
                        effective_moves.append((i - 2, j))
            return effective_moves

    @staticmethod
    def is_cell_on_board(cell, board_shape):  # TODO: Remove
        """Check if a cell is on the board.

        Args:
            cell ((int, int)): The coordinates of the cell.
            board_shape ((int, int)): The board shape.

        Returns:
            bool: True if the cell is on the board False if else. 
        """
        return (0, 0) <= cell < board_shape

    @staticmethod
    def _get_rules_possibles_moves(cell, board_shape):
        """Give all possibles moves for a piece according the game rules (Up, down, left, right).

        Args:
            cell ((int, int)): The coordinates of the piece on the board.
            board_shape ((int, int)): The board shape.

        Returns:
            List: A list containing all the coordinates where the piece could go.
        """
        return [(cell[0] + a[0], cell[1] + a[1])
                for a in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                if ((0 <= cell[0] + a[0] < board_shape[0]) and (0 <= cell[1] + a[1] < board_shape[1]))]

    @staticmethod
    def act(state, action, player, rewarding_move=False):  # TODO : Wondering if I should make the random move here.
        """Take the state and the player's action and make the move if possible.

        Args:
            state (YoteState): A state object from the yote game.
            action (Action): An action object containing the move.
            player (int): The number of the player making the move.
            rewarding_move (bool, optional): True if the move is a stealing move. Defaults to False.

        Returns:
            bool: True if everything goes fine and the move was made. False is else.
        """
        if YoteRules.is_legal_move(state, action, player, rewarding_move=rewarding_move):
            return YoteRules.make_move(state, action, player, rewarding_move=rewarding_move)
        else:
            return False

    @staticmethod
    def make_move(state, action, player, rewarding_move=False):  # TODO : done and next_is_reward can be removed as
        # they are in the state object
        """Transform the action of the player to a move. The move is made and the reward computed. 

        Args:
            state (YoteState): A state object from the yote game.
            action (Action): An action object containing the move.
            player (int): The number of the player making the move.
            rewarding_move (bool, optional): True if the move is a stealing move. Defaults to False.

        Returns: (next_state, done, next_is_reward): Gives the next state of the game along with the game status and
        the type of the next step.
        """
        board = state.get_board()
        json_action = action.get_json_action()
        action = action.get_action_as_dict()
        captured = None
        reward = 0
        next_is_reward = False
        previous_is_reward = False
        if rewarding_move:
            state.boring_moves = 0
            previous_is_reward = True
            if action['action_type'] == YoteActionType.STEAL_FROM_HAND:
                reward += 1
                state.in_hand[player * -1] -= 1
            elif action['action_type'] == YoteActionType.STEAL_FROM_BOARD:
                board.empty_cell(action['action']['at'])
                reward += 1
        else:
            if action['action_type'] == YoteActionType.ADD:
                state.boring_moves += 1
                state.in_hand[player] -= 1
                board.fill_cell(action['action']['to'], Color(player))
                print(board.get_board_state()[action['action']['to']], action['action']['to'])
            elif action['action_type'] == YoteActionType.MOVE:
                at = action['action']['at']
                to = action['action']['to']

                def distance(cell_1, cell_2):
                    import math
                    return math.sqrt((cell_1[0] - cell_2[0]) ** 2 + (cell_1[1] - cell_2[1]) ** 2)

                board.empty_cell(at)
                board.fill_cell(to, Color(player))
                if int(distance(at, to)) == 1:
                    state.boring_moves += 1
                elif int(distance(at, to)) > 1:
                    state.boring_moves = 0
                    next_is_reward = True
                    board.fill_cell(to, Color(player))
                    if at[0] == to[0] and at[1] < to[1]:
                        board.empty_cell((at[0], at[1] + 1))
                        captured = (at[0], at[1] + 1)
                    elif at[0] == to[0] and at[1] > to[1]:
                        board.empty_cell((at[0], at[1] - 1))
                        captured = (at[0], at[1] - 1)
                    elif at[1] == to[1] and at[0] < to[0]:
                        board.empty_cell((at[0] + 1, at[1]))
                        captured = (at[0] + 1, at[1])
                    elif at[1] == to[1] and at[0] > to[0]:
                        board.empty_cell((at[0] - 1, at[1]))
                        captured = (at[0] - 1, at[1])
                    reward += 1

        state.set_board(board)
        state.score[player] += reward
        state.captured = captured
        state.rewarding_move = next_is_reward
        state.previous_is_reward = previous_is_reward
        state.set_latest_player(player)
        state.set_latest_move(json_action)
        if next_is_reward:
            state.set_next_player(player)
        else:
            state.set_next_player(player * -1)

        done = YoteRules.is_end_game(state)
        return state, done, next_is_reward

    @staticmethod
    def get_player_actions(state, player, reward_move=False):
        """Provide for a player and at a state all of his possible actions.

        Args:
            state (YoteState): A state object from the yote game.
            player (int): The number of the player making the move.
            reward_move (bool, optional): True if the move is a stealing move. Defaults to False.

        Returns:
            List[YoteAction]: Contains all possible actions for a player at the given state.
        """

        actions = []
        board = state.get_board()
        empty_cells = board.get_all_empty_cells()
        opponent_pieces = board.get_player_pieces_on_board(Color(player * -1))

        if reward_move:
            for piece in opponent_pieces:
                actions.append(YoteAction(action_type=YoteActionType.STEAL_FROM_BOARD, at=piece))
            if state.in_hand[player * -1] > 0:
                actions.append(YoteAction(action_type=YoteActionType.STEAL_FROM_HAND))
            return actions
        else:
            if empty_cells and state.in_hand[player] > 0:
                for cell in empty_cells:
                    actions.append(YoteAction(action_type=YoteActionType.ADD, to=cell))
            player_pieces = board.get_player_pieces_on_board(Color(player))
            for piece in player_pieces:
                moves = YoteRules.get_effective_cell_moves(state, piece, player)
                if moves:
                    for move in moves:
                        actions.append(YoteAction(action_type=YoteActionType.MOVE, at=piece, to=move))
            return actions

    @staticmethod
    def random_play(state, player):
        """Return a random move for a player at a given state.

        Args:
            state (YoteState): A state object from the yote game.
            player (int): The number of the player making the move.

        Returns:
            action : An action
        """
        import random
        #print("Player, ", player, "Reward, ", state.rewarding_move)
        actions = YoteRules.get_player_actions(state, player, reward_move=state.rewarding_move)
        return random.choice(actions)

    @staticmethod
    def is_player_stuck(state, player):  # WARNING: Note used yet
        """Check if a player has the possibility to make a move

        Args:
            state (YoteState): A state object from the yote game.
            player (int): The number of the player making the move.

        Returns:
            bool: True if a player can make a move. False if not.
        """
        return len(YoteRules.get_player_actions(state, player)) == 0

    @staticmethod
    def is_end_game(state):
        """Check if the given state is the last one for the current game.

        Args:
            state (YoteState): A state object from the yote game.

        Returns:
            bool: True if the given state is the final. False if not.
        """
        if YoteRules.is_boring(state):
            return True
        latest_player_score = state.score[state.get_latest_player()]
        if latest_player_score >= MAX_SCORE:
            return True
        return False

    @staticmethod
    def is_boring(state):
        """Check if the game is ongoing without winning moves

        Args:
            state (YoteState): A state object from the yote game.
        Returns:
            bool: True if the game is boring. False if else.
        """
        return state.boring_moves >= state.just_stop

    @staticmethod
    def get_results(state):  # TODO: Add equality case.
        """Provide the results at the end of the game.

        Args:
            state (YoteState): A state object from the yote game.

        Returns:
            Dictionary: Containing the winner and the game score.
        """
        return {'winner': max(state.score, key=state.score.get),
                'score': state.score}
