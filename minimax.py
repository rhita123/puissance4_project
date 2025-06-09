
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

# fonction minimax_decision
def minimax_decision(board, depth, player):
    """
    Choisit la meilleure action pour le joueur donné (1 ou -1) en utilisant Minimax.
    """
    # Initialisation
    best_move = None

    # Si joueur MAX (1), on cherche à maximiser
    if player == 1:
        best_value = float('-inf')
        for move in get_valid_moves(board):
            new_board = [row.copy() for row in board]
            make_move(new_board, move, player)
            v = min_value(new_board, depth - 1)
            print(f"Action {move} → valeur {v}")
            if v > best_value:
                best_value = v
                best_move = move

    # Si joueur MIN (-1), on cherche à minimiser
    else:
        best_value = float('inf')
        for move in get_valid_moves(board):
            new_board = [row.copy() for row in board]
            make_move(new_board, move, player)
            v = max_value(new_board, depth - 1)
            print(f"Action {move} → valeur {v}")
            if v < best_value:
                best_value = v
                best_move = move

    return best_move