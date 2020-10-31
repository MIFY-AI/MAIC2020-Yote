"""
Created on 30 oct. 11:20 2020

@author: HaroldKS
"""

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from gui.panel import Panel
from gui.board import BoardGUI
from yote import YoteState
from core import Color
from yote import YoteRules
from yote import YoteAction
from copy import deepcopy
from utils.timer import Timer
from utils.trace import Trace
import argparse
import time
import sys


class YoteGUI(QMainWindow):
    depth_to_cover = 9
    automatic_save_game = False

    def __init__(self, app, shape, players, allowed_time=60.0, sleep_time=.500, first_player=-1, boring_limit=200,
                 parent=None):
        super(YoteGUI, self).__init__(parent)
        self.app = app

        self.saved = True
        self.board_shape = shape
        self.players = players
        self.allowed_time = allowed_time
        self.sleep_time = sleep_time
        self.first_player = first_player
        self.just_stop = boring_limit

        self.setWindowTitle("[*] MAIC 2019 - Yote Game")
        self.statusBar()
        self.setWindowIcon(QtGui.QIcon("assets/icon.png"))
        layout = QHBoxLayout()
        layout.addStretch()
        self.board_gui = BoardGUI(self.board_shape)
        layout.addWidget(self.board_gui)
        layout.addSpacing(15)
        self.panel = Panel([players[-1].name, players[1].name])
        layout.addWidget(self.panel)
        layout.addStretch()
        content = QWidget()
        content.setLayout(layout)
        self.setCentralWidget(content)
        self.create_menu()

        self._reset()

        # self.trace = Trace(self.board.get_board_array())

        # self.random_player = AI(self.board.currentPlayer, self.board_size)

    def _reset(self):

        self.done = False
        self.rewarding_move = False
        self.board = BoardGUI(self.board_shape)
        self.state = YoteState(board=self.board.get_board_state(), next_player=self.first_player,
                               boring_limit=self.just_stop)
        self.trace = Trace(self.state, players={-1: self.players[-1].name, 1: self.players[1].name})
        self.current_player = self.first_player

    def reset(self):
        self._reset()

    def create_menu(self):
        menu = self.menuBar()
        # Game Menu
        game_menu = menu.addMenu("Game")

        # New Game Submenu
        new_game_action = QAction(QtGui.QIcon.fromTheme("document-new", QtGui.QIcon("../assets/New file.png")),
                                  'New Game',
                                  self)
        new_game_action.setShortcut(QtGui.QKeySequence.New)
        new_game_action.setStatusTip("New game Luncher")

        new_game_action.triggered.connect(self.new_game_trigger)

        game_menu.addAction(new_game_action)

        game_menu.addSeparator()

        # Load Game Submenu
        load_game_action = QAction(QtGui.QIcon.fromTheme("document-new", QtGui.QIcon("../assets/Open file.png")),
                                   'Load Game', self)
        load_game_action.setShortcut(QtGui.QKeySequence.Open)
        load_game_action.setStatusTip("Load a previous game")
        load_game_action.triggered.connect(self.load_game_trigger)
        game_menu.addAction(load_game_action)

        # Save Game
        save_game_action = QAction(QtGui.QIcon.fromTheme("document-new", QtGui.QIcon("pieces/Save.png")), 'Save Game',
                                   self)
        save_game_action.setShortcut(QtGui.QKeySequence.Save)
        save_game_action.setStatusTip("Save current game")
        save_game_action.triggered.connect(self.save_game_trigger)
        game_menu.addAction(save_game_action)

        game_menu.addSeparator()

        # Exit and close game
        exit_game_action = QAction(QtGui.QIcon.fromTheme("document-new", QtGui.QIcon("pieces/Close.png")), 'Exit Game',
                                   self)
        exit_game_action.setShortcut(QtGui.QKeySequence.Quit)
        exit_game_action.setMenuRole(QAction.QuitRole)
        exit_game_action.setStatusTip("Exit and close window")
        exit_game_action.triggered.connect(self.exit_game_trigger)
        game_menu.addAction(exit_game_action)

        menu.addSeparator()

        # Help Menu
        help_menu = menu.addMenu("Help")

        # Rules
        game_rules_action = QAction(QtGui.QIcon.fromTheme("document-new", QtGui.QIcon("pieces/Help.png")), 'Rules',
                                    self)
        game_rules_action.setMenuRole(QAction.AboutRole)
        game_rules_action.triggered.connect(self.game_rules_trigger)
        help_menu.addAction(game_rules_action)

        help_menu.addSeparator()

        # About
        about_action = QAction('About', self)
        about_action.setMenuRole(QAction.AboutRole)
        about_action.triggered.connect(self.about_trigger)
        help_menu.addAction(about_action)

    def new_game_trigger(self):
        new_game = QMessageBox.question(self, 'New Game', "You're about to start a new Game.",
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if new_game == QMessageBox.Yes:
            self._reset_for_new_game()
            self.play_game()
        else:
            pass

    def _reset_for_new_game(self):
        self.board.reset_board()
        self.board.score = {-1: 0, 1: 0}
        self.done = False

        self.board.enable_all_squares()
        self.panel.reset_panel_player()
        self.board.current_player = -1
        self.current_player = self.first_player
        self.panel.update_current_player(self.current_player)

        self.state = YoteState(board=self.board.get_board_state(), next_player=self.first_player,
                               boring_limit=self.just_stop)
        self.board.set_default_colors()

        for key in self.players.keys():
            self.players[key].reset_player_informations()

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

    def play_game(self):
        hit = 0

        timer_first_player = Timer("first_player", total_time=0.1, logger=None)
        timer_second_player = Timer("second_player", total_time=0.1, logger=None)
        turn = self.first_player
        while not self.done:
            hit += 1
            time.sleep(self.sleep_time)
            state = deepcopy(self.state)
            remain_time = timer_first_player.remain_time() if turn == -1 else timer_second_player.remain_time()
            if remain_time > 0:
                timer_first_player.start() if turn == -1 else timer_second_player.start()
                action = self.players[turn].play(state)
                elapsed_time = timer_first_player.stop() if turn == -1 else timer_second_player.stop()
                remain_time = timer_first_player.remain_time() if turn == -1 else timer_second_player.remain_time()
                if self.step(action):
                    print('Action performed successfully by', turn, ' in', str(elapsed_time), ' rest ', remain_time)
                else:
                    print("An illegal move were given. Performing a random move")
                    print(f"Lunching a random move for {turn}, and reward is {state.rewarding_move}")
                    action = YoteRules.random_play(state, turn)  # TODO: Should we use the original state?

            else:
                print("Not remain time for ", turn, " Performing a random move")
                print(f"Lunching a random move for {turn}, and reward is {state.rewarding_move}")
                action = YoteRules.random_play(state, turn)  # TODO: Should we use the original state?
            self._update_gui()
            self.trace.add(self.state)
            self.players[turn].update_player_infos(self.get_player_info(turn))
            turn = self.state.get_next_player()
        self._results()
        self.save_game_trigger()
        self.board_gui.set_default_colors()
        print("\nIt's over.")

    def _update_gui(self):
        action = self.state.get_latest_move()
        if self.state.previous_is_reward:
            self.app.processEvents()
            if action['action_type'] == 'STEAL_FROM_BOARD':
                at = action['action']['at']
                self.board_gui.squares[at[0]][at[1]].set_background_color("red")
                self.app.processEvents()
                time.sleep(self.sleep_time)
                self.board_gui.remove_piece(at)
        else:
            self.app.processEvents()
            if action['action_type'] == 'ADD':
                # app.processEvents()
                to = action['action']['to']
                self.board_gui.squares[to[0]][to[1]].set_background_color("blue")
                self.board_gui.add_piece(to, self.state.get_latest_player())
                self.app.processEvents()
            elif action['action_type'] == 'MOVE':
                to = action['action']['to']
                at = action['action']['at']
                self.app.processEvents()
                self.board_gui.squares[at[0]][at[1]].set_background_color("blue")
                time.sleep(self.sleep_time / 2)
                self.board_gui.squares[to[0]][to[1]].set_background_color("green")
                self.board_gui.move_piece(at, to, self.state.get_latest_player())
                if self.state.captured is not None:
                    i, j = self.state.captured
                    self.board_gui.squares[i][j].set_background_color("red")
                    self.app.processEvents()
                    time.sleep(self.sleep_time)
                    self.board_gui.remove_piece(self.state.captured)
                self.app.processEvents()
                time.sleep(self.sleep_time)
        self.panel.update_score(self.state.score, self.state.in_hand)
        self.board_gui.set_default_colors()
        self.panel.update_current_player(self.state.get_next_player())

    def get_player_info(self, player):
        return self.state.get_player_info(player)

    def is_end_game(self):
        return self.done

    def _results(self):
        if self.done:
            self.trace.done = self.done
            results = YoteRules.get_results(self.state)
            if not results['tie']:
                end = QMessageBox.information(self, "End", f"{self.players[results['winner']].name} wins.")
            else:
                end = QMessageBox.information(self, "End", "No winners.")

    def load_battle(self, states, delay=0.5, done=True):
        hit = 0
        self.board.set_default_colors()
        self.state = states[0]
        for state in states[1:]:
            action = state.get_latest_move()
            self.state = state
            self._update_gui()
            time.sleep(delay)
        self.done = done
        self._results()
        print("It's over.")

    def load_game_trigger(self):
        self.board.set_default_colors()
        name = QtWidgets.QFileDialog.getOpenFileName(self, 'Load Game', options=QFileDialog.DontUseNativeDialog)
        print(name[0])
        trace = self.trace.load(name[0])
        print(trace.players)
        self._reset_for_new_game()
        actions = trace.get_actions()
        delay, ok = QInputDialog.getDouble(self, 'Enter the delay', '')
        players_name = trace.players
        self.panel.update_players_name(players_name)
        self.load_battle(actions, delay, trace.done)

    def save_game_trigger(self):
        if self.done:
            if self.automatic_save_game:
                self.trace.write(self.players[-1].name + "-" + self.players[1].name)
            else:
                name = QtWidgets.QFileDialog.getSaveFileName(self, 'Save Game', options=QFileDialog.DontUseNativeDialog)
                if name[0] == "":
                    pass
                else:
                    self.trace.write(name[0])
        else:
            warning = QMessageBox.warning(self, "Warning", "No game ongoing")

    def exit_game_trigger(self):
        sys.exit(self.app.exec_())

    def game_rules_trigger(self):
        rules = "Yoté Rules \n " \
                "The game is played on a 5×6 board, which is empty at the beginning of the game. Each player has twelve pieces in hand. Players alternate turns, with White(or green) moving first. In a move, a player may either: \n" \
                "-Place a piece in hand on any empty cell of the board. \n" \
                "-Move one of their pieces already on the board orthogonally to an empty adjacent cell. \n" \
                "-Capture an opponent's piece if it is orthogonally adjacent to a player's piece, by jumping to the empty cell immediately beyond it. The captured piece is removed from the board, and the capturing player removes another of the opponent's pieces of his choosing from the board. \n" \
                "The player who captures all the opponent's pieces is the winner. The game can end in a draw if both players are left with three or fewer pieces. \n" \
                "For more informations : https://en.wikipedia.org/wiki/Yot%C3%A9";
        box = QMessageBox()
        box.about(self, "Rules", rules)

    def about_trigger(self):
        about = "MAIC 2019 Yote Game by MIFY and AAAI Benin"
        box = QMessageBox()
        box.about(self, "About", about)

    def closeEvent(self, a0: QtGui.QCloseEvent):
        if self.exit_game_trigger() == True:
            a0.accept()
        else:
            a0.ignore()


if __name__ == "__main__":
    import sys
    import ctypes

    app_id = 'myfi.maic.yote.1.0'
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    except AttributeError:
        pass
    app = QApplication(sys.argv)

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', help='total number of seconds credited to each player')
    parser.add_argument('-ai0', help='path to the ai that will play as player 0')
    parser.add_argument('-ai1', help='path to the ai that will play as player 1')
    parser.add_argument('-s', help='time to show the board')
    args = parser.parse_args()

    # set the time to play
    allowed_time = float(args.t) if args.t is not None else .1
    sleep_time = float(args.s) if args.s is not None else 0.

    player_type = ['human', 'human']
    player_type[0] = args.ai0 if args.ai0 != None else 'human'
    player_type[1] = args.ai1 if args.ai1 != None else 'human'
    for i in range(2):
        if player_type[i].endswith('.py'):
            player_type[i] = player_type[i][:-3]
    agents = {}

    # load the agents
    k = -1
    for i in range(2):
        if player_type[i] != 'human':
            j = player_type[i].rfind('/')
            # extract the dir from the agent
            dir = player_type[i][:j]
            # add the dir to the system path
            sys.path.append(dir)
            # extract the agent filename
            file = player_type[i][j + 1:]
            # create the agent instance
            agents[k] = getattr(__import__(file), 'AI')(Color(k))
            k *= -1
    if None in agents:
        raise Exception('Problems in  AI players instances. \n'
                        'Usage:\n'
                        '-t time credited \n'
                        '\t total number of seconds credited to each player \n'
                        '-ai0 ai0_file.py \n'
                        '\t path to the ai that will play as player 0 \n'
                        '-ai1 ai1_file.py\n'
                        '\t path to the ai that will play as player 1 \n'
                        '-s sleep time \n'
                        '\t time(in second) to show the board(or move)')
    game = YoteGUI((5, 6), agents, sleep_time=sleep_time, allowed_time=allowed_time)
    game.show()
    sys.exit(app.exec_())
