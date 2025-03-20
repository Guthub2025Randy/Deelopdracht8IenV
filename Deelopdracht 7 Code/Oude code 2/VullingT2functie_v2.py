# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 14:50:39 2025

@author: randy
"""

from bibliotheek import g, Waterdichtheid, ip

def VullingT2(Krachtensom):
    """
    Deze functie genereert uit de resultante kracht het volume van het water in tank twee en geeft deze terug. Beide deze 
    variabelen zijn floats.
    """
    Volume_T2 = (Krachtensom / g) / Waterdichtheid
    return Volume_T2