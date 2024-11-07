import tkinter as tk
import tkinter.ttk as ttk
import random
from tkinter import messagebox
from tkinter import font
import math
import unidecode
import keyboard as key
import matplotlib.pyplot as plt

# Define the global variables


class WordleApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Wordle")
        self.root.configure(background="black")
        self.root.geometry("800x400")
        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(
            self.root,
            text="Welcome to Wordle!\n Please enter your chosen language and word length.",
            foreground="white",
            font=("Garamond", 16),
            background="black",
            width=50,
            height=2,
        )
        label2 = tk.Label(
            self.root,
            text="*Note: The word length must be between 4 and 7.\n**Note: All accents are stripped.",
            foreground="grey",
            font=("Garamond", 10),
            background="black",
            width=50,
            height=3,
        )

        # Input fields
        self.entry = tk.Entry(self.root, width=20, font=("Garamond", 16))
        self.entry.insert(0, "Enter word length")

        self.combo = ttk.Combobox(
            self.root,
            width=20,
            values=["English", "Francais", "Espanol", "Deutsch"],
            font=("Garamond", 16),
            state="readonly",
        )
        submit_button = tk.Button(
            self.root, text="Submit", font=("Garamond", 16), command=self.on_submit
        )

        # Pack the widgets
        label.pack(pady=20)
        label2.pack()
        self.entry.pack(pady=10)
        self.combo.pack(pady=10)
        submit_button.pack(pady=20)

        self.root.mainloop()

    def on_submit(self):
        language = self.combo.get()
        try:
            word_length = int(self.entry.get())
            if 4 <= word_length <= 7:
                self.root.destroy()
                WordleGame(word_length, language, "Garamond")
            else:
                messagebox.showerror(
                    "Error", "Please enter a word length between 4 and 7."
                )
        except ValueError:
            messagebox.showerror("Error", "Invalid word length. Please enter a number.")


class WordleGame:
    global jolly

    def __init__(self, word_length, language, jolly):
        self.word_length = word_length
        self.language = language
        self.current_guess = 0
        self.num_guesses = word_length + 1

        self.window = tk.Tk()
        self.window.title("Wordle (test)")
        self.window.configure(background="black")
        self.window.geometry(f"{int(word_length * 52 + 255)}x{word_length * 100 + 200}")
        self.window.resizable(False, False)
        self.word_entry = tk.Entry(
            self.window,
            width=20,
            borderwidth=5,
            foreground="black",
            background="white",
            font=(jolly, 24),
        )
        self.word_entry.grid(row=1, column=0, pady=10)

        self.grid_frame = tk.Frame(self.window)
        self.grid_frame.grid(row=0, column=0, padx=120, pady=60)

        self.load_words()
        self.create_grid()
        self.virtual_keyboard()
        key.add_hotkey("enter", self.on_guess)

        self.window.mainloop()

    def load_words(self):
        try:
            if self.language == "English":
                with open("en.txt", "r", encoding="UTF-8") as f:
                    words = f.readlines()
            elif self.language == "Francais":
                with open("fr.txt", "r", encoding="UTF-8") as f:
                    words = f.readlines()
            elif self.language == "Espanol":
                with open("es.txt", "r", encoding="UTF-8") as f:
                    words = f.readlines()
            elif self.language == "Deutsch":
                with open("de.txt", "r", encoding="UTF-8") as f:
                    words = f.readlines()
            else:
                raise ValueError("Unsupported language selected.")
        except FileNotFoundError:
            messagebox.showerror("Error", "Word file not found!")
            self.window.destroy()
            return

        filtered_words = [
            w.strip() for w in words if len(w.strip()) == self.word_length
        ]
        self.word = unidecode.unidecode(random.choice(filtered_words))
        print(f"Selected word: {self.word}")

    def create_grid(self):
        self.boxes = [
            [None for _ in range(self.word_length)] for _ in range(self.num_guesses)
        ]
        self.images = [
            tk.PhotoImage(width=1, height=1)
            for _ in range(self.word_length * self.num_guesses)
        ]

        for x in range(self.num_guesses):
            for y in range(self.word_length):
                self.boxes[x][y] = tk.Label(
                    self.grid_frame,
                    image=self.images[x * self.word_length + y],
                    width=50,
                    height=50,
                    borderwidth=2,
                    relief="solid",
                    background="grey",
                    font=("Garamond", 36),
                    text=" ",
                    foreground="white",
                    compound="center",
                )
                self.boxes[x][y].grid(
                    row=x, column=y + math.ceil(self.word_length / 2), sticky=""
                )

    def virtual_keyboard(self):
        keyboard_frame = tk.Frame(self.window)
        keyboard_frame.grid(row=2, column=0, pady=20)

        self.keyboxes = [None for _ in range(26)]
        for i in range(26):
            letter = chr(65 + i)
            if i < 13:
                row = 2
                col = i
            if i >= 13:
                row = 3
                col = i - 13
            self.keyboxes[i] = tk.Label(
                keyboard_frame,
                text=letter,
                width=2,
                height=1,
                borderwidth=1,
                relief="solid",
                background="grey",
                font=("Garamond", 16),
                compound="center",
                foreground="white",
            )
            print(row, col)
            self.keyboxes[i].grid(row=row, column=col)
            self.window.columnconfigure(col, weight=1)

    def on_guess(self):
        guess = self.word_entry.get().strip().lower()
        if len(guess) != self.word_length:
            messagebox.showerror("Warning", f"Enter a {self.word_length}-letter word.")
            return

        for i in range(self.word_length):
            if guess[i] == self.word[i]:
                color = "olivedrab"
            elif guess[i] in self.word:
                color = "goldenrod"
            else:
                color = "grey"
            self.boxes[self.current_guess][i].config(
                background=color,
                text=guess[i].upper(),
            )
            for j in range(26):
                if self.keyboxes[j].cget("text").lower() == guess[i]:
                    self.keyboxes[j].config(background=color)
        if guess == self.word:

            def destroyAll():
                victoryMessage.destroy()
                self.window.destroy()

            def playAgain():

                self.window.destroy()
                WordleApp()
                victoryMessage.destroy()

            victoryMessage = tk.Tk()
            tk.Label(victoryMessage, text="You win!").pack()
            tk.Button(victoryMessage, text="Exit", command=destroyAll).pack()
            tk.Button(victoryMessage, text="Play again", command=playAgain).pack()

            victoryMessage.mainloop()
        self.current_guess += 1
        if self.current_guess >= self.num_guesses:
            messagebox.showinfo("Game Over", f"The word was: {self.word}")
            self.window.destroy()


# Run the app
WordleApp()
