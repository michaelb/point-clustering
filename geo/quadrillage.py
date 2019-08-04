"""
Module implémentant une classe de quadrillage
On découpe le plan en des carrés, et on place les points dans le quadrillage correspondant
"""

from itertools import product
from math import ceil, floor, sqrt
from geo.point import Point
from collections import defaultdict

class Quadrillage:
    """classe Quadrillage
    On suppose toujours le plan comme etant x, y dans [0,1[^2
    """
    def __init__(self, distance):
        self.coord_max = ceil(1 / distance) - 1
        self.taille_maillage = distance
        self.cases = defaultdict(list)
    
    def __iter__(self):
        """itere sur les cases de grille mais dans un ordre non trivial
        c'est-a-dire d'abord en selon les x croissants puis les y croissants
        (ecrire mais en partant de la ligne du bas)"""
        x_max, y_max = self.coord_max +1, self.coord_max +1
        for x,y in product(range(x_max), range(y_max)):
            yield self.cases[(x,y)], [x,y]

    def iter_voisins_case(self,coordonees):
        """itère sur les cases voisines de la case de coordonnees (x, y), y compris elle-même
        on omet exprès quelques cases qui ont déjà été parcourues (tout coté gauche et celle en dessous)
        car on parcours les cases de grille dans un ordre bien determiné, ca marche"""
        x_case, y_case = coordonees
        for x,y in product((0,1), repeat = 2): #le carré de 4 cases dont <case> occupe celui en bas à gauche
            if 0 <= x + x_case <= self.coord_max and 0 <= y + y_case <= self.coord_max:
               yield self.cases[x + x_case ,y + y_case]

        if x_case >= 1 and y_case + 1  <= self.coord_max:
            yield self.cases[x_case -1, y_case +1]
    
    def case_correspondante(self, point):
        """renvoie les coordonnes de la case correspondant à un point"""
        x_point, y_point = point.coordinates
        return (floor(x_point / self.taille_maillage), floor(y_point / self.taille_maillage))
    
    def remplissage(self, liste_points):
        """replit un quadrillage avec une liste de points donnée en argument"""
        for point in liste_points:
            self.cases[self.case_correspondante(point)].append(point)









def iter_voisins_case_sqrt2(self,coordonees):
        """itère sur les cases voisines de la case de coordonnees (x, y)"""
        x_case, y_case = coordonees
        for x,y in product((-2,-1, 0, 1, 2), repeat = 2):
            if abs(x*y) <= 2  and 0 <= x + x_case <= self.coord_max and 0 <= y + y_case <= self.coord_max:
                yield self.cases[x + x_case ,y + y_case]









