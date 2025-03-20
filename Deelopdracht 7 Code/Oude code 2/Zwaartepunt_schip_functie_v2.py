# -*- coding: utf-8 -*-
"""
Created on Thu Mar  6 16:34:21 2025

@author: randy
"""

def Zwaartepuntschip(posities, krachten):
    """
    Deze functie berekent het totale zwaartepunt van het schip op basis van lijsten met de zwaartekrachten en zwaartepunten van 
    elk onderdeel van het schip. De individuele zwaartekrachten en producten van zwaartekrachten met hun locatie worden in een for-
    loop bij elkaar opgeteld. Vervolgens wordt elk van de  gedeeld door de totale zwaartekracht gedeeld om het lcg, tcg, en
    vcg te bepalen. Als output geeft de functie een tuple van drie floats. 
    """
    krachtenopgeteld = 0
    lcg_krachten_en_posities_vermenigvuldigd = 0
    tcg_krachten_en_posities_vermenigvuldigd = 0
    vcg_krachten_en_posities_vermenigvuldigd = 0
    for i in range(len(krachten)):
        if len(krachten) != len(posities):
            print("Error, ongelijke hoeveelheden krachten en posities")
            return None
        else:
            x = posities[i][0]
            y = posities[i][1]
            z = posities[i][2]
            krachtenopgeteld += krachten[i]
            lcg_krachten_en_posities_vermenigvuldigd += x*krachten[i]
            tcg_krachten_en_posities_vermenigvuldigd += y*krachten[i]
            vcg_krachten_en_posities_vermenigvuldigd += z*krachten[i]
    lcg = lcg_krachten_en_posities_vermenigvuldigd/krachtenopgeteld
    tcg = tcg_krachten_en_posities_vermenigvuldigd/krachtenopgeteld
    vcg = vcg_krachten_en_posities_vermenigvuldigd/krachtenopgeteld
    return lcg, tcg, vcg