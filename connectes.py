#!/usr/bin/env python3

"""
compute sizes of all connected components.
sort and display.
"""


from math import floor, sqrt, pi, log
from collections import defaultdict
from sys import argv
from os import nice, name
if name == "posix": #on ne sait jamais, au cas ou vous puissiez être sous Windows :-)
    nice(1) #set highest priority available to the python executer

from geo.point import Point


def load_instance(filename):
    """
    loads .pts file.
    returns distance limit and points.
    """
    with open(filename, "r") as instance_file:
        lines = iter(instance_file)
        distance = float(next(lines))
        points = [Point([float(f) for f in l.split(",")]) for l in lines]
    return distance, points

def facteur_optimal(distance, longueur_liste_points, dimension=2):
    """renvoie un facteur optimal pour la taille des carrés du quadrillage,
    (optimal tant que l'entrée est une distribution aléatoire uniforme)"""

    def approximation(dimension): #la percolation se comporte un peu différement dans les espaces de dimension différentes
        if dimension == 1:
            return sqrt(2)# cela aide à refléter le phénomène
        if dimension == 2:
            return 1
        if dimension >= 3:
            return 0.8 + 0.04 * dimension

    caracteristique = approximation(dimension)* distance * (longueur_liste_points)**(1/dimension)
    #cette valeur est très importante, elle traduit la densité des points relativement à la distance
    # et est donc une caractéristique exacte de la taille des clusters dans la distribution

    if caracteristique <= pi/24:              #presque 99.9% de points solitaires
        return 1/caracteristique
    elif pi/24 < caracteristique <= 0.5:     #on commence a avoir des clusters non unitaires
        return -3.75 * caracteristique + 2.85
    elif 0.5 < caracteristique < pi/2:        #clusters de taille relativement grande (>1% du nombre de points)
        return 1
                             #caractéristique >=pi/2, peu de clusters qui sont énormes
    return -caracteristique  #on va utiliser les programmes de connectes_sqrt2.py

def limites(points):
    """renvoie les coordonées max, min et la dimension de l'entrée"""
    dimension = len(points[0].coordinates)
    max_coordinates = [max([p.coordinates[i] for p in points]) for i in range(dimension)]
    min_coordinates = [min([p.coordinates[i] for p in points]) for i in range(dimension)]
    return max_coordinates, min_coordinates, dimension

def est_aleatoire(points, cmax, cmin):
    """renvoie à quel point l'entrée est 'aléatoire'
    forcément en dimension 2 et + de 1000 points"""
    from random import sample
    from geo.quadrillage_sqrt2 import Quadrillage_sqrt2
    s = floor(sqrt(len(points)) + 100)
    echantillon = sample(points, s)
    decoupe = 1 / sqrt(s) * sqrt(2)
    grille = Quadrillage_sqrt2(decoupe)
    grille.remplissage(echantillon)
    freq = []
    for _, case in grille:
        if case.count:
            freq.append(case.count / s)
    entropie = sum([x * log(x, 2) for x in freq if x != 0])
    qte_info_fisher = - entropie / log(s, 2)
    return qte_info_fisher > 0.5# on calcule les probas sur les points de l'echantillon d'etre dans une case donnée, probas qu'on place dans la liste freq, puis calcule entropie et info pour pouvoir dire si la liste a l'air random

def scale(points, distance, max_coordinates, min_coordinates):
    """met à l'échelle (=> dans le carré (ou cube, etc...) unité)"""
    pmin = Point(min_coordinates)
    echelle = 1 / (max(max_coordinates) - min(min_coordinates))
    nvpoints = []
    for p in points:
        nvpoints.append((p - pmin) * echelle)
    return nvpoints, distance * echelle


