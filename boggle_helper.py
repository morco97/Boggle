# Intro2cs, 67101-2
# Exercise 12: Boggle
# By: Mor Cohen

import boggle_board_randomizer as rd


def load_words():
    """
    this function load the words list from the given file
    """
    f = open("boggle_dict.txt")
    words = set(line.strip() for line in f.readlines())
    f.close()
    return words


def load_board():
    """
    this function loads a random board
    """
    return rd.randomize_board()


