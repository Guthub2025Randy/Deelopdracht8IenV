# -*- coding: utf-8 -*-
"""
Created on Tue Mar  4 16:18:34 2025

@author: randy
"""
from bibliotheek import np

def moment(positie,kracht):
    Moment = np.cross(positie, kracht)
    return Moment