def print_components_sizes(distance, points):#juste un sélecteur maintenant
    """
    selectionne les fonctions optimales dans chaque cas
    """
    if not points:#au cas où liste vide
        print([])
        return None
    if distance == 0:
        print_components_sizes_distance_zero(points)
        return None

    max_coordinates, min_coordinates, dimension = limites(points)

    if len(points) <= 1000:#les test statistiques ont peu de sens sinon:
        print_components_sizes_not_random(distance, points, dimension, min_coordinates, max_coordinates)
        return None

    if dimension == 2 and not (0.8 < max(max_coordinates) <= 1 and 0 <= min(min_coordinates) < 0.2): #mettre à l'échelle si c'est pas terrible
        points, distance = scale(points, distance, max_coordinates, min_coordinates)             #plus calcul du facteur de percolation
        facteur_percolation = facteur_optimal(distance, len(points), dimension)                  #(nom peut-être pas 100% approprié vu qu'il dépend
    else:                                                                                            #aussi de résultats statistiques)
        facteur_percolation = facteur_optimal(distance, len(points), dimension)





    if dimension == 2 and est_aleatoire(points, max_coordinates, min_coordinates):         #on utilise les fonctions basées sur quadrillage
        if facteur_percolation > 0:                                                     #if facteur <= 0, on utilise un autre algo il y a trop de points qui se touchent
            print_components_sizes_standart(distance, points, max(1, facteur_percolation))
        else:
            print_components_sizes_sqrt2(distance, points, -facteur_percolation)          #ici uniquement ce facteur est juste la caractéristique

    else:#plus lent, mais marche en toute dimension et avec des distributions non aleatoires concues pour embeter quadrillage
        print_components_sizes_not_random(distance, points, dimension, min_coordinates, max_coordinates) #on pourrait mais n'utilise pas facteur_percolation
                                                                                                        #car cela a peu de sens pour des distribution non-random
                                                                                                        #et les cas 3D+ nous intéressent moins








def print_components_sizes_distance_zero(points):
    """renvoie rapidement le résultat si la distance est nulle"""
    result = []
    d = {} #dictionnaire ayant pour clés les points et pour valeurs le nombre de points 'superposés' dans le même cluster
    for p in points: #si distance == 0 alors il suffit de compter les points identiques
        if p in d.keys():
            d[p] += 1
        else:
            d[p] = 1
    for val in d:
        result.append(d[val])
    print(sorted(result, reverse=True))

def print_components_sizes_standart(distance, points, facteur_percolation):
    """affiche les tailles des composantes connexes"""
    from geo.quadrillage import Quadrillage
    distance2 = distance ** 2
    grille = Quadrillage(distance * facteur_percolation) #Crée un quadrillage vide
    grille.remplissage(points)                         #On remplit le quadrillage
    for case, coordonees_case in grille:
        for point in case:
            for case_voisine in grille.iter_voisins_case(coordonees_case):    #On regarde les cases voisines
                for autre_point in case_voisine:                              #Et les points dans ces cases
                    if point.distance_carre_to(autre_point) <= distance2:
                        point.cluster.merge_with(autre_point.cluster)

    longueurs = []
    ID_prises = defaultdict(bool) #On utilise defaultdict car ainsi vérifier qu'un cluster a été
                                  #parcouru est en O(1)
    for point in points:          #on compte le nombre de points dans chaque cluster
        if not ID_prises[point.cluster.ID]:
            ID_prises[point.cluster.ID] = True
            longueurs.append(point.cluster.count)
    print(sorted(longueurs, reverse=True))

def ultra_dense(distance, points):
    """vérifie rapidement si une condition suffisante
    à ce que tous les points soient liés est remplie"""
    from geo.point_sqrt2 import Point
    from geo.quadrillage_dense import Quadrillage_dense
    grille = Quadrillage_dense(distance / sqrt(8)) #si toutes les cases de ce quadrillage sont pleines forcément on
    grille.remplissage(points)                   #un seul gros cluster réunissant tous les points
    limite = 0
    for _, case in grille:
        if case.empty: #case a déjà été importé dans le contexte de 'sqrt2'
            limite += 1
    if limite > 2: #si on a plus de 2 cases vides on ne peut pas conclure
        return False
    #sinon on a bien un seul gros cluster
    print([len(points)])
    return True

