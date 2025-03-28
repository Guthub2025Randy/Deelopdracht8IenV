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

def traagheid_en_plaatdikte_schalen(benodigde, t, traagheidsmoment, D, B):
    plaatdiktes = [0.001]
    traagheidsmomenten = [traagheidsmoment]
    if traagheidsmoment<=benodigde:
        t += 0.001 # in m
        plaatdiktes.append(t)
        traagheidsmoment2 = (t*D**2*(D-B))/6
        traagheidsmomenten.append(traagheidsmoment2)
        c, d = traagheid_en_plaatdikte_schalen(benodigde, t, traagheidsmoment2, D, B)
    elif traagheidsmoment>=benodigde:
        return t, traagheidsmoment
    elif Error == True:
        print("Error binnen recursieve functie")
        return None
    plt.figure(figsize=(8,5))
    plt.plot(traagheidsmomenten, plaatdiktes, color='b', label='Traagheidsmomenten')
    plt.xlabel("Traagheidsmomenten (T) in [m4]")
    plt.ylabel("Plaatdiktes (t) in [m]")
    plt.title("Traagheidsmomenten als functie van de plaatdiktes")
    plt.legend()
    plt.grid(True)
    return traagheid_en_plaatdikte_schalen(benodigde, c, d, D, B)

tplaat = 0.001
benodigde1 = 100
Dikte = 10
Breedte = 6 
traagheidsmoment1 = (tplaat*Dikte**2*(Dikte-Breedte))/6

traagheid_en_plaatdikte_schalen(benodigde1, tplaat, traagheidsmoment1, Dikte, Breedte)