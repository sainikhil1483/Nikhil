import tkinter as tk
import random
import tkinter.messagebox

# List of words for the game
word_list = ["python", "hangman", "computer", "programming", "keyboard", "mouse", "monitor", "software", "developer", "algorithm"]

class HangmanGame:
    def __init__(self, master, mode):
        self.master = master
        self.master.title("Hangman Game")
        self.mode = mode
        self.word = random.choice(word_list)
        self.guesses = 8 if mode == 'classic' else float('inf')  # Guesses limit based on mode
        self.correct_guesses = 0
        self.word_display = ['_' for _ in self.word]
        self.guessed_letters = []
        self.parts_drawn = 0

        self.canvas = tk.Canvas(master, width=200, height=200)
        self.canvas.pack()

        self.word_label = tk.Label(master, text=' '.join(self.word_display), font=('Arial', 24))
        self.word_label.pack()

        self.guess_label = tk.Label(master, text=f'Guesses left: {self.guesses}', font=('Arial', 16))
        self.guess_label.pack()

        self.entry_label = tk.Label(master, text="Enter a letter:", font=('Arial', 16))
        self.entry_label.pack()

        self.entry = tk.Entry(master, font=('Arial', 16))
        self.entry.pack()

        self.guess_button = tk.Button(master, text="Guess", command=self.guess_letter, font=('Arial', 16))
        self.guess_button.pack()

        if self.mode == 'race':
            self.timer_label = tk.Label(master, text='Time left: 10', font=('Arial', 16))
            self.timer_label.pack()
            self.remaining_time = 10
            self.timer()

    def guess_letter(self):
        letter = self.entry.get().lower()
        if len(letter) != 1 or not letter.isalpha():
            tkinter.messagebox.showerror("Invalid Input", "Please enter a single letter.")
            return

        if letter in self.guessed_letters:
            tkinter.messagebox.showinfo("Already Guessed", "You have already guessed this letter.")
            return

        self.guessed_letters.append(letter)

        if letter in self.word:
            for i in range(len(self.word)):
                if self.word[i] == letter:
                    self.word_display[i] = letter
                    self.correct_guesses += 1
            self.word_label.config(text=' '.join(self.word_display))
        else:
            self.guesses -= 1
            self.draw_hangman()

        if self.correct_guesses == len(self.word):
            tkinter.messagebox.showinfo("Congratulations!", f"You've guessed the word: {self.word}")
            self.master.destroy()
            return
        elif self.guesses == 0:
            tkinter.messagebox.showinfo("Game Over", f"The word was: {self.word}")
            self.master.destroy()
            return

        self.guess_label.config(text=f'Guesses left: {self.guesses}')
        self.entry.delete(0, tk.END)

    def draw_hangman(self):
        parts = ["head", "body", "right_arm", "left_arm", "right_leg", "left_leg", "rope"]
        if self.parts_drawn < len(parts):
            part = parts[self.parts_drawn]
            if part == "rope":
                self.canvas.create_line(50, 20, 50, 50, width=3)
            else:
                draw_function = getattr(self, f"draw_{part}")
                draw_function()
            self.parts_drawn += 1

    def draw_head(self):
        self.canvas.create_oval(30, 50, 70, 90)

    def draw_body(self):
        self.canvas.create_line(50, 90, 50, 150)

    def draw_right_arm(self):
        self.canvas.create_line(50, 100, 80, 130)

    def draw_left_arm(self):
        self.canvas.create_line(50, 100, 20, 130)

    def draw_right_leg(self):
        self.canvas.create_line(50, 150, 80, 180)

    def draw_left_leg(self):
        self.canvas.create_line(50, 150, 20, 180)

    def draw_rope(self):
        self.canvas.create_line(50, 20, 50, 50, width=3)

    def timer(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.timer_label.config(text=f'Time left: {self.remaining_time}')
            self.master.after(1000, self.timer)
        else:
            self.guess_button.config(state='disabled')
            tkinter.messagebox.showinfo("Time's Up", f"Out of time! The word was: {self.word}")
            self.master.destroy()

def start_game(mode):
    root = tk.Tk()
    hangman_game = HangmanGame(root, mode)
    root.mainloop()

if __name__ == "__main__":
    start_game('classic')  # Change 'classic' to 'race' for race mode
