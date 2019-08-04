"""
Module implémentant la classe case
une case est un élément du quadrillage contenant des points
"""


class Case:
    """classe Case"""
    def __init__(self):
        self.empty = True

    def add(self, point):
        self.empty = False
