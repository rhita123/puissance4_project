from puissance4_game import *
import time


def evaluate_window(window, player):
    """Évalue une fenêtre de 4 cases."""
    score = 0
    opponent = -player

    if window.count(player) == 4:
        score += 10000
    elif window.count(player) == 3 and window.count(0) == 1:
        score += 10000  # Priorité absolue pour gagner
    elif window.count(player) == 2 and window.count(0) == 2:
        score += 10

    if window.count(opponent) == 4:
        score -= 10000
    elif window.count(opponent) == 3 and window.count(0) == 1:
        score -= 10000  # Priorité absolue au blocage
    elif window.count(opponent) == 2 and window.count(0) == 2:
        score -= 10

    return score

def score_position(board, player):
    """Score global du plateau pour le joueur."""
    score = 0
    ROW_COUNT = len(board)
    COLUMN_COUNT = len(board[0])

    ROW_WEIGHTS = [1, 2, 3, 4, 5, 6]  # Ligne 0 = haut, ligne 5 = bas

    # Score des lignes
    for row_index, row in enumerate(board):
        for c in range(COLUMN_COUNT - 3):
            window = row[c:c+4]
            score += evaluate_window(window, player) * ROW_WEIGHTS[row_index]

    # Score des colonnes
    for c in range(COLUMN_COUNT):
        col_array = [board[r][c] for r in range(ROW_COUNT)]
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r+4]
            score += evaluate_window(window, player)

    # Score diagonales positives (/)
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r+i][c+i] for i in range(4)]
            score += evaluate_window(window, player)

    # Score diagonales négatives (\)
    for r in range(3, ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r-i][c+i] for i in range(4)]
            score += evaluate_window(window, player)

    # Center control bonus with weighted columns
    center_weights = [3, 4, 5, 7, 8, 9, 9, 8, 7, 5, 4, 3]  # Example for 12 columns
    for c in range(COLUMN_COUNT):
        col_array = [board[r][c] for r in range(ROW_COUNT)]
        center_count = col_array.count(player)
        # If COLUMN_COUNT > len(center_weights), repeat edge weights
        w = center_weights[c] if c < len(center_weights) else center_weights[-1]
        score += center_count * w

    return score

#  fonction min_value
def min_value(board, depth, player, alpha, beta, start_time):
    if is_terminal(board):
        return utility(board)  # On garde utility pour fin de partie
    if depth == 0 or time.time() - start_time > 10:
        return score_position(board, player)  # Nouvelle heuristique pour évaluer

    v = float('inf')  # On veut minimiser la valeur

    for move in get_valid_moves(board):
        # On copie le plateau
        new_board = [row.copy() for row in board]
        # On joue le coup pour le joueur MIN (-1)
        make_move(new_board, move, -1)
        # On appelle max_value récursivement
        v = min(v, max_value(new_board, depth - 1, player, alpha, beta, start_time))

        if v <= alpha:
            break
        beta = min(beta, v)

    return v

# fonction max_value
def max_value(board, depth, player, alpha, beta, start_time):
    if is_terminal(board):
        return utility(board)
    if depth == 0 or time.time() - start_time > 10:
        return score_position(board, player)

    v = float('-inf')  # On veut maximiser la valeur

    for move in get_valid_moves(board):
        # On copie le plateau
        new_board = [row.copy() for row in board]
        # On joue le coup pour le joueur MAX (1)
        make_move(new_board, move, 1)
        # On appelle min_value récursivement
        v = max(v, min_value(new_board, depth - 1, player, alpha, beta, start_time))

        if v >= beta:
            break
        alpha = max(alpha, v)

    return v

# fonction minimax_decision
def minimax_decision(board, depth, player):
    """
    Choisit la meilleure action pour le joueur donné (1 ou -1) en utilisant Minimax.
    """
    start_time = time.time()
    # Initialisation
    best_move = None

    alpha = float('-inf')
    beta = float('inf')

    valid_moves = get_valid_moves(board)
    valid_moves.sort(key=lambda x: abs((len(board[0]) // 2) - x))

    # Si joueur MAX (1), on cherche à maximiser
    if player == 1:
        best_value = float('-inf')
        for move in valid_moves:
            new_board = [row.copy() for row in board]
            make_move(new_board, move, player)
            v = min_value(new_board, depth - 1, player, alpha, beta, start_time)
            print(f"Action {move} → valeur {v}")
            if v > best_value:
                best_value = v
                best_move = move
            alpha = max(alpha, best_value)

    # Si joueur MIN (-1), on cherche à minimiser
    else:
        best_value = float('inf')
        for move in valid_moves:
            new_board = [row.copy() for row in board]
            make_move(new_board, move, player)
            v = max_value(new_board, depth - 1, player, alpha, beta, start_time)
            print(f"Action {move} → valeur {v}")
            if v < best_value:
                best_value = v
                best_move = move
            beta = min(beta, best_value)

    return best_move