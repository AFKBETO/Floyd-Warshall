#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ce fichier contient la logique d'exécution du programme.
"""
from math import isinf
from F2_utils_ui import ask_boolean
from F2_utils_ui import ask_number
from F2_utils_ui import ask_file_path
from F2_utils_ui import print_matrix
from F2_utils_ui import write_line, write_matrix,write_new
from F2_utils_file import parse_matrix_from_file
from F2_floyd_warshall import calculate_path, extract_neg_node
from F2_floyd_warshall import floyd_warshall


def main():

    diviseur = "\n\t - - - - - - - -"

    while True:

        # Choix du fichier et validation, ou quitter
        file_path, file_name, error = ask_file_path("\nChoose the name of the file containing the graph you want to analyze (press N or Q to quit):")
        if file_path is None:
            # Vérification si error est None (quitter)
            if error is None:
                return
            print("ERROR: File not found:",error)
            write_new(file_name, f"ERROR: File not found: {error}")
            continue

        # Lecture de la matrice
        matrix, error = parse_matrix_from_file(file_path)
        if matrix is None:
            write_new(file_name, error)
            print(error)
            continue
        
        # Initialisation du fichier de traces d'exécution
        write_new(file_name,f"Source: {file_path}")
        node_count = len(matrix)
        
        # Affichage de la matrice représantant du graphe
        print(f"{diviseur}\nMatrix representation of the graph :")
        print_matrix(matrix)

        write_line(file_name,f"{diviseur}\nMatrix representation of the graph :")
        write_matrix(file_name,matrix)

        # Détection des boucles négatives
        for x in range(len(matrix)):
            if matrix[x][x] < 0:
                print("Negative self-loop at " + str(x))
                write_line(file_name, f"\nNegative self-loop at {str(x)}")


        # Calcul de Floyd-Warshall
        fw_matrix, fw_successors = floyd_warshall(file_name,matrix)
        print(f"{diviseur}\nAnalysis complete. Path matrix of this graph:")
        print_matrix(fw_matrix)

        write_line(file_name,f"{diviseur}\nAnalysis complete. Path matrix of this graph:")
        write_matrix(file_name,fw_matrix)

        # Récupération des sommets affectés par les circuits absorbants
        neg_list = extract_neg_node(fw_matrix)

        # Détection de circuit absorbant
        if len(neg_list):
            print(f"{diviseur}\nGraph contains at least a cycle with negative weight (présence d'un circuit absorbant).")
            write_line(file_name,f"{diviseur}\nGraph contains at least a cycle with negative weight (présence d'un circuit absorbant).")
            print("List of nodes concerned:")
            write_line(file_name,"List of nodes concerned:")
            print(neg_list)
            write_line(file_name,f"{neg_list}")

        
        # Affichage des chemins
        if ask_boolean(f"{diviseur}\nDo you want to list every shortest path possible [Y/N]?"):
            count = 0       # compter le nombre de chemins
            for i in range(node_count):
                for j in range(node_count):
                    # Vérification s'il n'y a pas de chemin ou les sommets de départ et d'arrivée
                    # sont identiques
                    if isinf(fw_matrix[i][j]) or i == j:
                        continue
                    else:
                        path_constructed = calculate_path(fw_successors,neg_list, i, j)
                        if len(path_constructed):
                            print("\t", i, "->", j, ":", str(path_constructed).replace('[', '').replace(']', ''))
                            count = count + 1
            if count == 0:  # quand il n'y a pas de chemin le plus court dans le graphe
                print("There is no shortest path in this graph.")
        else:
            # Affichage du chemin au choix
            print(f"{diviseur}")
            while ask_boolean("Do you want to show the shortest path between two nodes of your choice [Y/N]?"):
                i = ask_number("Input starting node:")
                while i is None or i < 0 or i + 1 > node_count:
                    print("ERROR: Node not found.\n")
                    i = ask_number("Input starting node:")
                j = ask_number("Input ending node:")
                while j is None or j < 0 or j + 1 > node_count:
                    print("ERROR: Node not found.\n")
                    j = ask_number("Input ending node:")
                if isinf(fw_matrix[i][j]):
                    print("\t", i, "->", j, ": Does not exist")
                else:
                    path_constructed = calculate_path(fw_successors,neg_list, i, j)
                    if len(path_constructed):
                        print("\t", i, "->", j, ":", str(path_constructed).replace('[', '').replace(']', ''))
                    else:
                        print("\t", i, "->", j, ": No shortest path possible")
                    print("\n")


if __name__ == '__main__':
    main()
