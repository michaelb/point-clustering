"""
cluster of points
"""
MAX_ID = 0


class Cluster_sqrt2:
    """
    a cluster is a set of points
    """
    def __init__(self, cases, count):
        """
        init a cluster
        """
        global MAX_ID
        self.cases = cases
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
            self.cases += other.cases
            self.count += other.count
            for case in other.cases:
                case.cluster = self
