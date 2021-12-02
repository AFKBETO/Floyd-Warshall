#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ce fichier contient des méthodes liées à algorithme de Floyd-Warshall.
"""

from math import isinf

from utils_ui import print_matrix
from utils_ui import write_line,write_matrix


# * Il semble honnête de mentionner que l'un des membres du groupe (Guillaume Vandenneucker) avait déjà travaillé sur une version plus basique de cet algorithme dans un projet de cours l'année précédente.
# * Plus précisément, les trois lignes de boucles principales ainsi que le principe de mise à jour de distance (new_dist) étaient connus.
# * Le suivi des successeurs a quant à lui été adapté de https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm#Path_reconstruction
#   Algorithme de Floyd-Warshall
#   Paramètres :
#       file_name   : le nom de fichier où l'exécution de l'algorithme est ajoutée
#       matrix      : la matrice représentante le graphe à traiter
#   Retourne :
#       result      : la matrice résultante de l'algorithme
#       successors  : la matrice de successeurs pour reconstruire les chemins
def floyd_warshall(file_name,matrix):
    successors = [[None for i in line] for line in matrix]  # None si on a détecté un circuit absorbant
    diviseur = "\n\t - - - - - - - -"

    # Copie de la matrice
    result = [[i for i in line] for line in matrix]
    n = len(result)

    # Définition de la diagonale à 0
    for j in range(n):
        if isinf(result[j][j]):
            result[j][j] = 0
    
    print(f"{diviseur}\nInitial Floyd-Warshall matrix:")
    write_line(file_name,f"{diviseur}\nInitial Floyd-Warshall matrix:")
    print_matrix(result)
    write_matrix(file_name,result)

    # Initialisation des prédécesseurs
    for i in range(n):
        for j in range(n):
            successors[i][j] = j

    # Pour tout sommet intermédiaire, on vérifie s'il permet un chemin plus court pour toute autre pair de sommet
    for intermediate in range(0, n):
        for i in range(0, n):
            for j in range(0, n):
                new_dist = result[i][intermediate] + result[intermediate][j]
                
                #if successors is not None and i == j and new_dist < 0:
                #    successors = None

                if new_dist < result[i][j]:
                    result[i][j] = str(new_dist) + "*"
                    print("\nNew path found:")
                    write_line(file_name,"\nNew path found:")
                    print_matrix(result)
                    write_matrix(file_name,result)
                    result[i][j] = new_dist
                    if successors is not None:
                        successors[i][j] = successors[i][intermediate]
                    

    return result, successors

#   Adapté de https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm#Path_reconstruction
#   Construction de chemin (path)
#   Paramètres :
#       successors  : la matrice de chemin
#       neg_list    : la liste des sommets dans circuits absorbants
#       u           : le sommet de départ
#       v           : le sommet d'arrivée
#   Retourne :
#       path        : le chemin sous forme d'une liste
def calculate_path(successors, neg_list, u, v):
    path = []
    if successors[u][v] is not None:
        if u in neg_list: #renvoyer une liste vide si oui
            return []
        else:             #ajouter u dans le chemin
            path.append(u)
        while u is not v:
            u = successors[u][v]
            #vérifier si u est un sommet dans le(s) circuit(s) absorbant(s)
            if u in neg_list: #renvoyer une liste vide si oui
                path = []
                break
            else:             #ajouter u dans le chemin
                path.append(u)
    return path

#   Récupérer la liste des sommets dans le(s) circuit(s) absorbant(s)
#   Paramètres :
#       matrix_graph    : la matrice résultante de l'algorithme Floyd-Warshall
#   Retourne :
#       list_node_neg   : la liste des sommets appartiennant dans le(s) circuit(s) absorbant(s)
def extract_neg_node(matrix_graph):
    list_node_neg = []
    
    for i in range(len(matrix_graph)):
        if matrix_graph[i][i] < 0:
            list_node_neg.append(i)

    return list_node_neg
        