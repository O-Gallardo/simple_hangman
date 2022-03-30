from tkinter import *
import json

class Score():
    def __init__(self, master):
        """Sets the attribute for the scoring system."""
        self.master = master
        self.current_total_score = 0
        self.highscore = 0
        self.score_display = Label(self.master, text = "SCORE:  " + str(self.current_total_score), bg = "black", fg = "white")
        self.hscore_display = Label(self.master, text = "HIGHSCORE:  " + str(self.highscore), bg = "black", fg = "white")

    def load_hscore(self):
        """Loads the high score saved in the json file."""
        with open("highscore.json", "r") as hs:
            self.highscore = json.load(hs)
            return self.highscore

    def show_score(self):
        """Displays the score in the window."""
        self.highscore = self.load_hscore()
        if self.current_total_score >= self.highscore:
            self.hscore_display.grid_forget()
            self.hscore_display.config(text = "HIGHSCORE:  " + str(self.current_total_score))
        else:
            self.hscore_display.config(text = "HIGHSCORE:  " + str(self.load_hscore()))
        self.score_display.grid(row = 6, sticky = W, columnspan = 9)
        self.hscore_display.grid(row = 7, sticky = W, columnspan = 9)

    def save_hscore(self):
        """Stores the score in a json file if the user outscored the current highscore."""
        if self.current_total_score >= self.highscore:
            with open("highscore.json", "w") as f_obj:
                json.dump(self.current_total_score, f_obj)
                
try:         
	if __name__ == "__main__":
		main()
except NameError:
	print("Please run the main module") 
