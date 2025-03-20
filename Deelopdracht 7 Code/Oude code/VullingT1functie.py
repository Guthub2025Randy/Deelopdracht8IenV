# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 14:15:27 2025

@author: randy
"""
from bibliotheek import g, Waterdichtheid, ip

def Vulling1(Momentensom,TraagheidsmomentT1,TankvolumeT1):
    VullingT1_dmv_Krachtarm_overY = ip.interp1d(TraagheidsmomentT1, TankvolumeT1, kind='cubic')
    TraagheidsmomentTank1 = ((Momentensom[0] / g) / Waterdichtheid)
    vullingt1 = VullingT1_dmv_Krachtarm_overY(TraagheidsmomentTank1)
    return vullingt1
