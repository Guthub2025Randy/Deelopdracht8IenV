# -*- coding: utf-8 -*-
"""
Created on Thu Mar  6 16:30:02 2025

@author: randy
"""

def G_M(buoyant_volume, SIt, KG, KB, It):
    gm = KB - KG + It/buoyant_volume
    gnulg = SIt/buoyant_volume
    g_m = gm - gnulg
    return g_m