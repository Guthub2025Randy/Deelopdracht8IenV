# -*- coding: utf-8 -*-
"""
Created on Wed May  7 12:14:40 2025

@author: CWMaz
"""



def reduct_M(Moment,It,lengte_in_cm):
    """in deze functie berekenen en plotten we het gereduceerd moment.
    met als input het moment, het traagheidsmoment en de lengte van het schip
    de output is een plot van het gereduceerde moment"""
    RM=M/(E*I_traag)
    funcPlotFill(lengte_in_cm,RM, "Lengte van het schip (L) in [m]", "Gereduceerde moment (M/(E*I)) in [Nm]", "Het gereduceerde moment", 'Gereduceerde moment', 'black')
    return None


