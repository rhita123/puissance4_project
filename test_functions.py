from puissance4_game import *
from minimax import *

# -----------------------------------------------------
# TEST de la fonction minimax_decision
# -----------------------------------------------------

print("\n===== TEST MINIMAX DECISION =====")

# On part d'un plateau un peu rempli
board = create_board()
board[5][0] = 1
board[4][0] = -1
board[5][1] = 1
board[4][1] = -1
board[5][2] = 1

print_board(board)

# Test pour joueur 1 (MAX)
best_move_player1 = minimax_decision(board, depth=3, player=1)
print("Meilleure action pour joueur 1 :", best_move_player1)

# Test pour joueur -1 (MIN)
best_move_player_minus1 = minimax_decision(board, depth=3, player=-1)
print("Meilleure action pour joueur -1 :", best_move_player_minus1)