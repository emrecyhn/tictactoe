# from q_learning_agent import QLearningAgent
# from game import TicTacToe

# EPISODES = 50000
# SAVE_PATH = "q_table.pkl"

# def train():
#     env = TicTacToe()
#     agent = QLearningAgent()

#     for episode in range(EPISODES):
#         state = env.reset()
#         done = False
#         player = 1  # AI starts first

#         while not done:
#             actions = env.available_actions()
#             action = agent.choose_action(state, actions)
#             next_state, reward, done = env.step(action, player)
#             next_actions = env.available_actions() if not done else []

#             agent.update(state, action, reward if player == 1 else -reward, next_state, next_actions)

#             state = next_state
#             player *= -1  # switch turns

#         if (episode + 1) % 1000 == 0:
#             print(f"Episode {episode + 1}/{EPISODES}")

#     agent.save(SAVE_PATH)
#     print(f"Training completed. Q-table saved to {SAVE_PATH}")

# if __name__ == "__main__":
#     train()


# train_from_log.py
import csv
from q_learning_agent import QLearningAgent
from game import TicTacToe

LOG_FILE = "game_log.csv"
SAVE_PATH = "q_table.pkl"

def train_from_log():
    agent = QLearningAgent()
    try:
        agent.load(SAVE_PATH)
    except FileNotFoundError:
        print("Yeni Q-table oluşturulacak.")

    with open(LOG_FILE, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            timestamp, result, moves_str = row
            moves = eval(moves_str)  # [("human", (i,j)), ("ai", (i,j)), ...]

            env = TicTacToe()
            env.reset()
            state = env.board.copy()

            for i in range(len(moves)):
                player_str, action = moves[i]
                player = 1 if player_str == "ai" else -1

                next_state, reward, done = env.step(action, player)
                next_actions = env.available_actions() if not done else []

                if player == 1:
                    r = 1 if result == "win" else -1 if result == "lose" else 0
                    agent.update(state, action, r, next_state, next_actions)

                state = next_state

    agent.save(SAVE_PATH)
    print("Q-table güncellendi ve kaydedildi.")

if __name__ == "__main__":
    train_from_log()
