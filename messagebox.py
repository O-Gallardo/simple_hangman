from tkinter import *
import tkinter.messagebox
import time

class MessageBox():
    def __init__(self, master):
        """Sets the attributes for the messagebox."""
        self.master = master
        self.wmessage = "Congratulations, You win! Do you want to play again?"
        self.lmessage = ""

    def message_win(self, hangman):
        """Opens a message box that congratulates the player."""
        messagew = tkinter.messagebox.askyesno(title = None, message = self.wmessage)
        if messagew:
            time.sleep(0.5)
            hangman.replay()
            hangman.stage_image.grid_forget()
            hangman.display_widgets()
        elif not messagew:
            self.master.quit()

    def message_lose(self, hangman):
        """Opens a message box that tells the player that he lost."""
        messagel = tkinter.messagebox.askyesno(title = None, message = self.lmessage)
        if messagel:
            hangman.replay()
            hangman.stage_image.grid_forget()
            hangman.display_widgets()
        elif not messagel:
            self.master.quit()

    def replay_score(score, hangman):
        """Sets the score to zero if the player clicks the replay button."""
        r_message = tkinter.messagebox.askyesno(
            message="Are you sure you want to replay? Replay will reset your current score.")
        if r_message:
            score.current_total_score = 0
            score.score_display.config(text="SCORE:  " + str(score.current_total_score))
            hangman.replay()
            
if __name__ == "__main__":
	main()
