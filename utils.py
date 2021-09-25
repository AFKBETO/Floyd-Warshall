"""
Ce fichier contient des méthodes utilitaires diverses.
"""


def parse_number(raw):
    try:
        return int(raw)
    except:
        return None
