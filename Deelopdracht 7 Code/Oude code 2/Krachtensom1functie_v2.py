# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 15:28:16 2025

@author: randy
"""

from bibliotheek import np

def Krachtensom1(krachten):
    """
    deze functie maakt van een lijst met krachten een float die gelijk is aan de som van al die krachten en geeft deze terug
    """
    krachtensom = 0
    for i in range(len(krachten)):
        krachtensom += np.sum(np.array([0,0, krachten[i]]), axis=0, keepdims=True)
    return krachtensom