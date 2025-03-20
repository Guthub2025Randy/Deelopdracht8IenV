# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 14:01:43 2025

@author: randy
"""

from bibliotheek import *
from moment_functie import moment

def Momentensom1(posities, krachten):
    if len(posities) != len(krachten):
        print("Error, niet gelijke hoeveelheden krachten gekregen voor de eerste momentensom")
        return None
    momentensom = np.array([0.0,0.0,0.0])
    for i in range(len(krachten)):
        positie_1 = posities[i][0]
        positie_2 = posities[i][1]
        positie_3 = posities[i][2]
        momentensom += moment(np.array([positie_1,positie_2,positie_3]), np.array([0, 0, krachten[i]]))
    return momentensom