def print_components_sizes_sqrt2(distance, points, caracteristique):
    """
    affichage des tailles triees de chaque composante
    methode par quadrillage de taille distance/sqrt(2)
    """
    from geo.quadrillage_sqrt2 import Quadrillage_sqrt2
    from geo.case import Case

    if  caracteristique > 10* sqrt(2) and ultra_dense(distance, points): #le 10* sqrt(2) n'est pas un hasard
        return None #avec la condition ^ + 'aleatoire' on est quasi sûr que le problème ne comprend qu'un seul cluster
                    #mais il faut utiliser ultra_dense avec precaution car si il y a plus qu'une composante on doit lancer le 'vrai' algo_sqrt2
                    #et on aura perdu du temps
    distance2 = distance ** 2
    grille = Quadrillage_sqrt2(distance / sqrt(2))  #Crée un quadrillage vide
    grille.remplissage(points)                     #On remplit le quadrillage
    for coords, case in grille:                    #On parcours la grille par case
        for case_voisine in grille.iter_parcours(coords):
            if case.liee_a(case_voisine, distance2):
                case.cluster.merge_with(case_voisine.cluster)
    longueurs = []
    ID_prises = defaultdict(bool) #On utilise defaultdict car ainsi vérifier qu'un cluster a été
                                  #parcouru est en O(1)

    for _, case in grille:
        if not ID_prises[case.cluster.ID] and case.cluster.count:
            ID_prises[case.cluster.ID] = True
            longueurs.append(case.cluster.count)
    print(sorted(longueurs, reverse=True))

