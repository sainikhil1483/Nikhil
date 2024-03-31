import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tic Tac Toe")
        self.game_over = False
        self.create_widgets()
        self.start_new_game()

    def create_widgets(self):
        self.buttons = []
        for i in range(3):
            row_buttons = []
            for j in range(3):
                button = tk.Button(self, text=' ', font=('Arial', 20), width=6, height=2,
                                   command=lambda row=i, col=j: self.button_click(row, col))
                button.grid(row=i, column=j, sticky='snew')
                row_buttons.append(button)
            self.buttons.append(row_buttons)

        self.player_turn_label = tk.Label(self, text="   Your turn!   ", font=('Arial', 12))
        self.player_turn_label.grid(row=3, column=0, columnspan=3, sticky='snew')

        self.player_details_label = tk.Label(self, text="    You are X\n\n    Computer is O", font=('Arial', 12))
        self.player_details_label.grid(row=4, column=0, columnspan=3, sticky='snew')

        self.restart_button = tk.Button(self, text='Restart', font=('Arial', 12), command=self.start_new_game)
        self.restart_button.grid(row=5, column=0, columnspan=3, sticky='snew')

    def start_new_game(self):
        self.game_over = False
        self.player_turn_label.config(text="   Your turn!   ")
        for row_buttons in self.buttons:
            for button in row_buttons:
                button.config(text=' ', state='normal')

    def button_click(self, row, col):
        if self.buttons[row][col]['text'] == ' ' and not self.game_over:
            self.buttons[row][col]['text'] = "X"
            if self.check_win("X"):
                self.end_game("Congratulations! You win!")
                return
            elif all(self.buttons[i][j]['text'] != ' ' for i in range(3) for j in range(3)):
                self.end_game("Match is Draw.")
                return
            self.player_turn_label.config(text="   Computer's turn!   ")
            self.after(1000, self.computer_move)

    def computer_move(self):
        empty_cells = [(i, j) for i in range(3) for j in range(3) if self.buttons[i][j]['text'] == ' ']
        if empty_cells:
            cell = random.choice(empty_cells)
            self.buttons[cell[0]][cell[1]]['text'] = "O"
            if self.check_win("O"):
                self.end_game("Computer wins!")
                return
        else:
            self.end_game("Match is Draw.")
            return
        self.player_turn_label.config(text="   Your turn!   ")

    def check_win(self, player):
        # Check rows, columns, and diagonals for a win
        for i in range(3):
            if all(self.buttons[i][j]['text'] == player for j in range(3)) or \
               all(self.buttons[j][i]['text'] == player for j in range(3)):
                return True
        if all(self.buttons[i][i]['text'] == player for i in range(3)) or \
           all(self.buttons[i][2 - i]['text'] == player for i in range(3)):
            return True
        return False

    def end_game(self, message):
        self.game_over = True
        for row_buttons in self.buttons:
            for button in row_buttons:
                button.config(state='disabled')
        messagebox.showinfo("Tic Tac Toe", message)

if __name__ == "__main__":
    game = TicTacToe()
    game.mainloop()
