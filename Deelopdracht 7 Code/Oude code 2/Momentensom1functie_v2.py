# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 14:01:43 2025

@author: randy
"""

from bibliotheek import *
from moment_functie import moment

def Momentensom1(posities, krachten):
    """
    Deze functie ontvangt twee lijsten aan input. De lijst van posities hoort te bestaan uit arrays met drie elementen: de lcg,
    tcg en vcg van elke massa (in het geval van de opdrijvende kracht het COB). De lijst van krachten bestaat uit floats die gelijk
    zijn aan de grootte van de corresponderende (zwaarte)krachten. Door middel van een for loop en de eerder geschreven momentfunctie
    worden de momenten van alle krachten bij elkaar opgeteld. Vervolgens wordt dit in de vorm van een array die de resultante
    momentvector bevat teruggegeven (dus drie elementen overeenkomend met resp. moment rond de x-as, y-as en z-as.
    """
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
