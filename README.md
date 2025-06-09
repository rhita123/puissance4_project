# Projet Puissance 4 

## Description

Ce projet consiste à développer une Intelligence Artificielle pour le jeu Puissance 4

Le but est de créer une IA capable de jouer efficacement sur une grille de **12 colonnes × 6 lignes**, avec une limite de **42 pions** par partie. Le joueur humain et l'IA s'affrontent en alternance. Une phase finale permettra de faire s'affronter les IA des différents étudiants.

---

## Fonctionnalités

 Interface de jeu en console  
 Choix du joueur qui commence (humain ou IA)  
 Limite de 42 pions joués  
 IA basée sur l'algorithme **Minimax avec élagage Alpha-Beta**  
 **Immediate Threat Check** → détection des menaces immédiates (blocage ou victoire)  
 Heuristique avancée :
- Score des alignements
- Pondération du centre
- Pondération des lignes (plus bas = plus fort)

 Gestion automatique des fins de partie  
 Fichier séparé `combat_ia.py` pour la phase **Combat entre IA** (conforme au sujet)

---

## Architecture du projet

- `main.py` → boucle de jeu principale pour jouer contre l'IA
- `minimax.py` → algorithme Minimax, heuristique, Threat Check
- `puissance4_game.py` → gestion du plateau, règles du jeu
- `combat_ia.py` → fonctions `IA_Decision` et `Terminal_Test` pour la phase tournoi IA

---

## Lancement du jeu

```bash
python3 main.py