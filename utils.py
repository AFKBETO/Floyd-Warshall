#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ce fichier contient des méthodes utilitaires diverses.
"""

#   Lecture d'une chaîne de chiffres
#   Paramètres :
#       raw     : la chaîne à traiter
#   Retourne :
#       integer : le nombre sous forme int - None si hors format
def parse_number(raw):
    try:
        return int(raw)
    except:
        return None
