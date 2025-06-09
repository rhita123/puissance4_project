
from puissance4_game import get_valid_moves, is_terminal, utility, make_move

#  fonction min_value
def min_value(board, depth):
    if is_terminal(board) or depth == 0:
        return utility(board)

    v = float('inf')  # On veut minimiser la valeur

    for move in get_valid_moves(board):
        # On copie le plateau
        new_board = [row.copy() for row in board]
        # On joue le coup pour le joueur MIN (-1)
        make_move(new_board, move, -1)
        # On appelle max_value récursivement
        v = min(v, max_value(new_board, depth - 1))

    return v

# fonction max_value
def max_value(board, depth):
    if is_terminal(board) or depth == 0:
        return utility(board)

    v = float('-inf')  # On veut maximiser la valeur

    for move in get_valid_moves(board):
        # On copie le plateau
        new_board = [row.copy() for row in board]
        # On joue le coup pour le joueur MAX (1)
        make_move(new_board, move, 1)
        # On appelle min_value récursivement
        v = max(v, min_value(new_board, depth - 1))

    return v