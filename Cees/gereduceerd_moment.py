# -*- coding: utf-8 -*-
"""
Created on Wed May  7 12:14:40 2025

@author: CWMaz
"""



def reduct_M(M,I_traag,lengte_in_cm):
    RM=M/(E*I_traag)
    funcPlotFill(lengte_in_cm,RM, "Lengte van het schip (L) in [m]", "Gereduceerde moment (M/(E*I)) in [Nm]", "Het gereduceerde moment", 'Gereduceerde moment', 'black')
    return None


