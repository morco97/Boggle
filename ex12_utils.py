# Intro2cs, 67101-2
# Exercise 12: Boggle
# By: Mor Cohen

# --------------------------------NOTES----------------------------------------
""" this file is divided by the four functions we were asked to implement.
    please note that some early helper function are used later, sometimes not
    as a helper of their original function."""
# -----------------------------------------------------------------------------

# ------------------------------CONSTANTS--------------------------------------
MOVES = {'UP': (-1, 0), 'DOWN': (1, 0), 'LEFT': (0, -1), 'RIGHT': (0, 1),
         'RIGHT_DIAGONAL_UP': (-1, 1), 'RIGHT_DIAGONAL_DOWN': (1, -1),
         'LEFT_DIAGONAL_UP': (-1, -1), 'LEFT_DIAGONAL_DOWN': (1, 1)}
# -----------------------------------------------------------------------------

# -------------------------------------------------------------
# the function is_valid_path() and the helper functions
# -------------------------------------------------------------


def boards_cells(board):
    """
    this function gets a board and return all the cells in the board in the
    format of matrix indexes
    :param board: a given board
    :return: a list of tuples
    """
    cells = []
    for row in range(len(board)):
        for col in range(len(board[0])):
            cells.append((row, col))
    return cells


def possible_moves(board, cell):
    """
    this function checks the possible moves a cell can make, given a cell
    and a board
    :param board: a given board
    :param cell: a given cell
    :return: a list of tuples
    """
    valid_cells = boards_cells(board)
    moves_list = []
    row = cell[0]
    col = cell[1]
    for move in MOVES.values():
        target_cell = (move[0] + row, move[1] + col)
        if target_cell in valid_cells:
            moves_list.append(target_cell)
    return moves_list


def appears_only_once(path):
    """
    this function checks if the path does not go in same cell more than once
    :param path: a given path, list of tuples
    :return: True if all cells appear only once, else False
    """
    for appearance in path:
        counter = path.count(appearance)
        if counter > 1:
            return False
    return True


def word_of_path(board, path):
    """
    this function gets a path and a board and returns what word is on that path
    note, this function does not know if the path is valid
    :param board: a given board
    :param path: a given path
    :return: the word (str), None if the path is out of the board
    """
    valid_cells = boards_cells(board)
    word = ''
    for cell in path:
        if cell in valid_cells:
            word += board[cell[0]][cell[1]]
        else:
            return None
    return word


def valid_first_step(board, path):
    row_size = len(board[0])
    col_size = len(board)
    if path[0][0] < 0 or path[0][1] < 0:
        return False
    if path[0][0] > col_size or path[0][1] > row_size:
        return False
    return True


def valid_moves(board, path):
    for place in range(len(path) - 1):
        if path[place + 1] not in possible_moves(board, path[place]):
            return False
    return True


def valid_path_regardless_words(board, path):
    """
    this function checks if the path is valid, but does not check if the word
    of the path is in path- it is needed for the backtracking functions
    :param board: a given board
    :param path: a given path
    :return: True if the path is valid, else None
    """
    valid_cells = boards_cells(board)
    if not path:
        return True
    # checking if the first step is valid
    if (path[0][0], path[0][1]) not in valid_cells:
        return False
    # check if a cell appears more than once in path
    if not appears_only_once(path):
        return False
    # checking if the moves are valid
    if not valid_moves(board, path):
        return False
    return True


def is_valid_path(board, path, words):
    """
    this function gets a path and checks if the path is valid
    :param board: the games board
    :param path: a path of a word
    :param words: iterable type container full of valid words
    :return: if path is valid the word (str), else None
    """
    valid_cells = boards_cells(board)
    if not path:
        return None
    # checking if the first step is valid
    if (path[0][0], path[0][1]) not in valid_cells:
        return None
    # check if a cell appears more than once in path
    if not appears_only_once(path):
        return None
    # checking if the moves are valid
    if not valid_moves(board, path):
        return None
    # building the word
    word = word_of_path(board, path)
    # checking if it is a valid word
    if word in words:
        return word
    return None


# -------------------------------------------------------------
# the functions find_length_n_paths(), find_length_n_words()
# and the helper functions
# -------------------------------------------------------------


def step_implementation(cell, step):
    """
    this function changes the index on the board based on the step it received
    :param cell: the current position on the board, tuple
    :param step: the wanted movement direction, tuple
    :return: a tuple, representing the new location
    """
    return cell[0] + step[0], cell[1] + step[1]


def valid_first_m_letters(board, path, words):
    """
    this function gets a path (with m letters on that path) and check if there
    is a word in words that this path could match fully or just a part of it
    :param board: a given board
    :param path: a given path
    :param words: iterable type container full of valid words
    :return: True if there is a matching word, else False
    """
    if not path:
        return True
    if word_of_path(board, path):
        first_letters = word_of_path(board, path)
        number_of_letters = len(first_letters)
        for letters in words:
            if first_letters == letters[: number_of_letters]:
                return True
        return False


