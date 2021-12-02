#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ce fichier contient des méthodes utilitaires diverses.
"""

#   Convertir d'une chaîne de chiffres à un résultat entier
#   Paramètres :
#       raw     : la chaîne à traiter
#   Retourne :
#       integer : l'entier sous forme int - None si hors format
def parse_number(raw):
    try:
        return int(raw)
    except:
        return None
