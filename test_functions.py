from puissance4_game import *
from minimax import *

# Exemple pour forcer une victoire pour 1
board = create_board()
board[5][0] = 1
board[4][0] = 1
board[3][0] = 1
board[2][0] = 1  # alignement vertical colonne 0

print_board(board)
print("Partie terminée ?", is_terminal(board))
print("Valeur utility du plateau :", utility(board))
print("Valeur min_value du plateau :", min_value(board, depth=3))
print("Valeur max_value du plateau :", max_value(board, depth=3))