# -*- coding: utf-8 -*-
"""
Created on Thu Mar  6 16:30:02 2025

@author: randy
"""

def G_M(buoyant_volume, SIt, KG, KB, It):
    """
    Deze functie bepaalt het G'M op basis van de inputs onderwatervolume, de som van de traagheidsmomenten van de wateroppervlakten 
    van de ballastanks, KG, KB en het traagheidsmoment van de waterlijn. Eerst wordt de GM bepaald, vervolgens wordt de 
    vrijevloeistofcorrectie toegepast. Bij de vrijevloeistofcorrectie is ervan uitgegaan dat de dichtheid van de water in de 
    ballasttanks gelijk zijn aan het water verplaatst door de romp. Alle inputs horen floats te zijn, net als return g'm.
    """
    gm = KB - KG + It/buoyant_volume
    gnulg = SIt/buoyant_volume
    g_m = gm - gnulg
    return g_m