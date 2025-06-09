from puissance4_game import *

board = create_board()
print_board(board)

# On joue quelques coups
make_move(board, 3, 1)
make_move(board, 3, -1)
make_move(board, 3, 1)
make_move(board, 3, -1)
make_move(board, 3, 1)
make_move(board, 3, -1)  # ici colonne 3 va être pleine si on fait 6 coups

print_board(board)

# On affiche les colonnes jouables
valid_moves = get_valid_moves(board)
print("Colonnes valides pour jouer :", valid_moves)

print("Partie terminée ?", is_terminal(board))

print("Valeur utility du plateau :", utility(board))