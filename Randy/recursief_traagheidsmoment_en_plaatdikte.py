# -*- coding: utf-8 -*-
"""
Created on Mon Mar 24 13:52:37 2025

@author: randy
"""
def Error():
    
    return None

# a is nodige sterkte, b is berekende sterkte

def traagheid_en_plaatdikte_schalen(benodigde, t, traagheidsmoment, D, B):
    if traagheidsmoment<=benodigde:
        t += 1 # in mm
        traagheidsmoment = (t*D**2*(D-B))/6
        #doe dingen
        c, d = traagheid_en_plaatdikte_schalen(benodigde, t, traagheidsmoment, D, B)
        return traagheid_en_plaatdikte_schalen(benodigde, t, traagheidsmoment, D, B)
    elif traagheidsmoment>=benodigde:
        return t, traagheidsmoment
    elif Error == True:
        print("Error binnen recursieve functie")
        return None
    
    