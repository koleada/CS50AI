"""
Tic Tac Toe Player
"""

import copy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_counter = 0
    o_counter = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                x_counter += 1
            elif board[i][j] == O:
                o_counter += 1
            else:
                pass
    if x_counter > o_counter:
        return O
    elif x_counter < o_counter:
        return X
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions.add((i, j))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    turn = player(board)
    i, j = action
    if board[i][j] == EMPTY and i >= 0 and j >= 0:
        board = copy.deepcopy(board)
        if turn == X:
            board[i][j] = X
            return board
        else:
            board[i][j] = O
            return board
    else:
        raise Exception


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # ** all keyword returns a boolean if all iterable items are true

    # checks horizontally for X
    for row in board:
        if all(cell == X for cell in row):
            return X
    # checks horizontally for O
    for row in board:
        if all(cell == O for cell in row):
            return O

    # checks vertically for X
    for col in range(3):
        if all(board[row][col] == X for row in range(3)):
            return X
    # checks vertically for O
    for col in range(3):
        if all(board[row][col] == O for row in range(3)):
            return O

    # checks diagonally for X
    if board[0][0] == X and board[1][1] == X and board[2][2] == X:
        return X
    elif board[0][2] == X and board[1][1] == X and board[2][0] == X:
        return X
    if board[0][0] == O and board[1][1] == O and board[2][2] == O:
        return O
    elif board[0][2] == O and board[1][1] == O and board[2][0] == O:
        return O
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == X or winner(board) == O:
        return True
    else:
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    return False
                else:
                    pass
        return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    who_won = winner(board)
    if who_won == X:
        return 1
    elif who_won == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # x would be maximizing as per the utility and O will be minimizing

    if terminal(board):
        return None

    # holds onto the best action
    best_move = None

    if player(board) == X:
        # init v = -inf for max
        v = -2
        # cycle through all actions from gameboard and pass the result of that action on curr board to max_value
        for a in actions(board):
            # save value returned by max_value
            score = max_value(result(board, a))

            # if score is better, update the score and the best move so we have a updated benchmark
            if score > v:
                best_move = a
                v = score

    elif player(board) == O:
        v = 2
        for a in actions(board):
            score = min_value(result(board, a))
            if score < v:
                best_move = a
                v = score

    return best_move


def max_value(board):
    v = -math.inf

    # this is how the function actually returns a "score" to be checked in the minimax func
    if terminal(board):
        return utility(board)
    # cycles through all possible actions from this new board and recursively calls min_value with them
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    # return the recursive call
    return v


def min_value(board):
    v = math.inf
    if terminal(board):
        return utility(board)
    # cycles thru all actions this time passing the to max_value
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v
