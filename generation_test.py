#!/usr/bin/env python3

"""
Module de création de fichiers d'ensembles de test
"""
from math import floor, sqrt
from random import random
import numpy as np

def generation_fichier(nb_points, distance_liaison, chemin="qg2 > gq1.pts"):
    with open(chemin, "w") as fichier:
        fichier.write(str(distance_liaison) + "\n")
        for _ in range(nb_points//2):
            fichier.write("{}, {}\n".format(str(random()),str(random())))
        for _ in range(nb_points//4):
            fichier.write("{}, {}\n".format(str(random()/2+0.25),str(random()/10+0.6)))
        for _ in range(nb_points//4):
            fichier.write("{}, {}\n".format(str((random()>0.5)/2+0.15+random()/10),str(random()/10+0.3)))
        



def generation_ensemble_de_test():
    for n in [1,0.5,0.25,0.1,0.05,0.4,0.3,0.2,0.1,0.09,0.8,0.08,0.07,0.06,0.05,0.04,0.03,0.02,0.01,0.009,0.008,0.007,0.006,0.004,0.005,0.003,0.002,0.001]:
        generation_fichier(10000,n, "test_{}.pts".format(str(n)))

def generation_quadrillage(distance):
    with open("test_quadrillage", "w") as fichier:
        fichier.write(str(distance) + "\n")
        distance -= 0.000000001
        x = 0
        while x < 1:
            y = 0
            while y < 1:
                fichier.write("{},{}\n".format(str(x),str(y)))
                y += distance
            x += distance
#generation_quadrillage(0.01)
#generation_ensemble_de_test()
generation_fichier(10000,0.01)
