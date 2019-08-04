"""
Module implémentant la classe case
une case est un élément du quadrillage contenant des points
"""

from geo.point import Point
from geo.cluster_sqrt2 import Cluster_sqrt2
from itertools import product

class Case:
    """classe Case"""
    def __init__(self, points=None, count=0):
        if points == None:
            self.points = []
        else:
            self.points = points
        self.count = count
        self.cluster = Cluster_sqrt2([self], count)

    def __iter__(self):
        for point in self.points:
            yield point

    def add(self, point):
        """ajoute un point à une case"""
        self.points.append(point)
        self.count += 1
        self.cluster.count += 1

    def liee_a(self, other, distance_carree):
        for point, autre_point in product(self.points, other.points):
            if point.distance_carre_to(autre_point) <= distance_carree:
                return True
        return False
