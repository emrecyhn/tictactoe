# eval.py
from q_learning_agent import QLearningAgent
from game import TicTacToe
import random

MODEL_PATH = "q_table.pkl"
GAMES = 1000

def random_player(actions):
    return random.choice(actions)

def evaluate():
    agent = QLearningAgent()
    agent.load(MODEL_PATH)
    
    results = {"win": 0, "lose": 0, "draw": 0}

    for _ in range(GAMES):
        env = TicTacToe()
        state = env.reset()
        player = 1

        while not env.done:
            actions = env.available_actions()
            if player == 1:
                action = agent.choose_action(state, actions)
            else:
                action = random_player(actions)

            state, reward, done = env.step(action, player)
            player *= -1

        if env.winner == 1:
            results["win"] += 1
        elif env.winner == -1:
            results["lose"] += 1
        else:
            results["draw"] += 1

    print(f"{GAMES} oyun sonunda sonuçlar:")
    print(f"Kazandı: {results['win']}")
    print(f"Kaybetti: {results['lose']}")
    print(f"Beraberlik: {results['draw']}")

if __name__ == "__main__":
    evaluate()
