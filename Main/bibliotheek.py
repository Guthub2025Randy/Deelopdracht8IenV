# -*- coding: utf-8 -*-
"""
Created on Tue Mar 18 12:33:18 2025

@author: randy
"""

# De bibliotheek met alle globale variabelen die doorgestuurt kunnen worden als lokale variabelen

import numpy as np
from scipy.integrate import simpson as sm
from scipy import interpolate as ip
from openpyxl import load_workbook
import matplotlib.pyplot as plt

g = 9.81
WATERDICHTHEID = 1025
STAALGEWICHT = 7850
transom_bhd_thickness = 0.01 # m
rest_thickness = 0.02 # m
WEIGHT_STAAL = 2.1*g*STAALGEWICHT
WEIGHT_WATER = g*WATERDICHTHEID
kraan_lcg = 40
gewicht_transition_piece = 230000
swlmax = (gewicht_transition_piece*g)/0.94
H = float(msp["H [m]"])
zwaarteKheis = -swlmax
zwaarteKboom = -swlmax*0.17
zwaarteKhuis = -swlmax*0.34
zwaarteWindmolen = -gewicht_transition_piece*g*4
COB = msp["COB [m]"]
buoyant_volume = float(msp["Buoyant Volume [m3]"])
it = float(msp["Inertia WPA around COF [m4]"][0])
lcg_tp = kraan_lcg
tcg_tp = -2
vcg_tp = H+10
lengte_kraan_fundatie = 1
Draaihoogte_kraan = 1
jib_length = 32.5
Zwenkhoek = 90
Giekhoek = 60
LCG_TP = kraan_lcg
TCG_TP = 8+(32.5*np.cos(np.deg2rad(60)))
VCG_TP = (H+1+(32.5*np.sin(np.deg2rad(60))))
LCG_kraanhuis = kraan_lcg 
TCG_kraanhuis = 8
VCG_kraanhuis = H+1
LCG_kraanboom = kraan_lcg
TCG_kraanboom = 8+(0.5*32.5*np.cos(np.deg2rad(60)))
VCG_kraanboom = (H+1+(0.5*32.5*np.sin(np.deg2rad(60))))
LCG_heisgerei = kraan_lcg
TCG_heisgerei = 8+(32.5*np.cos(np.deg2rad(60)))
VCG_heisgerei = (H+1+(32.5*np.sin(np.deg2rad(60))))
