# play_vs_ai.py
from q_learning_agent import QLearningAgent
from game import TicTacToe

MODEL_PATH = "q_table.pkl"

def get_human_move(actions):
    print("Geçerli hamleler:", actions)
    while True:
        try:
            move = input("Hamleni gir (örnek: 0 1): ")
            i, j = map(int, move.strip().split())
            if (i, j) in actions:
                return (i, j)
            else:
                print("Geçersiz hamle. Tekrar dene.")
        except Exception:
            print("Format yanlış. Örnek: 0 1")

def play():
    env = TicTacToe()
    agent = QLearningAgent()
    agent.load(MODEL_PATH)

    state = env.reset()
    player = 1
    human = int(input("X için 1, O için -1 girin (X ilk oynar): "))

    env.render()

    while not env.done:
        if player == human:
            action = get_human_move(env.available_actions())
        else:
            action = agent.choose_action(state, env.available_actions())
            print(f"AI'nin hamlesi: {action}")

        state, reward, done = env.step(action, player)
        env.render()

        player *= -1

    if env.winner == human:
        print("Kazandın!")
    elif env.winner == -human:
        print("Kaybettin!")
    else:
        print("Berabere.")

if __name__ == "__main__":
    play()