def _find_length_n_paths_helper(n, board, words, start, path, paths):
    """
    a helper recursive (backtracking) function finds all valid length n paths
    that start on a given cell
    :param n: int, the wanted length path
    :param board: a given board
    :param words: iterable type container full of valid words
    :param start: the given cell we start searching from
    :param path: the path we are checking
    :param paths: list containing the paths
    :return: does not have a return value, but changes result (a list)
    """
    # the base case
    if len(path) == n and is_valid_path(board, path, words):
        paths.append(path[:])
        return
    # the backtracking part
    if (not len(path) < n) or (not valid_first_m_letters(board, path, words)) \
            or (not valid_path_regardless_words(board, path)):
        return
    # do the recursion in every valid direction:
    for move in possible_moves(board, start):
        path.append(move)
        _find_length_n_paths_helper(n, board, words,
                                    move, path, paths)
        path.pop()


def find_length_n_paths(n, board, words):
    """run on every cell with the helper function"""
    if n == 0:
        return []
    paths = []
    rows = len(board)
    cols = len(board[0])
    for row in range(rows):
        for col in range(cols):
            _find_length_n_paths_helper(n, board,
                                        words, (row, col),
                                        [(row, col)], paths)
    return paths


def _find_length_n_words_helper(n, board, words, start, path, paths):
    """
    a helper recursive (backtracking) function finds all valid length n words
    that start on a given cell
    :param n: int, the wanted length word
    :param board: a given board
    :param words: iterable type container full of valid words
    :param start: the given cell we start searching from
    :param path: the path we are checking
    :param paths: list containing the paths
    :return: does not have a return value, but changes result (a list)
    """
    # the base case
    if not word_of_path(board, path):
        return
    if len(word_of_path(board, path)) == n and\
            is_valid_path(board, path, words):
        paths.append(path[:])
        return
    # the backtracking part
    if (not word_of_path(board, path)) or (len(word_of_path(board, path)) > n)\
            or (not valid_first_m_letters(board, path, words)) or\
            (not valid_path_regardless_words(board, path)):
        return
    # do the recursion in every valid direction:
    for move in possible_moves(board, start):
        path.append(move)
        _find_length_n_words_helper(n, board, words,
                                    move, path, paths)
        path.pop()


def find_length_n_words(n, board, words):
    """run on every cell with the helper function"""
    if n == 0:
        return []
    paths = []
    rows = len(board)
    cols = len(board[0])
    for row in range(rows):
        for col in range(cols):
            _find_length_n_words_helper(n, board,
                                        words, (row, col),
                                        [(row, col)], paths)
    return paths


# -------------------------------------------------------------
# the function max_score_paths() and helpers functions
# -------------------------------------------------------------


def biggest_word_length(words):
    """
    this function finds the length of the longest words in words
    :param words: iterable type container full of valid words
    :return: the length of the longest word(int)
    """
    biggest = 0
    for word in words:
        if len(word) > biggest:
            biggest = len(word)
    return biggest


def _find_every_path_helper(board, word, start, path, paths):
    """
    this function checks if a word has a path starting from a given cell and
    if so, returns the path/ paths
    :param board: a given board
    :param word:  a given word
    :param start: a given cell that we scan from
    :return: if there are paths to the word that start on that cell- a list
    of paths, else None(empty list)
    """
    # base case
    if is_valid_path(board, path, [word]):
        paths.append(path[:])
        return
    # the backtracking part
    if not valid_first_m_letters(board, path, [word]) or \
            (not valid_path_regardless_words(board, path)):
        return
    # doing the recursion on every possible cell
    for move in possible_moves(board, start):
        path.append(move)
        _find_every_path_helper(board, word, move, path, paths)
        path.pop()


def find_every_path(board, word):
    """
    this function finds every path for a word in a given board
    :param board: a given board
    :param word: a given word
    :return: list of lists of tuples, representing all paths to a word on the
    board
    """
    paths = []
    rows = len(board)
    cols = len(board[0])
    for row in range(rows):
        for col in range(cols):
            if _find_every_path_helper(board, word, (row, col),
                                       [(row, col)], paths):
                _find_every_path_helper(board, word, (row, col),
                                        [(row, col)], paths)
    return paths


def longest_path(board, word):
    """
    this function gets a word on the board and returns the longest path to the
    word
    :param board: a given board
    :param word: a given word(str)
    :return: a list of tuples, representing the longest path
    """
    paths = find_every_path(board, word)
    largest_path = []
    for path in paths:
        if len(path) > len(largest_path):
            largest_path = path
    return largest_path


def max_score_paths(board, words):
    """
    run with a loop on words in len for range(1, biggest)
    for every word return the longest path
    :param board: a given board
    :param words: iterable type container full of valid words
    :return: a list of paths
    """
    if not words:
        return []
    paths = []
    for length in range(1, biggest_word_length(words) + 1):
        for word in find_length_n_words(length, board, words):
            modified_word = word_of_path(board, word)
            paths.append(longest_path(board, modified_word))
    return paths
