import numpy as np

class TicTacToe:
    def __init__(self):
        self.reset()

    def reset(self):
        self.board = np.zeros((3, 3), dtype=int)  # 0: boş, 1: X, -1: O
        self.done = False
        self.winner = None
        return self.board.copy()

    def available_actions(self):
        return [(i, j) for i in range(3) for j in range(3) if self.board[i, j] == 0]

    def step(self, action, player):
        if self.done:
            raise ValueError("Oyun bitti")

        i, j = action
        if self.board[i, j] != 0:
            raise ValueError("Geçersiz hamle")

        self.board[i, j] = player
        self.winner = self.check_winner()
        self.done = self.winner is not None or len(self.available_actions()) == 0
        reward = self.get_reward(player)
        return self.board.copy(), reward, self.done

    def get_reward(self, player):
        if self.winner == player:
            return 1
        elif self.winner == -player:
            return -1
        else:
            return 0

    def check_winner(self):
        lines = []
        lines.extend(self.board)                          # satırlar
        lines.extend(self.board.T)                        # sütunlar
        lines.append(np.diag(self.board))                # köşegen
        lines.append(np.diag(np.fliplr(self.board)))     # ters köşegen

        for line in lines:
            if np.all(line == 1):
                return 1
            elif np.all(line == -1):
                return -1
        return None

    def render(self):
        symbol_map = {1: 'X', -1: 'O', 0: '.'}
        for row in self.board:
            print(' '.join(symbol_map[val] for val in row))
        print()


