#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ce fichier contient des méthodes utilitaires pour l'interaction avec l'utilisateur et l'affichage.
"""

from os.path import exists
from os.path import dirname
from os.path import join
from os import makedirs

__GRAPHS_FOLDER = join(dirname(__file__), 'f2_graphs') # chemin du dossier des graphes
__OUTPUT_FOLDER = join(dirname(__file__), 'f2_output') # chemin du dossier des traces d'exécution

#   Demande confirmation Oui/Non
#   Paramètres :
#       message : la question à afficher
#   Retourne :
#       True/False
def ask_boolean(message):
    print(message)
    return input() in ['Y', 'y', 'yes', 'Yes', 'oui', 'Oui', 'O', 'o']


#   Demande d'un nombre
#   Paramètres :
#       message : la question à afficher
#   Retourne :
#       integer - None si hors format
def ask_number(message):
    print(message)
    raw = input()
    try:
        return int(raw)
    except:
        return None


#   Demande d'un fichier
#   Paramètres :
#       message     : la question à afficher
#   Retourne :
#       file_path   : le chemin du fichier
#       file_name   : le nom du fichier
#       path_error  : si et seulement si le fichier non trouvé
def ask_file_path(message):
    print(message)
    file_name = input()
    # Vérification si l'utilisateur souhaite quitter
    if file_name in ['N','n','Non','No','Q','q','Quit','quit','non','no', 'NON', 'NO','QUIT']:
        return None,None,None
    if not '.' in file_name:
        file_name = file_name + '.txt'
    file_path = join(__GRAPHS_FOLDER, file_name)
    # Vérification si le fichier existe :
    if not exists(file_path):
        return None, file_name, file_path   # retourne de chemin est None
    return file_path, file_name, None       # retourne le chemin du fichier et son nom s'il existe


#   Afficher une matrice
#   Paramètres :
#       matrix  : la matrice à afficher
#   Retourne :
#       None
def print_matrix(matrix):
    for line in matrix:
        pretty = ''
        for nb in line:
            pretty += str(nb) + '\t'
        print(pretty)


#   Ajouter une matrice dans un fichier
#   Paramètres :
#       file_name   : nom du fichier
#       matrix      : la matrice à ajouter
#   Retourne :
#       None
def write_matrix(file_name, matrix):
    for line in matrix:
        pretty = ''
        for nb in line:
            if len(str(nb)) >= 4:
                pretty += str(nb) + '\t'    
            else:
                pretty += str(nb) + '\t\t'
        write_line(file_name,pretty)

#   Ajouter une ligne de texte dans un fichier
#   Paramètres :
#       file_name   : nom du fichier
#       text        : le texte à ajouter
#   Retourne :
#       None
def write_line(file_name, text):
    if not exists(__OUTPUT_FOLDER):
        makedirs(__OUTPUT_FOLDER)
    file_path = join(__OUTPUT_FOLDER,file_name)
    with open(file_path,'a',encoding='utf-8') as f:
        f.write('\n'+text)


#   Vider le fichier(si existe) et ajouter à nouveau
#   Paramètres :
#       file_name   : nom du fichier
#       text        : le texte à ajouter
#   Retourne :
#       None
def write_new(file_name, text):
    if not exists(__OUTPUT_FOLDER):
        makedirs(__OUTPUT_FOLDER)
    file_path = join(__OUTPUT_FOLDER,file_name)
    with open(file_path,'w',encoding='utf-8') as f:
        f.write(text+'\n')