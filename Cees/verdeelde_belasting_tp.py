# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 15:18:03 2025

@author: CWMaz




"""

import numpy as np
from Library import *
import matplotlib.pyplot as plt



def parabolischProfielTP(zwaartepunt_tp, totaal_kracht, lengte_in_cm):
    """de input van deze functie is het zwaartepunt van één Transition Piece, de totale kracht van alle transition pieces
    en een array over de lengte van het schip die te vinden is in de main. dan maakt hij eerst het bereik waar het parabolisch profiel van de TP's
    te vinden is. dan maakt hij van de fysieke positie een index in een array. in het 2de deel van de functie bereidt hij parabool waarden voor.
    x_norm zijn dan de genormaliseerde afstanden tov het zwaartepunt. in het laatste deel maakt hij het parabolisch profiel en alle negatieve waardes op 0. 
    en dan zorgt hij ervoor dat de som gelijk is aan de totale kracht."""
    start = lengte_in_cm[0]
    eind = lengte_in_cm[-1]
    begin = max(zwaartepunt_tp - straal_tp, start)
    eind = min(zwaartepunt_tp + straal_tp, eind)
    idx_begin = int(begin - start)
    idx_eind = int(eind - start)

    bereik = np.arange(idx_begin, idx_eind + 1)
    afstanden = (bereik + start) - zwaartepunt_tp
    x_norm = afstanden / straal_tp

    profiel = np.clip(1 - x_norm**2, 0, None)
    profiel /= profiel.sum()
    profiel *= totaal_kracht
    kracht = np.zeros(lengte_in_cm)
    kracht[bereik] = profiel
    return kracht

def berekenKrachtVerdeling(lading_posities, massa, lengte_in_cm):
    """hier maakt hij eerst een krachten verdeling van 0 over de lengte. dan maakt hij van de massa van de TPs het gewicht van de TPs.
    doormiddel van de functie parabolischProfielTP voegt hij deze kracht verdeling toe op de eerst  zero-array over de lengte."""
    krachtverdeling = np.zeros(lengte_in_cm)
    kracht = massa * GRAVITATIONAL_CONSTANT
    for pos in lading_posities:
        krachtverdeling += parabolischProfielTP(pos, kracht, lengte_in_cm)

    return np.arange(start_cm, eind_cm + 1), krachtverdeling

# deze functie moeten nog geplot worden. met lengte op de x-as en krachtverdeling op de y-as. met als title: "Krachtverdeling over het Schip"




