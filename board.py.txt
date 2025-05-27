import torch
import numpy as np

class Board:
    def __init__(self, rows=7, cols=9, win_length=5):
        self.rows = rows
        self.cols = cols
        self.win_length = win_length
        self.board = np.zeros((rows, cols), dtype=int)
        self.current_player = 1

    def play(self, action):
        for row in reversed(range(self.rows)):
            if self.board[row][action] == 0:
                new_board = Board(self.rows, self.cols, self.win_length)
                new_board.board = np.copy(self.board)
                new_board.board[row][action] = self.current_player
                new_board.current_player = -self.current_player
                return new_board
        raise ValueError("Invalid action")

    def is_terminal(self):
        return self.get_winner() != 0 or not (self.board == 0).any()

    def get_winner(self):
        # Check rows, columns and diagonals for a win
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == 0:
                    continue
                player = self.board[r][c]
                # Horizontal
                if c + self.win_length <= self.cols and all(self.board[r][c+i] == player for i in range(self.win_length)):
                    return player
                # Vertical
                if r + self.win_length <= self.rows and all(self.board[r+i][c] == player for i in range(self.win_length)):
                    return player
                # Diagonal down-right
                if r + self.win_length <= self.rows and c + self.win_length <= self.cols and all(self.board[r+i][c+i] == player for i in range(self.win_length)):
                    return player
                # Diagonal up-right
                if r - self.win_length >= -1 and c + self.win_length <= self.cols and all(self.board[r-i][c+i] == player for i in range(self.win_length)):
                    return player
        return 0  # No winner

    def get_tensor(self):
        tensor = torch.tensor(self.board, dtype=torch.float32).unsqueeze(0)
        return tensor

    def get_legal_actions(self):
        return [c for c in range(self.cols) if self.board[0][c] == 0]

    def get_cols(self):
        return self.cols
