import torch
import torch.nn as nn
import torch.optim as optim
import random

from model import AlphaZeroNet
from mcts import MCTS, Node
from board import Board

def self_play(model, games=10):
    data = []
    for _ in range(games):
        board = Board()
        root = Node(board)
        mcts = MCTS(model)
        cols = board.cols if hasattr(board, 'cols') else 9

        while not board.is_terminal():
            mcts.search(root)
            pi = [0] * cols
            for action, child in root.children.items():
                pi[action] = child.visits
            sum_visits = sum(pi)
            pi = [p / sum_visits for p in pi] if sum_visits > 0 else [1 / cols] * cols

            action = random.choices(range(cols), weights=pi)[0]
            data.append((board.get_tensor(), pi, None))
            board = board.play(action)
            root = Node(board)

        winner = board.get_winner()
        for i in range(len(data)):
            state, pi, _ = data[i]
            player_turn = 1 if i % 2 == 0 else -1
            reward = 0 if winner == 0 else 1 if winner == player_turn else -1
            data[i] = (state, pi, reward)

    return data

def train(model, data, epochs=5):
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    loss_fn = nn.MSELoss()

    for epoch in range(epochs):
        total_loss = 0
        for state, pi, reward in data:
            state = state.unsqueeze(0).float()
            pi = torch.tensor(pi).unsqueeze(0)
            reward = torch.tensor([[reward]], dtype=torch.float32)

            out_pi, out_v = model(state)
            policy_loss = -(pi * torch.log_softmax(out_pi, dim=1)).sum()
            value_loss = loss_fn(out_v, reward)
            loss = policy_loss + value_loss

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        print(f"Epoch {epoch + 1}, Loss: {total_loss:.4f}")

if __name__ == "__main__":
    model = AlphaZeroNet(rows=7, cols=9)
    data = self_play(model, games=5)
    train(model, data, epochs=5)
    torch.save(model.state_dict(), "alphazero_model.pth")
