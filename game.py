# game.py
import numpy as np

class Connect5Game:
    def __init__(self, rows=7, cols=9, win_length=5):
        self.rows = rows
        self.cols = cols
        self.win_length = win_length
        self.board = np.zeros((self.rows, self.cols), dtype=int)
        self.current_player = 1

    def clone(self):
        clone = Connect5Game(self.rows, self.cols, self.win_length)
        clone.board = self.board.copy()
        clone.current_player = self.current_player
        return clone

    def available_moves(self):
        return [c for c in range(self.cols) if self.board[0][c] == 0]

    def make_move(self, col):
        for row in reversed(range(self.rows)):
            if self.board[row][col] == 0:
                self.board[row][col] = self.current_player
                self.current_player *= -1
                return True
        return False

    def check_winner(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == 0:
                    continue
                if self._check_direction(r, c, 1, 0) or \
                   self._check_direction(r, c, 0, 1) or \
                   self._check_direction(r, c, 1, 1) or \
                   self._check_direction(r, c, 1, -1):
                    return self.board[r][c]
        if np.all(self.board != 0):
            return 0  # draw
        return None  # game not over

    def _check_direction(self, r, c, dr, dc):
        count = 0
        player = self.board[r][c]
        for i in range(self.win_length):
            nr, nc = r + dr * i, c + dc * i
            if 0 <= nr < self.rows and 0 <= nc < self.cols and self.board[nr][nc] == player:
                count += 1
            else:
                break
        return count == self.win_length

    def encode(self):
        return np.expand_dims(self.board * self.current_player, axis=0)
