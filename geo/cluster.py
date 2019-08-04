"""
cluster of points
"""
MAX_ID = 0


class Cluster:
    """
    a cluster is a set of points
    """
    def __init__(self, points = [], count = 0):
        """
        init a cluster
        """
        global MAX_ID
        self.points = points
        self.count = count
        self.ID = MAX_ID #Utile pour tester l'égalité entre deux clusters en complexité 1
        MAX_ID += 1

    def merge_with(self,other):
        """
        Fusionne deux_clusters ; modifie les points concernés
        complexité : O(min(taille self, taille other))
        """
        if self.ID != other.ID: #Permet de s'affranchir des cas ou on fusionnerait deux  listes
                                #ayant des éléments en commun
            if other.count > self.count:
                other, self = self, other #Permet de faire la fusion la moins couteuse
            self.points.extend(other.points)
            self.count += other.count
            for point in other.points:
                point.cluster = self

    def merge_with_all(self, L):
        points_to_add = []
        for other in L:
            if self != other: #Permet de s'affranchir des cas ou on fusionnerait deux  listes
                                    #ayant des éléments en commun
                if other.count > self.count:
                    other, self = self, other #Permet de faire la fusion la moins couteuse
                self.points.extend(other.points)
                self.count += other.count
                points_to_add.extend(other.points)
        for point in points_to_add:
            point.cluster = self

