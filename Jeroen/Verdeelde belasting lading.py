# -*- coding: utf-8 -*-
"""
Created on Mon Mar 31 14:00:31 2025

@author: jeroe
"""

import numpy as np
import matplotlib.pyplot as plt

# Parameters
lading_kg = 230000  # Gewicht per lading in kg
aantal_ladingen = 4  # Aantal ladingen
g = 9.81  # Zwaartekracht in m/s^2
L = 140000 / 10  # Totale lengte van het schip in cm
cg = 41000 / 10  # Zwaartepunt in cm
straal_lading = 4000 / 10  # Standaardafwijking (straal van 400 cm)
n = 1000  # Aantal punten voor nauwkeurigheid

# Bereken de totale neerwaartse kracht per lading in N
F_lading = lading_kg * g
F_totaal = aantal_ladingen * F_lading

# x-coördinaten over de cilinderlengte (0.1 m tot 14000 m, in stappen van cm)
x = np.linspace(1 / 10, L, n)  # cm

# Posities van de 4 ladingen in de lengterichting (centraal op 4100 cm)
lading_posities = [cg] * aantal_ladingen  # Alle ladingen op dezelfde lengtepositie

# Bereken de totale belasting als de som van 4 verdelingen
q = np.zeros_like(x)
for pos in lading_posities:
    q += (F_lading / (straal_lading * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - pos) / straal_lading) ** 2)

# Normaliseer zodat de totale kracht F_totaal blijft
q = q * (F_totaal / np.trapz(q, x))

q = -q

# Combineer in een array
distributed_load = np.column_stack((x, q))

# Plot de verdeelde belasting
plt.figure(figsize=(10, 5))
plt.plot(x / 100, -q, label="verdeelde belasting lading", color="b")  # omzetten naar meters
plt.axvline(cg / 100, color="r", linestyle="--", label="Zwaartepunt lading (41 m)")
plt.xlabel("Lengte langs het schip (m)")
plt.ylabel("Verdeelde belasting  [N/cm]")
plt.title(" verdeelde belasting lading")
plt.legend()
plt.grid(True)
plt.show()

# Print de eerste paar waarden
print(distributed_load[:10])
