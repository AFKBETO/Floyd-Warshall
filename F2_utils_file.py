#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ce fichier contient des méthodes utilitaires pour la lecture et validation du programme.
"""

from math import inf
from F2_utils import parse_number

#   Lecture de fichier
#   Paramètres :
#       file_path   : le fichier contiennant le graphe à traiter
#   Retourne :
#       matrix      : la matrice représantant le graphe - None s'il y a des erreurs
#       error_msg   : le message d'erreur (s'il y en a)
def parse_matrix_from_file(file_path):

    with open(file_path, 'r') as f:
        lines = [l.strip() for l in f.readlines() if len(l.strip()) is not 0]

        if len(lines) < 3:                  # vérification des données
            return None, "SYNTAX ERROR: File does not contain enough graph data."

        node_count = parse_number(lines[0])
        edge_count = parse_number(lines[1])
        if node_count == None:              # nombre des sommets hor format
            return None, "SYNTAX ERROR: Wrong node count format"
        if edge_count == None:              # nombre des arcs hor format
            return None, "SYNTAX ERROR: Wrong edge count format"
        if not edge_count == len(lines)-2:  # mauvais nombre des arcs
            return None, "DATA ERROR: Wrong edge count or not enough edge data."
        
        # initialisation de la matrice représantant du graphe
        matrix = [[inf for i in range(node_count)] for i in range(node_count)]

        # lecture des données d'arcs
        for i in range(2, edge_count + 2):
            split = lines[i].split(' ')
            print(split)
            # essaie de passer la donnée en entier
            a = parse_number(split[0])
            b = parse_number(split[1])
            weight = parse_number(split[2])
            if a == None or b == None:      # extrémités hors format
                return None, "SYNTAX ERROR: Wrong endpoint format: Line " + str(i+1)
            if weight == None:              # poids hors format
                return None, "SYNTAX ERROR: Wrong edge weight format: Line " + str(i+1)
            if a < 0 or a > edge_count:     # mauvaise extrémité initiale
                return None, "DATA ERROR: Tail node out of bound: Line " + str(i+1)
            if b < 0 or b > edge_count:     # mauvaise extrémité terminale
                return None, "DATA ERROR: Head node out of bound: Line " + str(i+1)
            if matrix[a][b] == inf:         # détection d'arcs multiples
                matrix[a][b] = weight
            else:
                return None, "GRAPH ERROR: Multiple edges with same endpoints detected: Line " + str(i+1)

    return matrix, None


