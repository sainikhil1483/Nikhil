from tkinter import *
from tkinter import ttk, messagebox

root = Tk()
root.title("Tic Tac Toe")

# Game variables
current_player = "X"
game_board = [[" " for _ in range(3)] for _ in range(3)]
buttons = []

# Function to handle button click
def button_click(row, col):
    global current_player
    if game_board[row][col] == " ":
        buttons[row][col].config(text=current_player)
        game_board[row][col] = current_player
        if check_winner():
            messagebox.showinfo("Tic Tac Toe", f"Player {current_player} wins!")
            reset_game()
        elif is_board_full():
            messagebox.showinfo("Tic Tac Toe", "Match is Draw.")
            reset_game()
        else:
            current_player = "O" if current_player == "X" else "X"
            player_turn_label.config(text=f"Player {current_player} turn")

# Function to check for a winner
def check_winner():
    for i in range(3):
        if game_board[i][0] == game_board[i][1] == game_board[i][2] != " ":
            return True
        if game_board[0][i] == game_board[1][i] == game_board[2][i] != " ":
            return True
    if game_board[0][0] == game_board[1][1] == game_board[2][2] != " ":
        return True
    if game_board[0][2] == game_board[1][1] == game_board[2][0] != " ":
        return True
    return False

# Function to check if the board is full
def is_board_full():
    for row in game_board:
        if " " in row:
            return False
    return True

# Function to reset the game
def reset_game():
    global current_player, game_board
    current_player = "X"
    game_board = [[" " for _ in range(3)] for _ in range(3)]
    for row in buttons:
        for button in row:
            button.config(text=" ", state="normal")
    player_turn_label.config(text="Player X turn")

# Create buttons and labels
for i in range(3):
    button_row = []
    for j in range(3):
        button = ttk.Button(root, text=" ", command=lambda row=i, col=j: button_click(row, col))
        button.grid(row=i, column=j, sticky="snew", ipadx=40, ipady=40)
        button_row.append(button)
    buttons.append(button_row)

player_turn_label = ttk.Label(root, text="Player X turn")
player_turn_label.grid(row=3, column=0, columnspan=3, sticky="snew", ipadx=40, ipady=10)

reset_button = ttk.Button(root, text="Restart", command=reset_game)
reset_button.grid(row=4, column=0, columnspan=3, sticky="snew", ipadx=40, ipady=10)

root.mainloop()
