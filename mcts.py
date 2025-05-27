# mcts.py
import math
import numpy as np
import copy

class TreeNode:
    def __init__(self, parent, prior_prob):
        self.parent = parent
        self.children = {}
        self.n_visits = 0
        self.Q = 0
        self.u = 0
        self.P = prior_prob

    def expand(self, action_priors):
        for action, prob in action_priors:
            if action not in self.children:
                self.children[action] = TreeNode(self, prob)

    def select(self, c_puct):
        return max(self.children.items(), key=lambda act_node: act_node[1].get_value(c_puct))

    def update(self, leaf_value):
        self.n_visits += 1
        self.Q += (leaf_value - self.Q) / self.n_visits

    def update_recursive(self, leaf_value):
        if self.parent:
            self.parent.update_recursive(-leaf_value)
        self.update(leaf_value)

    def get_value(self, c_puct):
        self.u = (c_puct * self.P * math.sqrt(self.parent.n_visits) / (1 + self.n_visits))
        return self.Q + self.u

    def is_leaf(self):
        return self.children == {}

    def is_root(self):
        return self.parent is None

class MCTS:
    def __init__(self, policy_value_fn, c_puct=5, n_playout=1000):
        self.root = TreeNode(None, 1.0)
        self.policy_value_fn = policy_value_fn
        self.c_puct = c_puct
        self.n_playout = n_playout

    def _playout(self, state):
        node = self.root
        while not node.is_leaf():
            action, node = node.select(self.c_puct)
            state.do_move(action)

        action_probs, leaf_value = self.policy_value_fn(state)
        end, winner = state.game_end()
        if not end:
            node.expand(action_probs)
        else:
            if winner == -1:
                leaf_value = 0.0
            else:
                leaf_value = 1.0 if winner == state.get_current_player() else -1.0

        node.update_recursive(-leaf_value)

    def get_move_probs(self, state, temp=1e-3):
        for n in range(self.n_playout):
            state_copy = copy.deepcopy(state)
            self._playout(state_copy)

        act_visits = [(act, node.n_visits) for act, node in self.root.children.items()]
        acts, visits = zip(*act_visits)
        act_probs = softmax(1.0 / temp * np.log(np.array(visits) + 1e-10))
        return acts, act_probs

    def update_with_move(self, last_move):
        if last_move in self.root.children:
            self.root = self.root.children[last_move]
            self.root.parent = None
        else:
            self.root = TreeNode(None, 1.0)

def softmax(x):
    probs = np.exp(x - np.max(x))
    probs /= np.sum(probs)
    return probs
