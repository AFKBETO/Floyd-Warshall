#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ce fichier contient des méthodes liées à algorithme de Floyd-Warshall.
"""

from math import inf


# * Il semble honnête de mentionner que l'un des membres du groupe (Guillaume Vandenneucker) avait déjà travaillé sur une version plus basique de cet algorithme dans un projet de cours l'année précédente.
# * Plus précisément, les trois lignes de boucles principales ainsi que le principe de mise à jour de distance (new_dist) étaient connus.
# * Le suivi des successeurs a quant à lui été adapté de https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm#Path_reconstruction
def floyd_warshall(matrix):
    successors = [[None for i in line] for line in matrix]  # None si on a détecté un circuit absorbant

    # Copie de la matrice
    result = [[i for i in line] for line in matrix]
    n = len(result)

    # Définition de la diagonale à 0
    for j in range(n):
        result[j][j] = 0

    # Initialisation des prédécesseurs
    for i in range(n):
        for j in range(n):
            successors[i][j] = j

    # Pour tout sommet intermédiaire, on vérifie s'il permet un chemin plus court pour toute autre pair de sommet
    for intermediate in range(0, n):
        for i in range(0, n):
            for j in range(0, n):
                new_dist = result[i][intermediate] + result[intermediate][j]
                # TODO
                if successors is not None and i == j and new_dist < 0:
                    successors = None

                if new_dist < result[i][j]:
                    result[i][j] = new_dist
                    if successors is not None:
                        successors[i][j] = successors[i][intermediate]

    return result, successors

# * Adapté de https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm#Path_reconstruction
def calculate_path(successors, u, v):
    path = []
    if successors[u][v] is not None:
        path.append(u)
        while u is not v:
            u = successors[u][v]
            path.append(u)
    return path

#trouver une liste des sommets dans les circuits absorbant
def extract_neg_node(matrix_graph):
    list_node_neg = []
    
    for i in range(len(matrix_graph)):
        if matrix_graph[i][i] < 0:
            list_node_neg.append(i)
    
    if len(list_node_neg) == 0:
        return None

    return list_node_neg
        