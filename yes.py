
from os.path import exists
from os.path import dirname
from os.path import realpath
from os.path import join
from math import inf

input_folder = join(dirname(__file__), 'graphes')

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

def main():
    first_time = True

    while True:

        # Quitter le programme ?
        if not first_time and not ask_boolean("Tu veux traiter un nouveau graphe mec ? [Y/n] "):
            return
        first_time = False

        # Choix du fichier et validation
        print("Choisis ton graphe mec :")
        file_name = input()
        file_path = join(input_folder, file_name)

        if not exists(file_path):
            print("... ça marche pas")
            continue

        # Lecture de la matrice
        with open(file_path, 'r') as f:
            lines = [l.strip() for l in f.readlines()]

            if len(lines) < 3:
                print("... tu troll mec")
                continue

            node_count = int(lines[0])
            edge_count = int(lines[1])

            matrix = [[inf for i in range(node_count)] for i in range(node_count)]

            for i in range(2, edge_count + 2):
                split = lines[i].split(' ')
                a = int(split[0])
                b = int(split[1])
                weight = int(split[2])
                matrix[a][b] = weight
        
        # Affichage du graphe
        print("Ton graphe mec :")
        print_matrix(matrix)

        # Calcul de Floyd-Warshall
        fw_matrix, fw_successors = floyd_warshall(matrix)
        print("Ton résultat mec :")
        print_matrix(fw_matrix)

        # Détection de circuit absorbant
        if fw_successors is None:
            print("Y'a un circuit absorbant mec")
        
        # Affichage des circuits
        else:
            if ask_boolean("Tu veux afficher tous les chemins mec ? [Y/n] "):
                for i in range(node_count):
                    for j in range(node_count):
                        if fw_matrix[i][j] > 0:
                            print("\t", i, "->", j, ":", str(path(fw_successors, i, j)).replace('[', '').replace(']', ''))
            while ask_boolean("Tu veux afficher un chemin particulier mon reuf ? [Y/n] :"):
                i = ask_number("Premier sommet ? ")
                if i is None or i < 0 or i + 1 > node_count:
                    print("... tu troll")
                    continue
                j = ask_number("Second sommet ? ")
                if j is None or i < 0 or i + 1 > node_count:
                    print("... tu troll")
                    continue
                print("\t", i, "->", j, ":", str(path(fw_successors, i, j)).replace('[', '').replace(']', ''))

if __name__ == '__main__':
    main()
