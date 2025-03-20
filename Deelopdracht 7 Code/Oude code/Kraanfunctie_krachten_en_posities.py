# -*- coding: utf-8 -*-
"""
Created on Tue Mar  4 18:58:40 2025

@author: randy
"""
from bibliotheek import *

def Kraanfunctie(Krachten, Posities, H, kraan_lcg, SWLMax):
    ZwaarteKheis = -SWLMax
    arrayPositieKheis = np.array([kraan_lcg, 8+(32.5*np.cos(np.deg2rad(60))), (H+1+(32.5*np.sin(np.deg2rad(60))))])
    ZwaarteKboom = -SWLMax*0.17
    arrayPositieKboom = np.array([kraan_lcg, 8+(0.5*32.5*np.cos(np.deg2rad(60))), (H+1+(0.5*32.5*np.sin(np.deg2rad(60))))])
    ZwaarteKhuis = -SWLMax*0.34
    arrayPositieKhuis = np.array([kraan_lcg, 8, H+1])
    ZwaarteWindmolen = -9025200
    arrayPositieWindmolen = np.array([kraan_lcg, -2, H+10])
    Posities.append(arrayPositieKheis)
    Krachten.append(ZwaarteKheis)
    Posities.append(arrayPositieKboom)
    Krachten.append(ZwaarteKboom)
    Posities.append(arrayPositieKhuis)
    Krachten.append(ZwaarteKhuis)
    Posities.append(arrayPositieWindmolen)
    Krachten.append(ZwaarteWindmolen)
    return Krachten, Posities