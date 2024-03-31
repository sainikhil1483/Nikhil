import tkinter as tk
import random
import tkinter.messagebox

class Game2048:
    def __init__(self, root, board_size=4):
        self.root = root
        self.root.title("2048 Game")
        self.board_size = board_size
        self.board = [[0] * self.board_size for _ in range(self.board_size)]
        self.empty_cells = [(i, j) for i in range(self.board_size) for j in range(self.board_size)]
        self.score = 0

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.canvas = tk.Canvas(self.frame, width=400, height=400, bg="lightgray")
        self.canvas.pack()

        self.score_label = tk.Label(self.root, text="Score: 0", font=("Helvetica", 14))
        self.score_label.pack()

        self.new_game_button = tk.Button(self.root, text="New Game", command=self.new_game)
        self.new_game_button.pack()

        self.new_game()

        # Bind arrow keys to move functions
        self.root.bind("<Left>", lambda event: self.move_left())
        self.root.bind("<Right>", lambda event: self.move_right())
        self.root.bind("<Up>", lambda event: self.move_up())
        self.root.bind("<Down>", lambda event: self.move_down())

    def new_game(self):
        self.board = [[0] * self.board_size for _ in range(self.board_size)]
        self.empty_cells = [(i, j) for i in range(self.board_size) for j in range(self.board_size)]
        self.score = 0
        self.add_random_tile()
        self.add_random_tile()
        self.draw_board()

    def add_random_tile(self):
        if self.empty_cells:
            row, col = random.choice(self.empty_cells)
            self.board[row][col] = 2 if random.random() < 0.9 else 4
            self.empty_cells.remove((row, col))

    def draw_board(self):
        self.canvas.delete("all")
        cell_size = 400 // self.board_size
        for i in range(self.board_size):
            for j in range(self.board_size):
                x0, y0 = j * cell_size, i * cell_size
                x1, y1 = (j + 1) * cell_size, (i + 1) * cell_size
                value = self.board[i][j]
                color = "#eee4da" if value == 0 else "#%02x%02x%02x" % ((1 << (value % 11 + 7)) & 255, (1 << (value % 11 + 11)) & 255, (1 << (value % 11 + 13)) & 255)
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="gray")
                if value != 0:
                    self.canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=str(value), font=("Helvetica", 24, "bold"))

        self.score_label.config(text="Score: {}".format(self.score))

    def merge(self, row):
        i = 0
        while i < self.board_size - 1:
            if row[i] == row[i + 1] and row[i] != 0:
                row[i] *= 2
                self.score += row[i]
                row[i + 1] = 0
                i += 2
            else:
                i += 1

    def transpose_board(self):
        self.board = [list(row) for row in zip(*self.board)]

    def move_left(self):
        for row in self.board:
            self.merge(row)
        self.empty_cells = [(i, j) for i in range(self.board_size) for j in range(self.board_size) if self.board[i][j] == 0]
        self.add_random_tile()
        self.draw_board()
        if not self.empty_cells:
            self.check_game_over()

    def move_right(self):
        self.reverse_rows()
        self.move_left()
        self.reverse_rows()

    def move_up(self):
        self.transpose_board()
        self.move_left()
        self.transpose_board()

    def move_down(self):
        self.transpose_board()
        self.reverse_rows()
        self.move_left()
        self.reverse_rows()
        self.transpose_board()

    def reverse_rows(self):
        for row in self.board:
            row.reverse()

    def check_game_over(self):
        for i in range(self.board_size):
            for j in range(self.board_size - 1):
                if self.board[i][j] == self.board[i][j + 1] or self.board[j][i] == self.board[j + 1][i]:
                    return
        self.end_game()

    def end_game(self):
        self.new_game_button.config(state="disabled")
        tkinter.messagebox.showinfo("Game Over", "No more moves possible! Game Over.")

root = tk.Tk()
game = Game2048(root)
root.mainloop()
