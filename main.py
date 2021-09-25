#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ce fichier contient la logique d'exécution du programme.
"""

from utils_ui import ask_boolean
from utils_ui import ask_number
from utils_ui import ask_file_path
from utils_ui import print_matrix
from utils_file import parse_matrix_from_file
from floyd_warshall import calculate_path
from floyd_warshall import floyd_warshall


def main():
    first_time = True

    while True:

        # Quitter le programme ?
        if not first_time and not ask_boolean("\nDo you want to analyze another graph [Y/N] ?"):
            return
        first_time = False

        # Choix du fichier et validation
        file_path, error = ask_file_path("\nChoose the name of the file containing the graph you want to analyze:")
        if file_path is None:
            print("ERROR: File not found.")
            print("ERROR:", error)
            continue

        # Lecture de la matrice
        matrix, error = parse_matrix_from_file(file_path)
        if matrix is None:
            print(error)
            continue
        node_count = len(matrix)
        
        # Affichage du graphe
        print("\nMatrix representation of the graph :")
        print_matrix(matrix)

        # Calcul de Floyd-Warshall
        fw_matrix, fw_successors = floyd_warshall(matrix)
        print("\nAnalysis complete. Path matrix of this graph:")
        print_matrix(fw_matrix)

        # Détection de circuit absorbant
        if fw_successors is None:
            print("\nGraph contains a cycle with negative weight (présence d'un circuit absorbant).")
        
        # Affichage des circuits
        else:
            if ask_boolean("\nDo you want to list every shortest path possible [Y/N]?"):
                for i in range(node_count):
                    for j in range(node_count):
                        if fw_matrix[i][j] > 0:
                            print("\t", i, "->", j, ":", str(calculate_path(fw_successors, i, j)).replace('[', '').replace(']', ''))
            while ask_boolean("\nDo you want to show the shortest path between two nodes of your choice [Y/N]?"):
                i = ask_number("Input starting node:")
                while i is None or i < 0 or i + 1 > node_count:
                    print("ERROR: Node not found.\n")
                    i = ask_number("Input starting node:")
                j = ask_number("Input ending node:")
                while j is None or j < 0 or j + 1 > node_count:
                    print("ERROR: Node not found.\n")
                    j = ask_number("Input ending node:")
                print("\t", i, "->", j, ":", str(calculate_path(fw_successors, i, j)).replace('[', '').replace(']', ''))


if __name__ == '__main__':
    main()
