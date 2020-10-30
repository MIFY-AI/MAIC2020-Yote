from PyQt5.QtWidgets import *
from gui.piece import Piece
from gui.square import Square
from core import Board
from core import Color


class BoardGUI(QWidget):
    def __init__(self, shape, current_player=-1, parent=None):
        super(BoardGUI, self).__init__(parent)
        self.current_player = current_player
        self.color = ["black", "green"]
        self.score = {-1: 0, 1: 0}
        self.shape = shape
        self.setFixedSize(100 * shape[1], 100 * shape[0])
        grid_layout = QGridLayout()
        grid_layout.setSpacing(0)
        self.squares = list()
        self._board = Board(shape)
        for i in range(shape[0]):
            temp = list()
            for j in range(shape[1]):
                square = Square(i, j)
                grid_layout.addWidget(square, shape[0] - i, j)
                temp.append(square)
            self.squares.append(temp)
        self.set_default_colors()
        self.setLayout(grid_layout)

    def get_board_state(self):
        return self._board

    def add_piece(self, cell, player):
        x, y = cell[0], cell[1]
        self.squares[x][y].set_piece(Piece(player, Color(player).name))

    def move_piece(self, at, to, player):
        x, y = to[0], to[1]
        self.squares[x][y].set_piece(Piece(player, Color(player).name))
        x, y = at[0], at[1]
        self.squares[x][y].remove_piece()

    def remove_piece(self, cell):
        x, y = cell[0], cell[1]
        self.squares[x][y].remove_piece()

    def set_default_colors(self):
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                self.squares[i][j].setStyleSheet("border: 1px solid black; background-color : white")

    def set_current_player(self, player):
        self.current_player = player

    def reset_board(self):
        self._board = Board(self.shape)
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                self.squares[i][j].remove_piece()

    def enable_all_squares(self):
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                self.squares[i][j].set_active(True)

    def disable_all_squares(self):
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                self.squares[i][j].set_active(False)

    def putListBoard(self, listBoard):  # TODO: Need Update
        for i in range(len(self.self.squares)):
            for j in range(len(self.self.squares[0])):
                if listBoard[i][j] == None:
                    self.squares[i][j].removePiece()
                elif listBoard[i][j] == "black":
                    self.squares[i][j].setPiece(Piece(0, "black"))
                elif listBoard[i][j] == "green":
                    self.squares[i][j].setPiece(Piece(1, "green"))

    def get_board_array(self): # TODO: Need Update
        list_board = []
        for i in range(len(self.squares)):
            temp = []
            for j in range(len(self.squares[0])):
                if not self.squares[i][j].isPiece():
                    temp.append(None)
                else:
                    temp.append(self.squares[i][j].piece.getColor())
            list_board.append(temp)
        return list_board
