# -*- coding: utf-8 -*-
"""
Created on Tue Mar  4 13:40:13 2025

@author: randy
"""

from bibliotheek import *
from input_code import *

def locatie_interpoleren(dictionary_ballasttank, vulling_tank, tanknummer):
    vol_key = f"vol_{tanknummer}"
    lcg_key = f"lcg_{tanknummer}"
    tcg_key = f"tcg_{tanknummer}"
    vcg_key = f"vcg_{tanknummer}"
    TVolume = dictionary_ballasttank[vol_key]
    lcgT = dictionary_ballasttank[lcg_key]
    tcgT = dictionary_ballasttank[tcg_key]
    vcgT = dictionary_ballasttank[vcg_key]
    lcg_interpol = ip.interp1d(TVolume, lcgT, kind='cubic')
    tcg_interpol = ip.interp1d(TVolume, tcgT, kind='cubic')
    vcg_interpol = ip.interp1d(TVolume, vcgT, kind='cubic')
    lcg = lcg_interpol(vulling_tank)
    tcg = tcg_interpol(vulling_tank)
    vcg = vcg_interpol(vulling_tank)
    return np.array([lcg,tcg,vcg])
