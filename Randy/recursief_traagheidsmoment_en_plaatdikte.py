# -*- coding: utf-8 -*-
"""
Created on Mon Mar 24 13:52:37 2025

@author: randy
"""
def Error():
    
    return None
import numpy as np
import matplotlib.pyplot as plt
# a is nodige sterkte, b is berekende sterkte

def traagheid_en_plaatdikte_schalen(benodigde, t, traagheidsmoment, D, B, plaatdikteses, traagheidsmomentenen):
    if traagheidsmoment<=benodigde:
        t += 0.001 # in m
        plaatdikteses.append(t)
        traagheidsmoment2 = (t*D**2*(D-B))/6
        traagheidsmomentenen.append(traagheidsmoment2)
        return traagheid_en_plaatdikte_schalen(benodigde, t, traagheidsmoment2, D, B, plaatdikteses, traagheidsmomentenen)
    elif traagheidsmoment>=benodigde:
        plt.figure(figsize=(8,5))
        return t, traagheidsmoment, plaatdikteses, traagheidsmomentenen
    elif Error == True:
        print("Error binnen recursieve functie")
        return None

tplaat = 0.001
benodigde1 = 100
Dikte = 10
Breedte = 6 
traagheidsmoment1 = (tplaat*Dikte**2*(Dikte-Breedte))/6
Lengte_schip = np.linspace(-9, 140, 14000)
Dikte_op_lengte = np.array(dingen)
plaatdiktes = [0.001]
traagheidsmomenten = [traagheidsmoment1]

treal, Traagheidsreal, plaatdiktesreal, traagheidsmomentenreal = traagheid_en_plaatdikte_schalen(benodigde1, tplaat, traagheidsmoment1, Dikte, Breedte, plaatdiktes, traagheidsmomenten)

plt.plot(traagheidsmomentenreal, plaatdiktesreal, color='b', label='Traagheidsmomenten')
plt.xlabel("Traagheidsmomenten (T) in [m4]")
plt.ylabel("Plaatdiktes (t) in [m]")
plt.title("Traagheidsmomenten als functie van de plaatdiktes")
plt.legend()
plt.grid(True)

for i in range(len(Lenge_schip)):    