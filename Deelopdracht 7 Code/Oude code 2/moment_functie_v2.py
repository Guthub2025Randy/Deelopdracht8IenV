# -*- coding: utf-8 -*-
"""
Created on Tue Mar  4 16:18:34 2025

@author: randy
"""
from bibliotheek import np

def moment(positie,kracht):
    """
    deze functie berekent het kruisproduct tussen twee vectoren (in de vorm van arrays) en geeft een array terug die gelijk is 
    aan dit kruisproduct. Als een krachtvector en positievector als arguments worden opgegeven berekent de functie dus het moment.  
    """
    Moment = np.cross(positie, kracht)
    return Moment