def print_components_sizes_not_random(distance, points, dimension, min_coo, max_coo):
    """
    affichage des tailles triees de chaque composante
    methode par r-tree de taille distance
    il est conseillé de fold (replier) les fonctions create_tree* pour une
    meilleure compréhension du programme
    """
    from geo.quadrant import Quadrant
    from itertools import product

    def condition_continue(quadrant, distance):
        """condition selon laquelle on continue la recursion pour créer l'arbre,
        on s'arrete ou on passe aux quadrants denses"""
        if (len(quadrant.extended.list_point_inside) > 256) and (quadrant.taille('max') <= 3 * distance):
            return -1
        return (len(quadrant.list_point_inside) > 8) and (quadrant.taille('max') > 2 * distance)

    def condition_continue_dense(quadrant, distance):
        """permet de stopper la recursion pour les quadrants denses"""
        dimension = len(quadrant.min_coordinates)
        return (len(quadrant.list_point_inside) > 0) and (quadrant.taille('max') > distance / sqrt(dimension))

    def create_tree_dense(root, distance, globalroot):
        """à partir du quadrant dense root on crée un r-tree (remplit) de taille appropriée
        par ex en 2D cette fonction rajoute à l'arbre 4 quadrants découpant le root en quatre:
        de coordinates
        (xmin,ymin,xmoy,ymoy),(xmin,ymoy,xmoy,ymax), (xmoy, ymin, xmax,ymoy), (xmoy, ymoy, xmax,ymax)
        le reste se fait par la magie de la récursivité"""
        root.dense = True
        if condition_continue_dense(root, distance):
            Lchilds = []
            lmax = [x for x in root.max_coordinates]
            lmin = [x for x in root.min_coordinates]
            lmoy = [(x + y) / 2 for x, y in zip(lmax, lmin)]
            L_liste_coordinates_child_min = []
            L_liste_coordinates_child_max = []
            for mi, mo, ma in zip(lmin, lmoy, lmax):
                L_liste_coordinates_child_min.append([mi, mo])
                L_liste_coordinates_child_max.append([mo, ma])
            bon_iterable = zip(product(*L_liste_coordinates_child_min), product(*L_liste_coordinates_child_max))
            for coomins, coomaxs in bon_iterable:
                Lchilds.append(Quadrant(coomins, coomaxs))
            for child in Lchilds:
                for p in root.list_point_inside:
                    if child.contain(p):
                        child.list_point_inside.append(p)
                #child.minimal_bounding()   #can be interesting in some cases,
                                            #though it has a 'high' O(nbr_points_in_quadrant) complexity
                root.childs.append(child)
                child.parent = root
                create_tree_dense(child, distance, globalroot)
        else:
            globalroot.leafs.append(root)

    def create_tree(root, distance, globalroot):
        """à partir du quadrant root on crée un r-tree (remplit) de taille appropriée
        par ex en 2D cette fonction rajoute à l'arbre 4 quadrants découpant le root en quatre:
        de coordinates
        (xmin,ymin,xmoy,ymoy),(xmin,ymoy,xmoy,ymax), (xmoy, ymin, xmax,ymoy),(xmoy, ymoy, xmax,ymax)
        sans oublier d'avoir d'agrandir de distance les quadrants pour avoir tous les points (c'est un peu plus
        compliqué mais c'est l'idée"""
        continuer = condition_continue(root, distance)
        if continuer > 0:
            Lchilds = []


            #tout cela sert à découper le quadrant parent en quadrants enfants
            lmax = [x for x in root.max_coordinates]
            lmin = [x for x in root.min_coordinates]
            lmoy = [(x + y) / 2 for x, y in zip(lmax, lmin)]
            L_liste_coordinates_child_min = []
            L_liste_coordinates_child_max = []
            for mi, mo, ma in zip(lmin, lmoy, lmax):
                L_liste_coordinates_child_min.append([mi, mo])
                L_liste_coordinates_child_max.append([mo, ma])
            bon_iterable = zip(product(*L_liste_coordinates_child_min), product(*L_liste_coordinates_child_max))
            for coomins, coomaxs in bon_iterable:
                Lchilds.append(Quadrant(coomins, coomaxs))

            #on ajoute les points_inside et le quadrant agrandi aux enfants, qu'on ajoute finalement au parent
            for child in Lchilds:
                child.extended = child.copy()
                child.extended.inflate(distance)
                for p in root.extended.list_point_inside:
                    if child.extended.contain(p):
                        child.extended.list_point_inside.append(p)
                        if child.contain(p):
                            child.list_point_inside.append(p)
                #child.minimal_bounding()   #can be interesting in some cases,
                                            #though it has a 'high' O(nbr_points_in_quadrant) complexity
                root.childs.append(child)
                child.parent = root
                create_tree(child, distance, globalroot)

        #on décide si on continue ou pas la recursion, voire passer en mode dense
        elif continuer == 0:
            globalroot.leafs.append(root)
        else: #continuer <0
            create_tree_dense(root, distance, globalroot)


    #"""modifie la liste de points en les regroupants en (cluster de) composantes connexes"""
    #debut du programme :-)
    distance2 = distance ** 2
    Root = Quadrant(min_coo, max_coo)
    Root.extended = Root
    Root.list_point_inside = points
    create_tree(Root, distance, Root)#on crée un r-tree (spécial)

    dense_leafs = [quadrant for quadrant in Root.leafs if quadrant.dense] #les quadrants denses sont de cotés <=1/sqrt(dimension) donc tous les points intérieurs sont liés
    normal_leafs = [quadrant for quadrant in Root.leafs if not quadrant.dense]

    #on va fusionner tous les points dans les mêmes quadrants denses dans les mêmes clusters
    for quadrant in dense_leafs: #on fusionne tous les clusters dans les quadrants denses
        if quadrant.list_point_inside: #if not empty
            p1 = quadrant.list_point_inside[0]
            p1.cluster.merge_with_all([point.cluster for point in quadrant.list_point_inside])
    #on va fusionner les clusters des points dans des quadrants denses différents
    for quadrant in dense_leafs:
        for another_quadrant in dense_leafs:
            if quadrant.lies(another_quadrant, distance):
                quadrant.list_point_inside[0].cluster.merge_with(another_quadrant.list_point_inside[0].cluster)


    for quadrant in normal_leafs: #on fusionne tous les clusters dans les quadrants normaux
        for p1 in quadrant.list_point_inside:
            for p2 in quadrant.extended.list_point_inside:
                if p1.distance_carre_to(p2) <= distance2:
                    p1.cluster.merge_with(p2.cluster)

    longueurs = []
    ID_prises = defaultdict(bool) #On utilise defaultdict car ainsi vérifier qu'un cluster a été
                                  #parcouru est en O(1)
    for point in points:
        if not ID_prises[point.cluster.ID]:
            ID_prises[point.cluster.ID] = True
            longueurs.append(point.cluster.count)
    print(sorted(longueurs, reverse=True))










def main():
    """
    ne pas modifier: on charge une instance et on affiche les tailles
    """
    for instance in argv[1:]:
        distance, points = load_instance(instance)
        print_components_sizes(distance, points)


main()
