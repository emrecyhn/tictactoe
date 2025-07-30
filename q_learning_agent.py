# q_learning_agent.py
import numpy as np
import random
import pickle

class QLearningAgent:
    def __init__(self, alpha=0.5, gamma=0.9, epsilon=1.0, epsilon_decay=0.9995, epsilon_min=0.1):
        self.q_table = {}  # state -> action values
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min

    def get_state_key(self, board):
        return tuple(board.reshape(9))

    def choose_action(self, board, actions):
        state_key = self.get_state_key(board)
        if random.random() < self.epsilon:
            return random.choice(actions)

        if state_key not in self.q_table:
            self.q_table[state_key] = {a: 0.0 for a in actions}

        q_values = self.q_table[state_key]
        max_q = max(q_values.values())
        best_actions = [a for a, q in q_values.items() if q == max_q]
        return random.choice(best_actions)

    def update(self, board, action, reward, next_board, next_actions):
        state_key = self.get_state_key(board)
        next_key = self.get_state_key(next_board)

        if state_key not in self.q_table:
            self.q_table[state_key] = {a: 0.0 for a in [action]}
        if next_key not in self.q_table:
            self.q_table[next_key] = {a: 0.0 for a in next_actions}

        current_q = self.q_table[state_key].get(action, 0.0)
        max_future_q = max(self.q_table[next_key].values()) if next_actions else 0.0

        new_q = current_q + self.alpha * (reward + self.gamma * max_future_q - current_q)
        self.q_table[state_key][action] = new_q

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def save(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.q_table, f)

    def load(self, filename):
        with open(filename, 'rb') as f:
            self.q_table = pickle.load(f)
