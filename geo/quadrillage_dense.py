"""
Module implémentant une classe de quadrillage
On découpe le plan en des carrés, et on place les points dans le quadrillage correspondant
"""

from itertools import product
from math import ceil, floor, sqrt
from geo.point import Point
from geo.case_dense import Case
from collections import defaultdict


class Quadrillage_dense:
    """classe Quadrillage
    On suppose toujours le plan comme etant x, y dans [0,1[^2
    """
    def __init__(self, distance, limites = [[0,0],[1,1]]):
        self.coord_max = ceil(1 / distance) - 1 #oui il faut que ca soit un carré
        self.taille_maillage = distance
        self.cases = defaultdict(Case)   
    
    def __iter__(self):
        """itère sur les cases du quadrillage"""
        for i, j in product(range(self.coord_max + 1), repeat = 2):
            yield (i, j), self.cases[(i, j)]

    def iter_parcours(self, coord_case):
        """
        itère sur les cases a proximité d'une case (mais pas elle-même) vers "l'avant", dans le
        cas d'un parcours du quadrillage via la méthode __iter__ (jariv pa a expliquer clairement
        aled
        o sekour
        plz)
        """
        x_case, y_case = coord_case
        for x, y in product([0,1,2], [-2,-1,0,1,2]):
            if x + x_case <= self.coord_max and 0 <= y + y_case <= self.coord_max: #pas sortir du carré
                if abs(x*y)  <= 2 and not( x==0 and y <= 0): #pas les coins , pas elle-même ni ce qu'il y a en dessous
                    yield self.cases[(x + x_case, y + y_case)]


    def case_correspondante(self, point):
        """renvoie les coordonnes de la case correspondant à un point"""
        x_point, y_point = point.coordinates
        return (floor(x_point / self.taille_maillage), floor(y_point / self.taille_maillage))
        
    def remplissage(self, liste_points):
        """replit un quadrillage avec une liste de points donnée en argument"""
        for point in liste_points:
            self.cases[self.case_correspondante(point)].add(point)
