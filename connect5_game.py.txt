# connect5_game.py
import numpy as np

class Connect5:
    def __init__(self, rows=7, cols=9):
        self.rows = rows
        self.cols = cols
        self.board = np.zeros((rows, cols), dtype=int)
        self.current_player = 1

    def clone(self):
        clone = Connect5(self.rows, self.cols)
        clone.board = self.board.copy()
        clone.current_player = self.current_player
        return clone

    def get_legal_actions(self):
        return [c for c in range(self.cols) if self.board[0][c] == 0]

    def play(self, action):
        for r in range(self.rows-1, -1, -1):
            if self.board[r][action] == 0:
                self.board[r][action] = self.current_player
                self.current_player = 3 - self.current_player
                return True
        return False

    def is_full(self):
        return all(self.board[0][c] != 0 for c in range(self.cols))

    def check_winner(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == 0:
                    continue
                if c + 4 < self.cols and all(self.board[r][c+i] == self.board[r][c] for i in range(5)):
                    return self.board[r][c]
                if r + 4 < self.rows and all(self.board[r+i][c] == self.board[r][c] for i in range(5)):
                    return self.board[r][c]
                if r + 4 < self.rows and c + 4 < self.cols and all(self.board[r+i][c+i] == self.board[r][c] for i in range(5)):
                    return self.board[r][c]
                if r + 4 < self.rows and c - 4 >= 0 and all(self.board[r+i][c-i] == self.board[r][c] for i in range(5)):
                    return self.board[r][c]
        return 0

    def game_over(self):
        return self.check_winner() != 0 or self.is_full()

    def get_current_player(self):
        return self.current_player

    def get_board_tensor(self):
        # Returns board as a tensor for the neural network: shape (1, rows, cols)
        player = self.current_player
        return np.where(self.board == player, 1, np.where(self.board == 3 - player, -1, 0)).reshape(1, self.rows, self.cols).astype(np.float32)
