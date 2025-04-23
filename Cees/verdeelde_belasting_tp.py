# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 15:18:03 2025

@author: CWMaz


straal is de straal van een transition piece(TP)
start_cm staat voor het begin van het schip (-900)
eind_cm voor het einde (14100)
lengte =  eind_cm - start_cm + 1

plot staat er nu ook bij, maar die kun je nog aanpassen


"""

import numpy as np
from Library import *

def berekenKrachtVerdeling(lading_posities, massa, straal_cm, start_cm, eind_cm):
    lengte = eind_cm - start_cm + 1
    krachtverdeling = np.zeros(lengte)
    kracht = massa * GRAVITATIONAL_CONSTANT

    for pos in lading_posities:
        krachtverdeling += parabolischProfiel(pos, kracht, straal_cm, start_cm, eind_cm, lengte)

    return np.arange(start_cm, eind_cm + 1), krachtverdeling

def parabolischProfielTP(zwaartepunt_tp, totaal_kracht, straal, start, eind, lengte):
    begin = max(zwaartepunt_tp - straal, start)
    eind = min(zwaartepunt_tp + straal, eind)
    idx_begin = int(begin - start)
    idx_eind = int(eind - start)

    bereik = np.arange(idx_begin, idx_eind + 1)
    afstanden = (bereik + start) - zwaartepunt_tp
    x_norm = afstanden / straal

    profiel = np.clip(1 - x_norm**2, 0, None)
    profiel /= profiel.sum()
    profiel *= totaal_kracht

    kracht = np.zeros(lengte)
    kracht[bereik] = profiel
    return kracht

import matplotlib.pyplot as plt

def plot_krachtverdeling(x, krachtverdeling, titel="Krachtverdeling over schip"):
    plt.figure(figsize=(14, 4))
    plt.plot(x, krachtverdeling, color='darkgreen')
    plt.xlabel("Positie op schip (cm)")
    plt.ylabel("Neerwaartse kracht per cm (N)")
    plt.title(titel)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

