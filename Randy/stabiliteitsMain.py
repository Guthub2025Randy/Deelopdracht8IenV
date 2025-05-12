# -*- coding: utf-8 -*-
"""
Created on Wed May  7 11:11:28 2025

@author: randy
"""
# De main herschrijven haha, hier is het deel wat bij deelopdracht 7 hoort
from importGrasshopperFiles import *
from bibliotheek import *
import matplotlib.pyplot as plt
from schip_functies import *
from output_code import *

versienummer = 8

d1, d2, d3, dbh1, dbh2, dbh, msp, dha, dic_Shell_CSA, dic_csa_tank1, dic_csa_tank2, dic_csa_tank3 = importGrasshopperFiles(versienummer)
cob = msp["COB [m]"]
h = float(msp["H [m]"])
bouyant_volume = float(msp["Buoyant Volume [m3]"])
length_schip = float(msp["Loa  [m]"])
it = float(msp["Inertia WPA around COF [m4]"][0])
l_shell = dic_Shell_CSA["X [m]"]
i_x_shell = dic_Shell_CSA["INERTIA_X[m4]"]
B_CSA2 = dic_csa(df_csa)

def eersteMoment(d3, bouyant_volume, transom_bhd_thickness, dha, rest_thickness, kraan_lcg, cob):
    #Tank 3: er wordt een waarde gekozen voor het volume van tank 3. Vervolgens wordt hiervan het gewicht en
    #het zwaartepunt bepaald
    volume_t3 = d3["vol_3"][4]+643
    kracht_t3 = volume_t3*WEIGHT_WATER
    locatie_t3 = interpolerenLocatie(d3, volume_t3, 3)
    #Tank 1: om de vulling van tank 1 te bepalen worden alle momenten bij elkaar opgeteld. Eerst worden er lijsten
    #met de gewichten en aangrijpingspunten van de zwaartekrachten van alle massa's opgesteld met behulp van de
    #functie "positiesmetkrachtenlijst2". Vervolgens worden alle momenten bij elkaar opgeteld met de functie
    #"momentensom1". Voor meer informatie over deze functies, zie de docstrings in de functiebestanden.
    krachten, posities = positiesmetkrachtenlijst1(dbh1, locatie_t3, kracht_t3, h, cob, WEIGHT_STAAL,
                                                   transom_bhd_thickness, kraan_lcg, swlmax, dha, rest_thickness,
                                                   calculateOpdrijvendeKracht(WEIGHT_WATER, bouyant_volume))
    eerste_moment = calculateMomentensom(posities, krachten)
    return eerste_moment, kracht_t3, locatie_t3, volume_t3

def tankEen(dictio_1, momentensom):
    volu_t1 = calculateVullingT1(dictio_1['vol_1'], dictio_1['tcg_1'], momentensom, dictio_1['vulling_%_1'][:7],
                                   WEIGHT_WATER)
    kr_t1 = volu_t1*WEIGHT_WATER
    loca_t1 = interpolerenLocatie(dictio_1, volu_t1, 1)
    return volu_t1, kr_t1, loca_t1

def vullingPercFunc(dictio_1, dictio_2, dictio_3, momentensom, volu_2, volu_3):
    momentdic = dictio_1['vol_1'] * dictio_1['tcg_1'] * WEIGHT_WATER
    vulperc1dic = dictio_1['vulling_%_1'][:7]
    vulperc1ip = ip.interp1d(momentdic,vulperc1dic, kind = "cubic")
    vulperc1 = vulperc1ip(momentensom[0])
    print("De vulling [%] van tank 1 moet zijn:")
    print(vulperc1)
    vulperc2ip = ip.interp1d(dictio_2['vol_2'], dictio_2['vulling_%_2'][:7], kind = "cubic")
    vulperc2 = vulperc2ip(volu_2)
    print("De vulling [%] van tank 2 moet zijn:")
    print(vulperc2)
    vulperc3ip = ip.interp1d(dictio_3['vol_3'], dictio_3['vulling_%_3'][:7], kind = "cubic")
    vulperc3 = vulperc3ip(volu_3)
    print("De vulling [%] van tank 3 moet zijn:")
    print(vulperc3)
    return vulperc1, vulperc2, vulperc3

def tankTwee(krachten2, dbh1, locatie_t1, kracht_t1, locatie_t3, kracht_t3, h, cob, transom_bhd_thickness, kraan_lcg, swlmax, dha, rest_thickness, bouyant_volume, dbh2, d2):
    krachtensom = calculateKrachtensom1(krachten2)
    volume_t2 = calculateVullingT2(krachtensom, WEIGHT_WATER)[0]
    kracht_t2 = volume_t2*WEIGHT_WATER
    #Tank 2: voor het longitudinale evenwicht is er een nieuwe momentensom nodig, waar wel de vulling van tank 1
    #is inbegrepen maar niet de tankschotten van tank 2. De functie momentensom2 voegt de momenten veroorzaakt
    #door de vulling van tank 1 toe aan de eerdere momentensom. Vervolgens wordt de ligging van het zwaartepunt
    #van tank 2 bepaald.
    krachten_bh1, posities_bh1 = positiesmetkrachtenlijst2(dbh1, locatie_t1, kracht_t1, locatie_t3, kracht_t3, h, cob,
                                                     WEIGHT_STAAL, transom_bhd_thickness, kraan_lcg, swlmax, dha,
                                                     rest_thickness, calculateOpdrijvendeKracht(WEIGHT_WATER, bouyant_volume))
    TweedeMomentensom = calculateMomentensom(posities_bh1, krachten_bh1)
    TweedeKrachtensom = calculateKrachtsom2(krachtensom, dbh2, transom_bhd_thickness, WEIGHT_STAAL)
    vcgt2 = interpolerenLocatie(d2, volume_t2, 2)[2]
    positie_t2 = np.array([lcgTank2(TweedeMomentensom,TweedeKrachtensom)[0], 0, vcgt2])
    return volume_t2, kracht_t2, positie_t2

