#!/usr/bin/env python3
"""Fonctions permettant l'écriture sur la sortie standart de liste de points/segments en svg. NE PAS OUBLIER LES BALISES"""

from geo.segment import Segment
from geo.point import Point
from math import floor

def print_segment(liste):
    """fonction capable d'imprimer les lignes svg pour les segments d'une liste 'liste'
    sur la sortie standart
    , à utiliser intelligement au vu de la postition des balises svg"""
    for segment in liste:
        print('<line x1="{}" y1="{}" x2="{}" y2="{}" stroke="red" stroke-width="2" />'.
              format(floor(1000*segment.endpoints[0].coordinates[0]),floor (1000*segment.endpoints[0].coordinates[1]),
                  floor(1000*segment.endpoints[1].coordinates[0]), floor(1000*segment.endpoints[1].coordinates[1])))


def print_points(liste):
    """fonction capable d'imprimer des cerles (en svg)
    correspondant aux points de la liste en argument"""
    for point in liste:
        print('<circle cx="{}" cy="{}" r="{}" stroke="red" stroke-width="3" fill="red" />'.
              format(floor(1000*point.coordinates[0]),floor(1000*point.coordinates[1]), 1))



def print_balise(arg = 'ouverture',size=(1000,1000)):
    if arg == "ouverture":
        print('<svg witdh="{}" height="{}">'.format(size[0],size[1]))
    elif arg == 'fermeture':
        print("</svg>")



def print_quadrant(root):
    """marche uniquement en 2D"""
    xmin,ymin = root.min_coordinates
    xmax,ymax = root.max_coordinates
    p1 = Point([xmin,ymin])
    p2 = Point([xmin,ymax])
    p3 = Point([xmax,ymax])
    p4 = Point([xmax,ymin])
    s1 = Segment([p1,p2])
    s2 = Segment([p2,p3])
    s3 = Segment([p3,p4])
    s4 = Segment([p4,p1])
    print_segment([s1,s2,s3,s4])
    if root.childs:
        for child in root.childs:
            print_quadrant(child)

