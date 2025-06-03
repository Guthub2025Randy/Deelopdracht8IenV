# -*- coding: utf-8 -*-
"""
Created on Mon May 12 13:21:19 2025

@author: randy
"""
from importGrasshopperFiles import *
from bibliotheek import *
import matplotlib.pyplot as plt
from schip_functies import *
from output_code import *

def traagheidsmomentAsymptoot(traag_shell, l_shell, lengte_in_cm, huiddikte):
    # Het traagheidsmoment loopt bij de punt van het schip richting nul. Om een deel door nul fout te voorkomen worden de waardes afgekapt.
    traag1 = traagheidsmomentOverLengte(traag_shell, l_shell, lengte_in_cm)
    asymptootwaarde = 0.01
    for idx, val in enumerate(traag1):
        if idx > (len(traag1) - 100):
            traag1[idx] = traag1[-100] # Anders krijgen we een asymptoot bij M/(E*I)
    return traag1

def sterkteMain(d1, d2, d3, dbh1, dbh2, dbh, msp, dha, dic_shell_csa, dic_csa_tank1, dic_csa_tank2, dic_csa_tank3, cob, h, bouyant_volume, length_schip, it, l_shell, i_x_shell, bouyant_csa, lcg_TP, lengte_cm, straal_tp, rest_thickness, transom_bhd_thickness, kraan_lcg, swlmax, straal_kraanhuis, weight_kraan_totaal, weights_TP, tussenstappen_lengte, hoogte_neutrale_as, hoogte_kiel):
    # Begin deelopdracht 8
    scaling = ((len(lengte_cm)-1)/(lengte_cm[-1] - lengte_cm[0]))
    opwaartse_Kracht = opwaartseKracht(bouyant_csa, lengte_cm)  * scaling
    traag = traagheidsmomentAsymptoot(i_x_shell, l_shell, lengte_cm, 0.012)
    Kracht_Ballast = ballastwaterKracht(dic_csa_tank1, dic_csa_tank2, dic_csa_tank3, lengte_cm, scaling)
    kracht_TP = berekenKrachtVerdeling(lcg_TP, -weights_TP, lengte_cm, straal_tp)
    kracht_kraan = calcParaboolFunctie(kraan_lcg, weight_kraan_totaal, lengte_cm, straal_kraanhuis)
    neerwaartse_kracht_1 = calculateSpiegel(lengte_cm, dha, transom_bhd_thickness)
    neerwaartse_kracht_2 = calculateTrapezium(lengte_cm, dbh, transom_bhd_thickness)
    neerwaartse_kracht_3 = calculateHuid(lengte_cm, 1, dic_shell_csa)
    q = opwaartse_Kracht + Kracht_Ballast + kracht_kraan + kracht_TP + neerwaartse_kracht_2 + neerwaartse_kracht_3 + neerwaartse_kracht_1
    #plotten van q
    dwars_kracht = dwarskracht(q, lengte_cm)
    buigend_moment = buigendMoment(dwars_kracht, lengte_cm)
    reduct_m = reducMoment(buigend_moment, traag)
    #plotten van het gereduceerde moment.
    hoekverdraai_accent = hoekverdraaiingAcc(reduct_m, lengte_cm)
    doorbuig_acc = doorbuigingAcc(hoekverdraai_accent, lengte_cm)
    # hoekverdraaing (phi) = phi_accent + C
    # Doorbuiging (w) = w_acc +C
    # Dus C berekenen:
    c = doorbuig_acc[-1]/length_schip
    hoekverdraai = hoekverdraaiing(hoekverdraai_accent, lengte_cm, c)
    doorbuig = doorbuiging(doorbuig_acc, lengte_cm, c)
    #output_globale_sterkte(Maximaal_moment, LMmilvda, Maximale_afschuiving, LMailvda, Maximale_doorbuiging, LMdilvda)
    centroid_z_in_cm = calcNeutraleAs(lengte_cm, tussenstappen_lengte, hoogte_neutrale_as)
    kiel_z_in_cm = calcKiel(lengte_cm, tussenstappen_lengte, hoogte_kiel)
    vezelafstand_in_cm = calcVezelafstand(centroid_z_in_cm, kiel_z_in_cm)
    spanning = (buigend_moment * vezelafstand_in_cm) / traag
    maximale_spanning = max(spanning)
    return maximale_spanning, q, dwars_kracht, buigend_moment, centroid_z_in_cm, spanning, reduct_m, hoekverdraai_accent, doorbuig_acc, hoekverdraai, doorbuig, traag


