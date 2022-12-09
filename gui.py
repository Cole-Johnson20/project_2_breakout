from tkinter import *
import csv

class GUI:
    """
    Class that sets up the gui in order to get the name of the player to put on the leaderboard,
     also inputs the player name and their score to the leaderboard.csv file
    """
    def __init__(self, screen, score):
        """
        Initializes the gui and displays it to the user
        :param screen: The window that the gui is in
        :param score: The score that the player achieved
        """
        self.score = score
        self.screen = screen

        self.frame_name = Frame(self.screen)
        self.label_name = Label(self.frame_name, text='Name (max 16 characters):')
        self.entry_name = Entry(self.frame_name)
        self.label_name.pack(padx=5, side='left')
        self.entry_name.pack(padx=5, side='left')
        self.frame_name.pack(anchor='w', pady=10)

        self.frame_button = Frame(self.screen)
        self.button_submit = Button(self.frame_button, text='SAVE', command=self.clicked)
        self.label_response = Label(self.frame_button, text='')
        self.button_submit.pack()
        self.label_response.pack()
        self.frame_button.pack()

    def clicked(self):
        """
        Gets the player name for the entry box and inputs it into the leaderboards.csv file, along with the player score
        """
        name = self.entry_name.get()
        try:
            if len(name) < 16:
                player = [name, self.score]
                with open('leaderboard.csv', 'a') as csvfile:
                    content = csv.writer(csvfile)
                    csvfile.write('\n')
                    content.writerow(player)
                    self.label_response.config(text='Name Submitted')
                    self.screen.destroy()

        except FileNotFoundError:
            self.label_response.config(text='File not found')
        except:
            self.label_response.config(text='Invalid Input')

