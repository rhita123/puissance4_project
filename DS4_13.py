# ====================================================
# Projet Puissance 4 - Groupe DS4_13
#
# Ce fichier contient l’implémentation complète de notre IA pour le tournoi.
#
# Approche :
# - Utilisation de l’algorithme Minimax avec élagage alpha-bêta.
# - Fonction heuristique basée sur l’occupation centrale, la détection de menaces,
#   et la pondération de motifs de 2, 3 ou 4 pions alignés.
# - Un Threat Check permet de réagir immédiatement aux menaces de victoire adverses.
#
#  Objectif : Choisir le meilleur coup possible à chaque tour pour bloquer
# ou gagner en fonction du plateau, sans dépasser le temps imparti.
#
#  Fonctions attendues pour les battles :
# - IA_Decision(board): retourne la colonne à jouer.
# - Terminal_Test(board): retourne True si la partie est finie, sinon False.
#
#  Lancer le jeu localement : appeler Lancer_jeu()
# ====================================================

import math
import random
import copy

ROWS = 6
COLUMNS = 12
EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2
WINDOW_LENGTH = 4

def create_board():
    board = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[0][col] == 0

def get_next_open_row(board, col):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == 0:
            return r
    return None

def print_board(board):
    print("\nBoard:")
    for row in board:
        print(row)
    print()

def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMNS-3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMNS):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COLUMNS-3):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMNS-3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

    return False

def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

    if window.count(piece) == 4:
        score += 10000
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 100
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 10

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 80

    return score

def score_position(board, piece):
    score = 0

    # Score center column
    center_array = [board[r][COLUMNS//2] for r in range(ROWS)]
    center_count = center_array.count(piece)
    score += center_count * 6

    # Score Horizontal
    for r in range(ROWS):
        row_array = board[r]
        for c in range(COLUMNS-3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score Vertical
    for c in range(COLUMNS):
        col_array = [board[r][c] for r in range(ROWS)]
        for r in range(ROWS-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score positive sloped diagonal
    for r in range(ROWS-3):
        for c in range(COLUMNS-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    # Score negative sloped diagonal
    for r in range(3, ROWS):
        for c in range(COLUMNS-3):
            window = [board[r-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score

def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMNS):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000000000)
            else: # Game is over, no more valid moves
                return (None, 0)
        else: # Depth is zero
            return (None, score_position(board, AI_PIECE))
    if maximizingPlayer:
        value = -math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = copy.deepcopy(board)
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, value
    else: # Minimizing player
        value = math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = copy.deepcopy(board)
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_col, value

def threat_check(board, piece):
    # Check if opponent can win next move; if yes, block it immediately
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE
    valid_locations = get_valid_locations(board)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = copy.deepcopy(board)
        drop_piece(temp_board, row, col, opp_piece)
        if winning_move(temp_board, opp_piece):
            return col
    return None

def IA_Decision(board):
    # First, check if immediate threat to block
    threat = threat_check(board, AI_PIECE)
    if threat is not None:
        return threat
    # Else, use minimax to choose best move
    col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)
    return col

def Terminal_Test(board):
    return is_terminal_node(board)

def Lancer_jeu():
    board = create_board()
    game_over = False
    turn = random.randint(PLAYER_PIECE, AI_PIECE)  # Randomly choose who starts

    print("Bienvenue au Puissance 4!")
    print_board(board)

    while not game_over:
        if turn == PLAYER_PIECE:
            # Player move
            valid_move = False
            while not valid_move:
                try:
                    col = int(input(f"Joueur 1 (vous), entrez la colonne (0-{COLUMNS - 1}): "))
                    if col < 0 or col >= COLUMNS:
                        print("Colonne invalide, essayez encore.")
                    elif not is_valid_location(board, col):
                        print("Colonne pleine, essayez encore.")
                    else:
                        valid_move = True
                except ValueError:
                    print("Entrée invalide, veuillez entrer un nombre entre 0 et 11.")

            row = get_next_open_row(board, col)
            drop_piece(board, row, col, PLAYER_PIECE)

            if winning_move(board, PLAYER_PIECE):
                print_board(board)
                print("Félicitations! Vous avez gagné!")
                game_over = True
            else:
                if Terminal_Test(board):
                    print_board(board)
                    print("Match nul!")
                    game_over = True

            turn = AI_PIECE

        else:
            # AI move
            print("Tour de l'IA...")
            col = IA_Decision(board)
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)
                print(f"L'IA joue en colonne {col}.")

                if winning_move(board, AI_PIECE):
                    print_board(board)
                    print("L'IA a gagné! Bonne chance pour la prochaine fois.")
                    game_over = True
                else:
                    if Terminal_Test(board):
                        print_board(board)
                        print("Match nul!")
                        game_over = True

                turn = PLAYER_PIECE
            else:
                # This should not happen, but just in case
                print("Erreur: L'IA a choisi une colonne invalide.")
                game_over = True

        print_board(board)
