import random
from words import word_list
from tkinter import *
from PIL import ImageTk, Image
from string import ascii_uppercase
import time
import tkinter.messagebox
from messagebox import MessageBox
from score import Score

root = Tk()
root.title("Hangman")
root.config(bg = "black")
wlist = word_list
root.iconbitmap("./icon.ico")

class MainGame():
    def __init__(self, master, wlist):
        """Sets the attributes for the hangman game."""
        self.master = master
        self.counter = 0
        self.win_count = 0
        self.wlist = wlist
        self.word = random.choice(wlist)
        self.word = self.word.upper()
        self.word_letters = set(self.word)
        self.button = Button(master)
        self.guessed_letters = set()

        # Prepares the images for the stage.
        stage_1 = ImageTk.PhotoImage(Image.open("stage_1.jpg"))
        stage_2 = ImageTk.PhotoImage(Image.open("stage_2.jpg"))
        stage_3 = ImageTk.PhotoImage(Image.open("stage_3.jpg"))
        stage_4 = ImageTk.PhotoImage(Image.open("stage_4.jpg"))
        stage_5 = ImageTk.PhotoImage(Image.open("stage_5.jpg"))
        stage_6 = ImageTk.PhotoImage(Image.open("stage_6.jpg"))
        stage_7 = ImageTk.PhotoImage(Image.open("stage_7.jpg"))

        # Stores the images in a list so that it could be accessed using their index.
        self.stages = [
            stage_1, stage_2,
            stage_3, stage_4,
            stage_5, stage_6,
            stage_7
        ]

        # Prepares the text display for the secret word.
        self.stage_image = Label(self.master, image=self.stages[self.counter], bg = "black")
        self.set_blanks_list = ["_" for letter in self.word]
        self.set_blanks = "  ".join(self.set_blanks_list)
        self.word_display = Label(self.master, text = self.set_blanks, bg = "black", fg = "white", font=(None, 25))
        self.win_display = Label(self.master, text = "W I N S T R E A K:   " + str(self.win_count),
                                 bg = "grey", fg = "white", font=(None, 12))

    def display_widgets(self):
        """Displays the widget into the master window."""
        self.stage_image.grid(row=0, columnspan=9)
        self.word_display.grid(row=1, columnspan = 9, sticky=[W, E])
        self.win_display.grid(row=5, columnspan =9, sticky =[W, E])
        button_replay = Button(self.master, text="REPLAY", command = lambda:[replay_score(score, hangman)],
                               padx = 20, pady = 20, width = 3, bg = "grey", fg = "white")
        button_replay.grid(row=4, column=8)

    def add_buttons(self, hangman, message, master):
        """Adds the buttons for the letters."""
        self.button_list = []
        n = 0
        for l in ascii_uppercase:
            self.button = Button(self.master, text=l, padx=20, pady=20, width=3, bg="grey", fg = "white",
                            command=lambda l=l: [self.switch(l), game_play(l, hangman, message, master, score)], state = NORMAL)
            self.button_list.append(self.button)
            self.button.grid(row=2 + (n // 9), column=n % 9)
            n += 1

    def switch(self, letter):
        """Disables a button after click."""
        i = ascii_uppercase.index(letter)
        button_normal = self.button_list[i]
        if button_normal["state"] == NORMAL:
            button_normal.config(state = DISABLED)
            button_normal.config(bg = "black")

    def replay(self):
        """Replays the game."""
        self.word_letters.clear()
        self.guessed_letters.clear()
        self.counter = 0
        self.word = random.choice(self.wlist)
        self.word = self.word.upper()
        self.word_letters = set(self.word)
        self.stage_image.grid_forget()
        self.stage_image = Label(root, image = self.stages[self.counter], bg = "black")
        self.word_display.grid_forget()
        self.set_blanks_list = ["_" for letter in self.word]
        self.set_blanks = "  ".join(self.set_blanks_list)
        self.word_display.grid_forget()
        self.word_display = Label(self.master, text=(self.set_blanks), bg ="black", fg = "white", font=(None, 25))
        for b in self.button_list:
            if b["state"] == DISABLED:
                b.config(state = NORMAL, bg = "grey", fg = "white")
        self.display_widgets()

def replay_win_count(hangman):
    """Resets the win count."""
    hangman.win_count = 0
    hangman.win_display.config(text="W I N S T R E A K:   " + str(hangman.win_count))

def replay_score(score, hangman):
    """Sets the score to zero if the player clicks the replay button."""
    r_message = tkinter.messagebox.askyesno(message = "Are you sure you want to replay? Replay will reset your current score.")
    if r_message:
        score.current_total_score = 0
        score.score_display.config(text = "SCORE:  " + str(score.current_total_score))
        replay_win_count(hangman)
        hangman.replay()

def game_play(letter, hangman, message, root, score):
    """Establishes the game mechanics."""
    time.sleep(0.15)
    hangman.guessed_letters.add(letter)
    hangman.user_letters = [letter if letter in hangman.guessed_letters else "_" for letter in hangman.word]
    hangman.word_user = "  ".join(hangman.user_letters)
    hangman.word_display.config(text = hangman.word_user)
    current_score = (100 - int((hangman.counter * 10)))

    if "_" not in hangman.user_letters:
        time.sleep(0.5)
        message.message_win(hangman)
        score.current_total_score += int(current_score)
        score.score_display.config(text = "SCORE:  " + str(score.current_total_score))
        score.show_score()
        score.save_hscore()
        hangman.win_count += 1
        hangman.win_display.config(text="W I N S T R E A K:   " + str(hangman.win_count))
    elif letter not in hangman.word_letters:
        hangman.counter += 1
        hangman.stage_image.grid_forget()
        hangman.stage_image = Label(root, image = hangman.stages[hangman.counter], bg = "black")
        hangman.stage_image.grid(row = 0, columnspan = 9)
        if hangman.counter == (len(hangman.stages) - 1):
            time.sleep(0.5)
            message.lmessage = f"Sorry, You lose the game. Your total current score has been reset. The word is {hangman.word}. Do you want to play again?"
            message.message_lose(hangman)
            score.save_hscore()
            score.current_total_score = 0
            score.score_display.config(text="SCORE:  " + str(score.current_total_score))
            replay_win_count(hangman)

### SETTING INSTANCES OF THE CLASSES ABOVE ###
hangman = MainGame(root, wlist)
hangman.display_widgets()
message = MessageBox(root)
hangman.add_buttons(hangman, message, root)
score = Score(root)
score.load_hscore()
score.show_score()

### END OF GAMELOOP ###
root.mainloop()

       
if __name__ == "__main__":
	pass

