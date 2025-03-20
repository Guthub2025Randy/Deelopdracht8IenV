# -*- coding: utf-8 -*-
"""
Created on Fri Mar  7 10:39:13 2025

@author: jeroe
"""

import numpy as np
import matplotlib.pyplot as plt
from G_M_Functie import G_M
from Main_Deelopdracht_7 import posities2, krachten2, SIt
from Zwaartepunt_schip_functie import Zwaartepuntschip

# Gegevens uit het bestand
buoyant_volume = 8639.1405  # [m³] (uit "Buoyant Volume [m3]")
KG = Zwaartepuntschip(posities2, krachten2)  # [m] (uit "COV Total [m]")
KB = 3.4009  # [m] (uit "COB [m]")

# Traagheidsmomenten voor Tank 3 uit de dataset
I3_values = np.array([2.7282,306.9701,639.027,1092.8359,1474.8797,1700.9905,1807.573])

# Interpolatie om 10 punten te verkrijgen voor de vullingsgraden
I3_interpolated = np.interp(np.linspace(0, 6, 10), np.linspace(0, 6, len(I3_values)), I3_values)
def gnulg(onderwater_volume, SIt):
    ##SIt = Traagheidsmoment1 + Traagheidsmoment2 + Traagheidsmoment3
    return SIt/onderwater_volume

# Functie om GM te berekenen
def bereken_GM(onderwater_volume, KG, KB, gnulg):
    return KB - KG + 78660.9109 / onderwater_volume - gnulg(buoyant_volume, SIt)

# Vullingsgraden tussen 1437.448 en 1658.448 (10 waarden)
vullingsgraden = np.linspace(1437.448, 1658.448, 10)

# GM-waarden berekenen voor elke vullingsgraad met werkelijke It van Tank 3
GM_values = [bereken_GM(buoyant_volume, KG, KB, gnulg) for It in I3_interpolated]


# Grafiek plotten
plt.figure(figsize=(8,5))
plt.plot(vullingsgraden, GM_values, marker='o', linestyle='-', color='b', label='GM vs. vulling (Tank 3)')

# Labels en titel
plt.xlabel("Vullingsgraad (m³)")
plt.ylabel("Metacentrumhoogte (GM) [m]")
plt.title("Effect van ballasttankvulling (Tank 3) op GM")
plt.legend()
plt.grid(True)

# Grafiek tonen
plt.show()
