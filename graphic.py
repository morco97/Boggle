# Intro2cs, 67101-2
# Exercise 12: Boggle
# By: Mor Cohen

import ex12_utils as ex
import tkinter as tk
from boggle_helper import *

# ------------------------------CONSTANTS--------------------------------------
FRAME_BG = 'seashell2'
FRAME_HL_BG = 'azure'
FONT = ("Time", 20)
DEFAULT_TEXT = 'You Can Do It'
THREE_MINUTES = 180  # in seconds
# -----------------------------------------------------------------------------


class GUI:
    """
    this class contains the graphic part of the game boggle
    """

    def __init__(self):
        self.started = False  # a flag that tells if the timer started
        self.new_game = False  # flag that tells if the game is not the first
        root = tk.Tk()
        root.title("The Boggle Game")
        root.geometry('900x600')
        self.main_window = root
        root.resizable(False, False)
        # -----------------------------
        self.words = load_words()
        self.board = load_board()
        # -----------------------------
        self.clicked_cells = []
        self.chosen_letters = ''
        self.found_words = []
        self.score = 0
        self.last_score = 0
        # -----------------------------
        self.frames()
        self.buttons()
        self.labels()

    def frames(self):
        """
        these methods make the frames of the board- linked to the main window
        """
        # right side of the board
        self.boards_right_side = tk.Frame(self.main_window, width=10,
                                          height=10, bg=FRAME_BG,
                                          highlightbackground=FRAME_HL_BG,
                                          highlightthickness=2)
        self.boards_right_side.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
        # upper part of the board
        self.upper_board = tk.Frame(self.main_window, width=50, height=50,
                                    bg=FRAME_BG,
                                    highlightbackground=FRAME_HL_BG,
                                    highlightthickness=5)
        self.upper_board.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        # lower part of the board
        self.lower_board = tk.Frame(self.main_window, width=50, height=50,
                                    bg=FRAME_BG,
                                    highlightbackground=FRAME_HL_BG,
                                    highlightthickness=5)
        self.lower_board.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        # middle "main" part of the board
        self.main_board = tk.Frame(self.main_window, bg=FRAME_BG,
                                   highlightbackground=FRAME_HL_BG,
                                   highlightthickness=5)
        self.main_board.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    def buttons(self):
        """
        these methods make the buttons of the board- linked to the frames
        """
        # self.new_game_button = tk.Button(self.upper_board, font=FONT,
        #                                  bg='SeaGreen1',
        #                                  text='Boggle',
        #                                  command=lambda: self.start_over())
        self.new_game_button = tk.Button(self.upper_board, font=FONT,
                                         bg='white', fg='black',
                                         text='Boggle',
                                         command=lambda: self.start_over())
        self.new_game_button.pack(side=tk.TOP, fill=tk.X, expand=False)
        # self.message_slot_button = tk.Button(self.upper_board,
        #                                      font=FONT,
        #                                      bg="sky blue", width=30,
        #                                      text='Press To Start',
        #                                      command=lambda:
        #                                      self.start())
        self.message_slot_button = tk.Button(self.upper_board,
                                             font=FONT,
                                             bg="green", fg='white', width=30,
                                             text='Press To Start',
                                             command=lambda:
                                             self.start())
        self.message_slot_button.pack(side=tk.TOP, fill=tk.X, expand=True)
        # self.erase_button = tk.Button(self.lower_board,
        #                               font=FONT,
        #                               bg="maroon", fg="white", width=10,
        #                               relief="raised",
        #                               text="Erase",
        #                               command=lambda: self.erase())
        self.erase_button = tk.Button(self.lower_board,
                                      font=FONT,
                                      bg="grey", fg="white", width=10,
                                      relief="raised",
                                      text="Erase",
                                      command=lambda: self.erase())
        self.erase_button.pack(side=tk.LEFT, fill=tk.X, expand=True)
        # self.submit_button = tk.Button(self.lower_board, font=FONT,
        #                                bg="lime green", fg="black", width=10,
        #                                relief="raised",
        #                                text="Submit Word",
        #                                command=lambda: self.submit_word())
        self.submit_button = tk.Button(self.lower_board, font=FONT,
                                       bg="grey", fg="black", width=10,
                                       relief="raised",
                                       text="Submit Word",
                                       command=lambda: self.submit_word())
        self.submit_button.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def labels(self):
        """
        these methods make the labels of the board- linked to the frames
        """
        self.found_words_label = tk.Label(self.boards_right_side,
                                          font=FONT,
                                          bg='floral white', width=20,
                                          relief="groove",
                                          text="Found Words:\n", anchor=tk.NW)
        self.found_words_label.pack(side=tk.LEFT, fill=tk.Y)
        self.time_label = tk.Label(self.upper_board,
                                   font=FONT,
                                   bg="black", fg="white", width=5,
                                   text="03:00")
        self.time_label.pack(side=tk.LEFT, fill=tk.X)

        self.score_label = tk.Label(self.upper_board,
                                    font=FONT,
                                    bg="black", fg="white", width=8,
                                    relief="groove",
                                    text="score: " + str(self.score))
        self.score_label.pack(side=tk.LEFT, fill=tk.X)

        self.letter_guss_label = tk.Label(self.upper_board,
                                          font=FONT,
                                          bg="white", fg="black",
                                          text=str(self.chosen_letters),
                                          width=20, relief="sunken")
        self.letter_guss_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

    # ---------------------------------------------------------
    # this part of the code contains the methods of the cells
    # ---------------------------------------------------------

    def choose_cell(self, row, col):
        """
        this method gets the location of the pressed cell and updates the game
        according to the rules
        """
        if self.started:
            if (row, col) in self.clicked_cells:
                self.message_slot_button['text'] = "Can't Press Same Cell " \
                                                   "In One Word"
            else:
                if not self.clicked_cells:
                    self.clicked_cells.append((row, col))
                    self.chosen_letters += self.board[row][col]
                    self.letter_guss_label['text'] = self.chosen_letters
                    self.message_slot_button['text'] = DEFAULT_TEXT
                else:
                    last_step = self.clicked_cells[-1]
                    if (row, col) in ex.possible_moves(self.board, last_step):
                        self.clicked_cells.append((row, col))
                        self.chosen_letters += self.board[row][col]
                        self.letter_guss_label['text'] = self.chosen_letters
                        self.message_slot_button['text'] = DEFAULT_TEXT
                    else:
                        self.message_slot_button[
                            'text'] = "Letters Too Far Apart"

    def add_cells(self, board):
        """
        this method is used to add the cells to the board
        """
        if self.started:
            for i in range(len(board)):
                for j in range(len(board)):
                    tk.Button(self.main_board, font=FONT,
                              text=board[i][j], width=6,
                              borderwidth=17, command=lambda n=i, m=j:
                        self.choose_cell(n, m)
                              ).grid(row=i, column=j)

    # ---------------------------------------------------------
    # this part of the code contains the methods of the board
    # ---------------------------------------------------------

    def start(self):
        """
        this method is activated when the game is started it loads the game
        """
        self.timer_func(THREE_MINUTES)
        self.board = load_board()
        for i in range(4):
            for j in range(4):
                tk.Button(self.main_board, font=FONT,
                          text=self.board[i][j], width=6,
                          borderwidth=17, command=lambda n=i, m=j:
                    self.choose_cell(n, m)
                          ).grid(row=i, column=j)
        self.message_slot_button['bg'] = 'sky blue'
        self.message_slot_button['text'] = 'You Can Do It'
        self.message_slot_button['fg'] = 'black'
        self.erase_button['bg'] = "maroon"
        self.submit_button['bg'] = "lime green"
        self.new_game_button['bg'] = 'SeaGreen1'
        self.new_game_button['fg'] = 'black'

    def timer_func(self, timer):
        """
        this recursive method changes the time label every second
        """
        self.started = True
        self.message_slot_button['command'] = lambda: None
        minute, second = divmod(timer, 60)
        self.time_label.config(
            text=str('{:}:{:}'.format(minute, second)))
        count = self.time_label.after(1000, lambda: self.timer_func(timer - 1))
        if timer <= 60:
            self.time_label['bg'] = 'orange'
        if timer <= 10:
            self.time_label['bg'] = 'red'
        if timer == 0:
            self.time_label.after_cancel(count)
            self.started = False
            self.message_slot_button['text'] = 'Score:' + str(self.last_score)
            self.new_game = True
            self.time_up()

    def time_up(self):
        """
        this function updated the board when the time is up
        """
        self.score = 0
        self.message_slot_button['command'] = lambda: \
            self.timer_func(THREE_MINUTES)
        self.time_label['bg'] = 'black'
        self.found_words.clear()
        self.clicked_cells.clear()
        self.letter_guss_label['text'] = ''
        self.score_label['text'] = 'score:' + str(self.score)
        self.found_words_label['text'] = "Found Words:\n"
        self.chosen_letters = ''
        self.message_slot_button['command'] = lambda: None
        self.new_game_button['command'] = lambda: self.start_over()
        self.new_game_button['text'] = 'Press To Play Again'
        self.new_game_button['bg'] = 'maroon'  # this is a new addition
        self.new_game_button['fg'] = 'white'  # this is a new addition
        self.submit_button['bg'] = 'grey'  # this is a new addition
        self.erase_button['bg'] = 'grey'  # this is a new addition
        self.board = [['*'] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                tk.Button(self.main_board, font=FONT,
                          text=self.board[i][j], width=6,
                          borderwidth=17, command=lambda n=i, m=j:
                    self.choose_cell(n, m)
                          ).grid(row=i, column=j)

    def start_over(self):
        """
        this function updates the game when the user want to play another game
        """
        if self.new_game:
            self.new_game_button['text'] = 'Boggle'
            self.new_game_button['fg'] = 'black'
            self.new_game_button['command'] = lambda: None
            self.new_game_button['bg'] = "SeaGreen1"  # this is a new addition
            self.submit_button['bg'] = 'lime green'  # this is a new addition
            self.erase_button['bg'] = 'maroon'  # this is a new addition
            self.last_score = 0
            self.board = load_board()
            for i in range(4):
                for j in range(4):
                    tk.Button(self.main_board, font=FONT,
                              text=self.board[i][j], width=6,
                              borderwidth=17, command=lambda n=i, m=j:
                        self.choose_cell(n, m)
                              ).grid(row=i, column=j)
            self.timer_func(THREE_MINUTES)

    def submit_word(self):
        """
        this method updates the board according to the rules of the game when
        the user is pressing Submit- (self.submit_button)
        """
        if self.started:
            if self.chosen_letters not in self.found_words:
                if ex.is_valid_path(self.board, self.clicked_cells,
                                    self.words):
                    self.message_slot_button['text'] = 'Nice'
                    self.found_words.append(self.chosen_letters)
                    self.score += (len(self.clicked_cells) ** 2)
                    self.last_score += (len(self.clicked_cells) ** 2)
                    self.score_label['text'] = 'score:' + str(self.score)
                    self.found_words_label['text'] += str(
                        self.found_words[-1]) + '\n'
                else:
                    self.message_slot_button['text'] = 'Not A Word'
            else:
                self.message_slot_button['text'] = 'Word Already Found'
            self.clicked_cells.clear()
            self.chosen_letters = ''
            self.letter_guss_label['text'] = self.chosen_letters

    def erase(self):
        """
        this method updates the board according to the rules of the game when
        the user is pressing Erase- (self.erase_button)
        """
        if self.started:
            if self.chosen_letters and self.clicked_cells:
                self.chosen_letters = self.chosen_letters[:-1]
                self.clicked_cells.pop()
                self.letter_guss_label['text'] = self.chosen_letters
            else:
                self.message_slot_button['text'] = 'Can Nothing Disappear?'

    def run(self):
        """
        this function activates the built-in function of tkinter- mainloop()
        """
        self.main_window.mainloop()
