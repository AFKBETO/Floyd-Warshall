"""
Ce fichier contient des méthodes liées à algorithme de Floyd-Warshall.
"""

from math import inf


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

    # Distance du chemin direct de I à J et chemin indirect passant par K
    for k in range(0, n):
        for i in range(0, n):
            for j in range(0, n):
                new_dist = result[i][k] + result[k][j]

                if successors is not None and i == j and new_dist < 0:
                    successors = None

                if new_dist < result[i][j]:
                    result[i][j] = new_dist
                    if successors is not None:
                        successors[i][j] = successors[i][k]

    return result, successors


def calculate_path(successors, u, v):
    if successors[u][v] is None:
        return []
    path = [u]
    while u is not v:
        u = successors[u][v]
        path.append(u)
    return path
