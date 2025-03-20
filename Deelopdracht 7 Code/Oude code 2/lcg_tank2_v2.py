# -*- coding: utf-8 -*-
"""
Created on Tue Mar  4 14:53:05 2025

@author: randy
"""

from bibliotheek import np

def lcg_tank2(momentensom2,krachtensom2):
    """
    deze functie haalt uit het het resultante moment rond de y-as en de resultante kracht de arm van tank 2. De resultante kracht
    in dit geval is het totale gewicht van tank 2 (dus water+tankschotten), berekend door alle andere gewichten bij elkaar op te 
    tellen en daar de opdrijvende kracht van af te trekken. 
    """
    lcgt2 = momentensom2[1]/-krachtensom2
    return lcgt2