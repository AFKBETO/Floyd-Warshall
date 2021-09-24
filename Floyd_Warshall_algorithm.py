from os.path import exists
from os.path import dirname
from os.path import join
from math import inf

input_folder = join(dirname(__file__), 'graphs')


def print_matrix(matrix):
    for line in matrix:
        pretty = ''
        for nb in line:
            pretty += str(nb) + '\t'
        print(pretty)


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


def path(successors, u, v):
    if successors[u][v] is None:
        return []
    path = [u]
    while u is not v:
        u = successors[u][v]
        path.append(u)
    return path


def ask_boolean(message):
    print(message)
    return input() in ['Y', 'y', 'yes', 'Yes', 'oui', 'Oui', 'O', 'o']


def ask_number(message):
    print(message)
    raw = input()
    try:
        return int(raw)
    except:
        return None

def check_number(raw):
    try:
        return int(raw)
    except:
        return None


def main():
    first_time = True
    haserror = False

    while True:

        # Quitter le programme ?
        if not first_time and not ask_boolean("\nDo you want to analyze another graph [Y/N] ?"):
            return
        first_time = False

        # Choix du fichier et validation
        print("\nChoose the file containing the graph you want to analyze:")
        file_name = input()
        file_path = join(input_folder, file_name)

        if not exists(file_path):
            print("ERROR: File not found.")
            continue

        # Lecture de la matrice
        with open(file_path, 'r') as f:
            lines = [l.strip() for l in f.readlines()]

            if len(lines) < 3: #vérification des données
                print("SYNTAX ERROR: File does not contain enough graph data.")
                continue

            node_count = check_number(lines[0])
            edge_count = check_number(lines[1])
            if node_count == None: #nombre des sommets hor format
                print("SYNTAX ERROR: Wrong node count format")
                continue
            if edge_count == None: #nombre des arcs hor format
                print("SYNTAX ERROR: Wrong edge count format")
                continue
            if not edge_count == len(lines)-2: #mauvais nombre des arcs
                print("SYNTAX ERROR: Wrong edge count or not enough edge data.")
                continue
            
            matrix = [[inf for i in range(node_count)] for i in range(node_count)]

            for i in range(2, edge_count + 2):
                split = lines[i].split(' ')
                a = check_number(split[0])
                b = check_number(split[1])
                weight = check_number(split[2])
                if a == None or b == None: #extrémités hor format
                    print("SYNTAX ERROR: Wrong endpoint format: Line ",i+1)
                    haserror = True
                    break
                if weight == None: #poids hors format
                    print("SYNTAX ERROR: Wrong edge weight format: Line ",i+1)
                    haserror = True
                    break
                if a < 0 or a > edge_count: #mauvaise extrémité initiale
                    print("DATA ERROR: Tail node out of bound: Line ",i+1)
                    haserror = True
                    break
                if b < 0 or b > edge_count: #mauvaise extrémité terminale
                    print("DATA ERROR: Head node out of bound: Line ",i+1)
                    haserror = True
                    break
                if matrix[a][b] == inf: #détection de graphe multiple
                    matrix[a][b] = weight
                else:
                    print("GRAPH ERROR: Multiple edges with same endpoints detected: Line ",i+1)
                    haserror = True
                    break
        if haserror:
            continue
        
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
                            print("\t", i, "->", j, ":", str(path(fw_successors, i, j)).replace('[', '').replace(']', ''))
            while ask_boolean("\nDo you want to show the shortest path between two nodes of your choice [Y/N]?"):
                i = ask_number("Input starting node:")
                while i is None or i < 0 or i + 1 > node_count:
                    print("ERROR: Node not found.\n")
                    i = ask_number("Input starting node:")
                j = ask_number("Input ending node:")
                while j is None or j < 0 or j + 1 > node_count:
                    print("ERROR: Node not found.\n")
                    j = ask_number("Input ending node:")
                print("\t", i, "->", j, ":", str(path(fw_successors, i, j)).replace('[', '').replace(']', ''))


if __name__ == '__main__':
    main()
