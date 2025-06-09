# --------------------------
# FONCTIONS BASIQUES PUISSANCE 4
# --------------------------

# Crée un plateau vide (6 lignes x 7 colonnes)
def create_board():
    rows = 6
    columns = 7
    board = [[0 for _ in range(columns)] for _ in range(rows)]
    return board

# Affiche  le plateau
def print_board(board):
    print("Plateau actuel :")
    for row in board:
        print(row)
    print("Colonnes : 0 1 2 3 4 5 6")
    print("-" * 20)

# Ajoute un pion dans la colonne choisie pour le joueur donné
def make_move(board, column, player):
    # On part du bas de la colonne
    for row in reversed(range(len(board))):
        if board[row][column] == 0:
            board[row][column] = player
            return True  # coup effectué avec succès
    return False  # colonne pleine

# Renvoie la liste des colonnes où un coup est possible
def get_valid_moves(board):
    valid_moves = []
    columns = len(board[0])
    for col in range(columns):
        if board[0][col] == 0:
            valid_moves.append(col)
    return valid_moves

# Vérifie si la partie est terminée
def is_terminal(board):
    # On vérifie d'abord si quelqu'un a gagné
    if check_winner(board) is not None:
        return True

    # Sinon, on vérifie s'il reste des coups possibles
    if len(get_valid_moves(board)) == 0:
        return True  # plus de coups possibles : match nul

    # Sinon, la partie continue
    return False

# Vérifie s'il y a un gagnant
def check_winner(board):
    rows = len(board)
    columns = len(board[0])

    for row in range(rows):
        for col in range(columns):
            player = board[row][col]
            if player == 0:
                continue  # case vide, on passe

            # Vérification horizontale 
            if col <= columns - 4 and all(board[row][col + i] == player for i in range(4)):
                return player

            # Vérification verticale 
            if row <= rows - 4 and all(board[row + i][col] == player for i in range(4)):
                return player

            # Vérification diagonale ↘
            if row <= rows - 4 and col <= columns - 4 and all(board[row + i][col + i] == player for i in range(4)):
                return player

            # Vérification diagonale ↙
            if row <= rows - 4 and col >= 3 and all(board[row + i][col - i] == player for i in range(4)):
                return player

    # Aucun gagnant
    return None

# Renvoie la valeur utilitaire du plateau
def utility(board):
    winner = check_winner(board)
    if winner == 1:
        return 1
    elif winner == -1:
        return -1
    else:
        return 0  # soit match nul, soit partie non terminée