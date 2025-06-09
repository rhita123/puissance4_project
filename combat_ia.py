from puissance4_game import *
from minimax import *

# Profondeur fixée pour l'IA (ajustable si besoin)
DEPTH = 5

def IA_Decision(board, player):
    """
    Fonction IA_Decision  pour le combat IA.
    Prend un plateau (6x12) et un joueur (1 ou -1), retourne la colonne à jouer.
    """
    return minimax_decision(board, DEPTH, player)

def Terminal_Test(board):
    """
    Fonction Terminal_Test  pour le combat IA.
    Retourne True si le jeu est terminé, False sinon.
    """
    return is_terminal(board)