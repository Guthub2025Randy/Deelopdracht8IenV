# -*- coding: utf-8 -*-
"""
Created on Fri Mar  7 09:12:24 2025

@author: CWMaz
"""
from bibliotheek import *
from input_code import *


def opdrijvende_kracht(gewicht_water, onderwater_volume):
    """
    deze functie berekent de opdrijvende kracht op basis van het onderwatervolume en de dichtheid van water. 
    """
    opdrijvende_kracht = gewicht_water * onderwater_volume
    return opdrijvende_kracht