def stabilitietsMain(versienummer, transom_bhd_thickness, rest_thickness, kraan_lcg, d1, d2, d3, dbh1, dbh2, dbh, msp, dha, dic_Shell_CSA, dic_csa_tank1, dic_csa_tank2, dic_csa_tank3, cob, h, bouyant_volume):
    # De eerste momentensom voor het dwarsscheepse momentenevenwicht
    momentensom1_, kracht_t3, locatie_t3, volume_t3 = eersteMoment(d3, bouyant_volume, transom_bhd_thickness, dha, 
                                                                   rest_thickness, kraan_lcg, cob)
    #Tank 1: op basis van het berekende transversale moment wordt de vulling en gewicht van de vulling van het water
    #in tank 1 bepaald.
    volume_t1, kracht_t1, locatie_t1 = tankEen(d1, momentensom1_)
    #Tank 2: om het nieuwe krachtevenwicht en het longitudinale momentevenwicht te bepalen moeten
    #het gewicht en zwaartepunt van het water in tank 1 worden toegevoegd aan de lijsten met krachten en posities.
    #Dit wordt gedaan met de functie "positiemetkrachtenlijst1". Op basis van deze lijsten wordt de vulling en
    #het gewicht van tank 2 bepaald.
    krachten2, posities2 = positiesmetkrachtenlijst2(dbh, locatie_t1, kracht_t1, locatie_t3, kracht_t3, h, cob,
                                                     WEIGHT_STAAL, transom_bhd_thickness, kraan_lcg, swlmax, dha,
                                                     rest_thickness, calculateOpdrijvendeKracht(WEIGHT_WATER, bouyant_volume))
    volume_t2, kracht_t2, positie_t2 = tankTwee(krachten2, dbh1, locatie_t1, kracht_t1, locatie_t3, kracht_t3, h, cob, transom_bhd_thickness, 
                                                kraan_lcg, swlmax, dha, rest_thickness, bouyant_volume, dbh2, d2)
    #Stabiliteit: met de functie "traagheidsmomenten_ballasttanks" wordt de som van de traagheidsmomenten van de
    #vrije vloeistofoppervlakten van de tanks berekend. Voor meer informatie over deze functie, zie de docstring
    #in het functiebestand.
    SIt = calculateIttanks(d1["inertia_1"], d2["inertia_2"], d3["inertia_3"], d1["vol_1"],
                                          d2["vol_2"], d3["vol_3"], volume_t1, volume_t2, volume_t3)
    #Stabiliteit: om de totale zwaartepunten van het schip te berekenen, moeten het gewicht en zwaartepunt van het water in
    #tank 2 worden toegevoegd aan de lijsten met krachten en posities en de opdrijvende kracht en het
    #aangrijpingspunt daarvan juist verwijderd. Vervolgens wordt met de G_M functie het GM bepaald.
    krachten2.append(-kracht_t2)
    posities2.append(positie_t2)
    posities3, krachten3 = removeBuoyantForce(posities2, krachten2, cob, calculateOpdrijvendeKracht(WEIGHT_WATER, bouyant_volume))
    lcg_schip, tcg_schip, vcg_schip = calculateZwaartepuntschip(posities3, krachten3)
    G_M = calculateG_M(bouyant_volume, SIt, vcg_schip, cob[2], it)
    output_1(3, str(entrance_angle), Rtot_14knp, G_M, 20, msp["Loa  [m]"], msp["B [m]"], h, msp["T moulded [m]"], 
             0, 0, STAALGEWICHT, WATERDICHTHEID, calculateKrachtensom1(krachten3)[0], lcg_schip, tcg_schip, vcg_schip, 
             bouyant_volume*WEIGHT_WATER, cob[0], cob[1], cob[2], 
             calculateKrachtensom1(krachten3)[0]+(bouyant_volume*WEIGHT_WATER), (calculateKrachtensom1(krachten3)[0]*(lcg_schip - cob[0])), 
             (calculateKrachtensom1(krachten3)[0]*(tcg_schip - cob[1])), 4, -WEIGHT_TRANSITION_PIECE*GRAVITATION_CONSTANT, lcg_tp, tcg_tp, vcg_tp, 0o3)
    output_kraan(swlmax, -WEIGHT_TRANSITION_PIECE*GRAVITATION_CONSTANT, lengte_kraan_fundatie, Draaihoogte_kraan, jib_length, Zwenkhoek, 
                 Giekhoek, LCG_TP, TCG_TP, VCG_TP, LCG_kraanhuis, TCG_kraanhuis, VCG_kraanhuis, LCG_kraanboom, TCG_kraanboom, 
                 VCG_kraanboom, LCG_heisgerei, TCG_heisgerei, VCG_heisgerei, 0o3)
    vul1, vul2, vul3 = vullingPercFunc(d1, d2, d3, momentensom1_, volume_t2, volume_t3)
    return

stabilitietsMain(versienummer, transom_bhd_thickness, rest_thickness, kraan_lcg, d1, d2, d3, dbh1, dbh2, dbh, msp, dha, dic_Shell_CSA, dic_csa_tank1, dic_csa_tank2, dic_csa_tank3, cob, h, bouyant_volume)