# gui_play.py
import tkinter as tk
import csv
import datetime
from game import TicTacToe
from q_learning_agent import QLearningAgent

CELL_SIZE = 100
MODEL_PATH = "q_table.pkl"
LOG_FILE = "game_log.csv"

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe AI")

        self.moves = []  # hamleleri tutmak için liste

        self.selection_frame = tk.Frame(root)
        self.selection_frame.pack()
        tk.Label(self.selection_frame, text="Kim olarak oynamak istiyorsun?").pack(side=tk.LEFT)
        tk.Button(self.selection_frame, text="X (ilk oynar)", command=lambda: self.start_game(1)).pack(side=tk.LEFT)
        tk.Button(self.selection_frame, text="O (ikinci oynar)", command=lambda: self.start_game(-1)).pack(side=tk.LEFT)

        self.canvas = tk.Canvas(root, width=300, height=300)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.human_move)

        self.restart_button = tk.Button(root, text="Yeniden Başlat", command=self.restart_game)
        self.restart_button.pack()

        self.explanation_label = tk.Label(root, text="", font=("Arial", 12))
        self.explanation_label.pack()

        self.log_button = tk.Button(root, text="Oyun Geçmişini Göster", command=self.show_log)
        self.log_button.pack()

        self.log_listbox = tk.Listbox(root, width=50)
        self.log_listbox.pack()

        self.env = TicTacToe()
        self.agent = QLearningAgent()
        self.agent.load(MODEL_PATH)
        self.state = self.env.reset()
        self.human = None
        self.player = 1
        self.draw_board()

    def start_game(self, human_choice):
        self.human = human_choice
        self.player = 1
        self.selection_frame.pack_forget()
        if self.player != self.human:
            self.ai_move()

    def draw_board(self):
        self.canvas.delete("all")
        for i in range(1, 3):
            self.canvas.create_line(i * CELL_SIZE, 0, i * CELL_SIZE, 300)
            self.canvas.create_line(0, i * CELL_SIZE, 300, i * CELL_SIZE)

        for i in range(3):
            for j in range(3):
                x = j * CELL_SIZE + 50
                y = i * CELL_SIZE + 50
                if self.env.board[i, j] == 1:
                    self.canvas.create_text(x, y, text='X', font=("Arial", 32))
                elif self.env.board[i, j] == -1:
                    self.canvas.create_text(x, y, text='O', font=("Arial", 32))

    def human_move(self, event):
        if self.env.done or self.player != self.human:
            return
        i = event.y // CELL_SIZE
        j = event.x // CELL_SIZE
        if (i, j) in self.env.available_actions():
            self.state, _, _ = self.env.step((i, j), self.human)
            self.moves.append(("human", (i, j)))
            self.draw_board()
            self.player *= -1
            if not self.env.done:
                self.root.after(500, self.ai_move)
            else:
                self.show_result()

    def ai_move(self):
        if self.env.done:
            return
        action = self.agent.choose_action(self.state, self.env.available_actions())
        reason = self.explain_ai_action(action)
        self.state, _, _ = self.env.step(action, 1)
        self.moves.append(("ai", action))
        self.draw_board()
        self.explanation_label.config(text=reason)
        self.player *= -1
        if self.env.done:
            self.show_result()

    def explain_ai_action(self, action):
        temp_env = TicTacToe()
        temp_env.board = self.env.board.copy()
        temp_env.step(action, 1)
        if temp_env.done and temp_env.winner == 1:
            return "Kazandıran hamleyi yaptı."

        temp_env = TicTacToe()
        temp_env.board = self.env.board.copy()
        temp_env.step(action, -1)
        if temp_env.done and temp_env.winner == -1:
            return "Kazandıracak hamleni engelledi."

        return "En iyi skora sahip hamleyi yaptı."

    def show_result(self):
        msg = "Berabere!"
        result = "draw"
        if self.env.winner == self.human:
            msg = "Kazandın!"
            result = "win"
        elif self.env.winner == -self.human:
            msg = "Kaybettin!"
            result = "lose"
        self.canvas.create_text(150, 150, text=msg, font=("Arial", 24), fill="red")
        self.log_result(result)

    def log_result(self, result):
        now = datetime.datetime.now().isoformat()
        with open(LOG_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([now, result, self.moves])

    def show_log(self):
        self.log_listbox.delete(0, tk.END)
        try:
            with open(LOG_FILE, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    timestamp, result, _ = row
                    self.log_listbox.insert(tk.END, f"{timestamp}: {result}")
        except FileNotFoundError:
            self.log_listbox.insert(tk.END, "Log dosyası bulunamadı.")

    def restart_game(self):
        self.env.reset()
        self.state = self.env.board.copy()
        self.player = 1
        self.moves = []
        self.draw_board()
        self.explanation_label.config(text="")
        self.selection_frame.pack()

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeGUI(root)
    root.mainloop()
