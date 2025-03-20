# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 14:31:46 2025

@author: randy
"""
import numpy as np
from scipy import interpolate as ip
from input_code import *
from openpyxl import load_workbook

g = 9.81
Waterdichtheid = 1025
Staalgewicht = 7850
Transom_BHD_Thickness = 0.01 # m
Rest_Thickness = 0.02 # m
Weight_staal = 2.1*g*Staalgewicht
Weight_water = g*Waterdichtheid
kraan_lcg = 40
Gewicht_transition_piece = 230000
SWLMax = (Gewicht_transition_piece*g)/0.94
H = float(msp["H [m]"])
ZwaarteKheis = -SWLMax
ZwaarteKboom = -SWLMax*0.17
ZwaarteKhuis = -SWLMax*0.34
ZwaarteWindmolen = -Gewicht_transition_piece*g*4
COB = msp["COB [m]"]
Buoyant_volume = float(msp["Buoyant Volume [m3]"])
It = float(msp["Inertia WPA around COF [m4]"][0])
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