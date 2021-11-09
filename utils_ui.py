#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ce fichier contient des méthodes utilitaires pour l'interaction avec l'utilisateur et l'affichage.
"""

from os.path import exists
from os.path import dirname
from os.path import join

__GRAPHS_FOLDER = join(dirname(__file__), 'graphs')


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


def ask_file_path(message):
    print(message)
    file_name = input()
    # vérifier si l'utilisateur souhaite quitter
    if file_name in ['N','n','Non','No','Q','q','Quit','quit','non','no', 'NON', 'NO','QUIT']:
        return None,None
    if not '.' in file_name:
        file_name = file_name + '.txt'
    file_path = join(__GRAPHS_FOLDER, file_name)
    if not exists(file_path):
        return None, file_path
    return file_path, None


def print_matrix(matrix):
    for line in matrix:
        pretty = ''
        for nb in line:
            pretty += str(nb) + '\t'
        print(pretty)



