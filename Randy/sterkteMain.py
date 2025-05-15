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

versienummer = 1

d1, d2, d3, dbh1, dbh2, dbh, msp, dha, dic_Shell_CSA, dic_csa_tank1, dic_csa_tank2, dic_csa_tank3, resistance, B_CSA2 = importGrasshopperFiles(versienummer)
cob = msp["COB [m]"]
h = float(msp["H [m]"])
bouyant_volume = float(msp["Buoyant Volume [m3]"])
length_schip = float(msp["Loa  [m]"])
it = float(msp["Inertia WPA around COF [m4]"][0])
l_shell = dic_Shell_CSA["X [m]"]
i_x_shell = dic_Shell_CSA["INERTIA_X[m4]"]
lcg_TP = np.array([32,32,28,36])
weights_TP = np.array([WEIGHT_TRANSITION_PIECE, WEIGHT_TRANSITION_PIECE, WEIGHT_TRANSITION_PIECE, WEIGHT_TRANSITION_PIECE])
lengte_cm = np.linspace(-9, 141, 15001)
transom_bhd_thickness = 0.01 # m
rest_thickness = 0.012 # m
kraan_lcg = 10
straal_kraanhuis = 2

def traagheidsmomentAsymptoot(traag_shell, l_shell, lengte_in_cm):
    traag1 = traagheidsmomentOverLengte(traag_shell, l_shell, lengte_in_cm)
    asymptootwaarde = 0.01
    for idx, val in enumerate(traag1):
        if val < 0.01:
            traag1[idx] = asymptootwaarde # Anders krijgen we een asymptoot bij M/(E*I)
    return traag1

def sterkteMain(d1, d2, d3, dbh1, dbh2, dbh, msp, dha, dic_Shell_CSA, dic_csa_tank1, dic_csa_tank2, dic_csa_tank3, cob, h, bouyant_volume, length_schip, it, l_shell, i_x_shell, B_CSA2, lcg_TP, lengte_cm, STRAAL_TP, rest_thickness, transom_bhd_thickness, kraan_lcg, swlmax, straal_kraanhuis, WEIGHT_KRAAN_TOTAAL, weights_TP):
    # Begin deelopdracht 8
    opwaartse_Kracht = opwaartseKracht(B_CSA2, lengte_cm)  * ((len(lengte_cm)-1)/(lengte_cm[-1] - lengte_cm[0]))
    I_traag = traagheidsmomentAsymptoot(i_x_shell, l_shell, lengte_cm)
    Kracht_Ballast = ballastwaterKracht(dic_csa_tank1, dic_csa_tank2, dic_csa_tank3, lengte_cm) * ((len(lengte_cm)-1)/(lengte_cm[-1] - lengte_cm[0]))
    kracht_TP = berekenKrachtVerdeling(lcg_TP, -weights_TP * ((len(lengte_cm)-1)/(lengte_cm[-1] - lengte_cm[0])), lengte_cm, STRAAL_TP)
    funcPlotFill(lengte_cm, kracht_TP, "lengte", "gezeik", "transitionpieces", "meer gezeik", "black")
    kracht_kraan = parabolischProfielKraan(kraan_lcg, WEIGHT_KRAAN_TOTAAL * ((len(lengte_cm)-1)/(lengte_cm[-1] - lengte_cm[0])), lengte_cm, straal_kraanhuis)
    funcPlotFill(lengte_cm, kracht_kraan, "lengte", "gezeik", "kraan", "meer gezeik", "black")
    neerwaartse_kracht_1 = calculateSpiegel(lengte_cm, dha, transom_bhd_thickness) *10
    funcPlotFill(lengte_cm, neerwaartse_kracht_1, "lengte", "gezeik", "spiegel", "meer gezeik", "black")
    neerwaartse_kracht_2 = calculateTrapezium(lengte_cm, dbh, transom_bhd_thickness)
    funcPlotFill(lengte_cm, neerwaartse_kracht_2, "lengte", "gezeik", "bulkheads", "meer gezeik", "black")
    neerwaartse_kracht_3 = calculateHuid(lengte_cm, rest_thickness, dic_Shell_CSA) * (((len(lengte_cm)-1)/(lengte_cm[-1] - lengte_cm[0])))
    funcPlotFill(lengte_cm, neerwaartse_kracht_3, "lengte", "gezeik", "huid", "meer gezeik", "black")
    q = opwaartse_Kracht + Kracht_Ballast + kracht_kraan + kracht_TP + neerwaartse_kracht_2 + neerwaartse_kracht_3 + neerwaartse_kracht_1
    #plotten van q
    funcPlotFill(lengte_cm, -q, "Lengte van het schip (L) in [m]", "Netto verdeelde belasting (q) in [N]", "De netto verdeelde belasting", 'Netto load',"black")
    V = dwarskracht(q, lengte_cm)
    M = buigendMoment(V, lengte_cm)
    Reduct_M = M/(E*I_traag)
    #plotten van het gereduceerde moment.
    funcPlotFill(lengte_cm,Reduct_M, "Lengte van het schip (L) in [m]", "Gereduceerde moment (M/(E*I)) in [Nm]", "Het gereduceerde moment", 'Gereduceerde moment', 'black')
    hoekverdraai_accent = hoekverdraaiingAcc(M, lengte_cm)
    doorbuig_acc = doorbuigingAcc(hoekverdraai_accent, lengte_cm)
    # hoekverdraaing (phi) = phi_accent + C
    # Doorbuiging (w) = w_acc +C
    # Dus C berekenen:
    C = doorbuig_acc[-1]/length_schip
    hoekverdraai = hoekverdraaiing(hoekverdraai_accent, lengte_cm, C)
    doorbuig = doorbuiging(hoekverdraai, lengte_cm)
    #output_globale_sterkte(Maximaal_moment, LMmilvda, Maximale_afschuiving, LMailvda, Maximale_doorbuiging, LMdilvda)
    return

sterkteMain(d1, d2, d3, dbh1, dbh2, dbh, msp, dha, dic_Shell_CSA, dic_csa_tank1, dic_csa_tank2, dic_csa_tank3, cob, h, bouyant_volume, length_schip, it, l_shell, i_x_shell, B_CSA2, lcg_TP, lengte_cm, STRAAL_TP, rest_thickness, transom_bhd_thickness, kraan_lcg, swlmax, straal_kraanhuis, WEIGHT_KRAAN_TOTAAL, weights_TP)