# -*- coding: utf-8 -*-
"""
Created on Thu Mar  6 17:02:53 2025

@author: randy
"""
from bibliotheek import ip

def traagheidsmomenten_ballasttanks(Dictionary_Traagheidsmoment1, Dictionary_Traagheidsmoment2, Dictionary_Traagheidsmoment3, Dictionary_vulling1, Dictionary_vulling2, Dictionary_vulling3, tankvulling1, tankvulling2, tankvulling3):
    """
    Deze functie neemt als arguments arrays met de traagheidsmomenten op verschillende volumes en arrays met de correspoderende
    volumes van elke aan. Ook neemt hij de werkelijke volumes per tank aan. Vervolgens wordt met interpolatie het werkelijke 
    traagheidsmoment van het wateroppervlak per tank bepaald. Deze worden bij elkaar opgeteld en teruggegeven als float. 
    (de lokale variabelen heten "dictionary" omdat de arrays in dictionaries staan, maar de daadwerkelijk gevraagde inputs zijn 
    arrays)
    """
    TraagheidsmomentT1_dmv_tankfillingper = ip.interp1d(Dictionary_vulling1, Dictionary_Traagheidsmoment1, kind='cubic')
    TraagheidsmomentT2_dmv_tankfillingper = ip.interp1d(Dictionary_vulling2, Dictionary_Traagheidsmoment2, kind='cubic')
    TraagheidsmomentT3_dmv_tankfillingper = ip.interp1d(Dictionary_vulling3, Dictionary_Traagheidsmoment3, kind='cubic')
    Traagheidsmoment1x = TraagheidsmomentT1_dmv_tankfillingper(tankvulling1)
    Traagheidsmoment2x = TraagheidsmomentT2_dmv_tankfillingper(tankvulling2)
    Traagheidsmoment3x = TraagheidsmomentT3_dmv_tankfillingper(tankvulling3)
    SIt = Traagheidsmoment1x + Traagheidsmoment2x + Traagheidsmoment3x
    return SIt