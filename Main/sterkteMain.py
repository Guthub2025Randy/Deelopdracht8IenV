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
    traag1 = traagheidsmomentOverLengte(traag_shell, l_shell, lengte_in_cm)*huiddikte
    asymptootwaarde = 0.01
    for idx, val in enumerate(traag1):
        if idx > (len(traag1) - 100):
            traag1[idx] = traag1[-100] # Anders krijgen we een asymptoot bij M/(E*I)
    funcPlotFill(lengte_in_cm, traag1, "Lengte van het schip (L) [m]", "Traagheidsmoment I [m4]", "Het traagheidsmoment I [m4] over de lengte van het schip L [m]", "Traagheidsmoment I [m4]", 'purple')
    return traag1

def sterkteMain(d1, d2, d3, dbh1, dbh2, dbh, msp, dha, dic_shell_csa, dic_csa_tank1, dic_csa_tank2, dic_csa_tank3, cob, h, bouyant_volume, length_schip, it, l_shell, i_x_shell, bouyant_csa, lcg_TP, lengte_cm, straal_tp, rest_thickness, transom_bhd_thickness, kraan_lcg, swlmax, straal_kraanhuis, weight_kraan_totaal, weights_TP):
    # Begin deelopdracht 8
    scaling = ((len(lengte_cm)-1)/(lengte_cm[-1] - lengte_cm[0]))
    opwaartse_Kracht = opwaartseKracht(bouyant_csa, lengte_cm)  * scaling
    I_traag = traagheidsmomentAsymptoot(i_x_shell, l_shell, lengte_cm, 0.012)
    Kracht_Ballast = ballastwaterKracht(dic_csa_tank1, dic_csa_tank2, dic_csa_tank3, lengte_cm, scaling)
    kracht_TP = berekenKrachtVerdeling(lcg_TP, -weights_TP, lengte_cm, straal_tp)
    funcPlotFill(lengte_cm, kracht_TP, "lengte", "gezeik", "transitionpieces", "meer gezeik", "black")
    kracht_kraan = calcParaboolFunctie(kraan_lcg, weight_kraan_totaal, lengte_cm, straal_kraanhuis)
    funcPlotFill(lengte_cm, kracht_kraan, "lengte", "gezeik", "kraan", "meer gezeik", "black")
    neerwaartse_kracht_1 = calculateSpiegel(lengte_cm, dha, transom_bhd_thickness)
    funcPlotFill(lengte_cm, neerwaartse_kracht_1, "lengte", "gezeik", "spiegel", "meer gezeik", "black")
    neerwaartse_kracht_2 = calculateTrapezium(lengte_cm, dbh, transom_bhd_thickness)
    funcPlotFill(lengte_cm, neerwaartse_kracht_2, "lengte", "gezeik", "bulkheads", "meer gezeik", "black")
    neerwaartse_kracht_3 = calculateHuid(lengte_cm, 1, dic_shell_csa)
    funcPlotFill(lengte_cm, neerwaartse_kracht_3, "lengte", "gezeik", "huid", "meer gezeik", "black")
    q = opwaartse_Kracht + Kracht_Ballast + kracht_kraan + kracht_TP + neerwaartse_kracht_2 + neerwaartse_kracht_3 + neerwaartse_kracht_1
    #plotten van q
    funcPlotFill(lengte_cm, -q, "Lengte van het schip (L) in [m]", "Netto verdeelde belasting (q) in [N]", "De netto verdeelde belasting", 'Netto load',"black")
    V = dwarskracht(q, lengte_cm)
    M = buigendMoment(V, lengte_cm)
    Reduct_M = reducMoment(M, I_traag)
    #plotten van het gereduceerde moment.
    funcPlotFill(lengte_cm,Reduct_M, "Lengte van het schip (L) in [m]", "Gereduceerde moment (M/(E*I)) in [Nm]", "Het gereduceerde moment", 'Gereduceerde moment', 'black')
    hoekverdraai_accent = hoekverdraaiingAcc(Reduct_M, lengte_cm)
    doorbuig_acc = doorbuigingAcc(hoekverdraai_accent, lengte_cm)
    # hoekverdraaing (phi) = phi_accent + C
    # Doorbuiging (w) = w_acc +C
    # Dus C berekenen:
    C = doorbuig_acc[-1]/length_schip
    hoekverdraai = hoekverdraaiing(hoekverdraai_accent, lengte_cm, C)
    doorbuig = doorbuiging(doorbuig_acc, lengte_cm, C)
    #output_globale_sterkte(Maximaal_moment, LMmilvda, Maximale_afschuiving, LMailvda, Maximale_doorbuiging, LMdilvda)
    maximale_spanning = 10
    return maximale_spanning

