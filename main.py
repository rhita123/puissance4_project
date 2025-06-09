from puissance4_game import *
from minimax import *

# ----------- PARAMETRES ------------

DEPTH = 5  # Profondeur d'exploration de l'IA

# ----------- INITIALISATION --------

board = create_board()
print_board(board)

# Choisir qui commence : 1 = humain, -1 = IA
choice = input("Qui commence ? (1 = Humain, -1 = IA) : ")
while choice not in ['1', '-1']:
    choice = input("Choix invalide. Qui commence ? (1 = Humain, -1 = IA) : ")

current_player = int(choice)

# ----------- BOUCLE DE JEU ---------

while not is_terminal(board):
    print_board(board)
    print(f"Joueur {'Humain' if current_player == 1 else 'IA'} à toi de jouer.")

    if current_player == 1:
        # Tour du joueur humain
        valid_columns = get_valid_moves(board)
        print(f"Colonnes valides : {valid_columns}")
        col = int(input("Choisis ta colonne : "))
        while col not in valid_columns:
            col = int(input("Colonne invalide. Choisis une autre colonne : "))
    else:
        # Tour de l'IA
        print("L'IA réfléchit...")
        col = minimax_decision(board, DEPTH, current_player)
        print(f"L'IA joue en colonne : {col}")

    # Appliquer le coup
    move_success = make_move(board, col, current_player)
    if not move_success:
        print("Colonne pleine, choisis une autre colonne.")
        continue  # ne pas changer de joueur si le coup est invalide

    # Changer de joueur
    current_player *= -1

# ----------- FIN DE PARTIE ---------

print_board(board)
winner = check_winner(board)
if winner == 1:
    print("Victoire du joueur HUMAIN ! ")
elif winner == -1:
    print("Victoire de l'IA  !")
else:
    print("Match nul  !")