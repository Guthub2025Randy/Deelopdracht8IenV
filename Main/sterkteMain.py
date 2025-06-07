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

# Begin deelopdracht 8
def opwaartseKracht(dictio_CSA, lengte_schip):
    oppervlakte = dictio_CSA[" crossarea_in_m2"]
    lps = dictio_CSA["x_in_m"]
    oppervlakteInterp = ip.interp1d(lps, oppervlakte, kind='quadratic', fill_value='extrapolate')
    oppervlakte_cm = oppervlakteInterp(lengte_schip)
    Onderwater_volume = []
    for i in range(len(oppervlakte_cm)-1):
        dx = lengte_schip[i+1]-lengte_schip[i]
        Onderwater_volume.append(oppervlakte_cm[i]*dx)
    Onderwater_volume.append(0)
    opwaartse_kracht_cm = np.array(Onderwater_volume)*WEIGHT_WATER
    return opwaartse_kracht_cm

def traagheidsmomentOverLengte(traagheidsmoment_csa_shell, lengte_schip_csa_shell, lengte_schip):
    interpoleer_naar_cm = ip.interp1d(lengte_schip_csa_shell, traagheidsmoment_csa_shell, kind='cubic')
    traagheidsmoment_csa_shell_cm = interpoleer_naar_cm(lengte_schip)
    return traagheidsmoment_csa_shell_cm

def ballastLoop(x_in_m, opp, lengte_schip):
    leng_scale = int(((x_in_m[-1] - x_in_m[0])*(len(lengte_schip)/(lengte_schip[-1] - lengte_schip[0]))))
    donnot = np.array([0.0])
    rescaling_length = np.linspace(x_in_m[0], x_in_m[-1], leng_scale)
    oppervlakteInterp = ip.interp1d(x_in_m, opp, kind='quadratic', fill_value=donnot)
    oppervlakte_cm = oppervlakteInterp(rescaling_length)
    Water_volume = []
    for i in range(len(oppervlakte_cm)-1):
        dx = rescaling_length[i+1] - rescaling_length[i]
        Water_volume.append(oppervlakte_cm[i]*dx)
    Water_volume.append(0)
    Neerwaartse_kracht_pre = np.array(Water_volume)*WEIGHT_WATER
    Neerwaartse_kracht = np.interp(lengte_schip, rescaling_length, Neerwaartse_kracht_pre, left=0, right=0)
    return Neerwaartse_kracht

def ballastwaterKracht(dic_tank, dic_tank_2, dic_tank_3, lengte_schip, scaling):
    oppervlakte1 = dic_tank[" crossarea_in_m2"]
    lps1 = dic_tank["x_in_m"]
    oppervlakte2 = dic_tank_2[" crossarea_in_m2"]
    lps2 = dic_tank_2["x_in_m"]
    oppervlakte3 = dic_tank_3[" crossarea_in_m2"]
    lps3 = dic_tank_3["x_in_m"]
    Neerwaartse_kracht1 = ballastLoop(lps1, oppervlakte1, lengte_schip)
    Neerwaartse_kracht2 = ballastLoop(lps2, oppervlakte2, lengte_schip)
    Neerwaartse_kracht3 = ballastLoop(lps3, oppervlakte3, lengte_schip)
    Neerwaartse_kracht_cm = (Neerwaartse_kracht1 + Neerwaartse_kracht2 + Neerwaartse_kracht3) * scaling
    return -Neerwaartse_kracht_cm

def dwarskracht(q_x, lengte_schip):
    dwarskracht = cumtrapz(q_x, lengte_schip, initial=0)
    dwarskracht[0]= 0
    dwarskracht[-1]= 0
    return dwarskracht

def buigendMoment(dwars_kracht, lengte_schip):
    buigend_moment = cumtrapz(dwars_kracht, lengte_schip, initial=0)
    buigend_moment[0]= 0
    buigend_moment[-1]= 0
    return buigend_moment

def reducMoment(buigend_moment, i_traag):
    gereduceerd_moment = calcGarbageValues(buigend_moment)/(E*i_traag)
    return gereduceerd_moment


# door het gereduceerde moment de integreren krijg je de verdraaiing accent (phi accent)
def hoekverdraaiingAcc(gereduceerd_moment_uitkomst, lengte_schip):
    phi_accent_1 = cumtrapz(lengte_schip, gereduceerd_moment_uitkomst, initial = 0)
    phi_accent_1[0]=0
    phi_accent = phi_accent_1
    return phi_accent


# door de verdraaing accent (phi accent) te integreren krijg je de doorbuiging accent (w')

def doorbuigingAcc(phi_accent, lengte_schip):
    w_acc = cumtrapz(lengte_schip, phi_accent, initial = 0)
    return w_acc

#phi
def hoekverdraaiing(phi_acc, lengte_schip, c):
    phi_1 = phi_acc + c
    phi = phi_1
    return phi

#w
def doorbuiging(w_acc, lengte_schip, c):
    w = w_acc + c*(lengte_schip - lengte_schip[0])
    return w

def traagheidsmomentAsymptoot(traag_shell, l_shell, lengte_in_cm, huiddikte):
    # Het traagheidsmoment loopt bij de punt van het schip richting nul. Om een deel door nul fout te voorkomen worden de waardes afgekapt.
    traag1 = traagheidsmomentOverLengte(traag_shell, l_shell, lengte_in_cm) 
    traag2 = calcGarbageValues(traag1)
    return traag2

def parabolischProfielTP(zwaartepunt_tp, totaal_kracht, lengte_in_cm, straal_tp):
    """de input van deze functie is het zwaartepunt van één Transition Piece, de totale kracht van alle transition pieces
    en een array over de lengte van het schip die te vinden is in de main. dan maakt hij eerst het bereik waar het parabolisch profiel van de TP's
    te vinden is. dan maakt hij van de fysieke positie een index in een array. in het 2de deel van de functie bereidt hij parabool waarden voor.
    x_norm zijn dan de genormaliseerde afstanden tov het zwaartepunt. in het laatste deel maakt hij het parabolisch profiel en alle negatieve waardes op 0. 
    en dan zorgt hij ervoor dat de som gelijk is aan de totale kracht."""
    start = lengte_in_cm[0]
    eind = lengte_in_cm[-1]
    begin = max(zwaartepunt_tp - straal_tp, start)
    eind = min(zwaartepunt_tp + straal_tp, eind)
    idx_begin = int(begin - start)
    idx_eind = int(eind - start)

    bereik = np.arange(idx_begin, idx_eind + 1)
    afstanden = (bereik + start) - zwaartepunt_tp
    x_norm = afstanden / straal_tp

    profiel = np.clip(1 - x_norm**2, 0, None)
    profiel /= profiel.sum()
    profiel *= totaal_kracht
    kracht = np.zeros(len(lengte_in_cm))
    for i in range(len(bereik)):
      kracht[int(bereik[0]*100)+i] = profiel[i]
    return kracht

# deze functie moeten nog geplot worden. met lengte op de x-as en krachtverdeling op de y-as. met als title: "Krachtverdeling over het Schip"

def calculateSpiegel(arr_lengte, dic, huiddikte):
  fg_totaal = dic["Transom Area "][0]*huiddikte*WEIGHT_STAAL
  scaling = int(((len(arr_lengte))/(arr_lengte[-1] - arr_lengte[0])))
  fg_per_cm = (1.25*fg_totaal)/(scaling/10)
  arr_gewicht = np.zeros(len(arr_lengte))
  for i in range(int(scaling)):
    arr_gewicht[i] += fg_per_cm
  return -arr_gewicht*(scaling/10)

def calculateHuid(arr_x, huiddikte, dic_shell):
  """
  functie berekent de verdeelde belasting van de huid. 
  Inputs:
  arr_x: array met de lengtewaardes van het schip per centimeter
  huiddikte: in m (float)
  dic_csa: dictionary met de waarden uit het shell_csa bestand
  Returns:
  arr_gewicht: een array met de waarden van de verdeelde belasting in N/m op elke centimeter van de lengte. 
  """
  x = dic_shell["X [m]"]
  w = np.zeros(len(arr_x))
  w = dic_shell["CROSS SECTION AREA OF SHELL PLATING [m2]"]*WEIGHT_STAAL*huiddikte
  f = ip.interp1d(x,w, kind='cubic')
  arr_gewicht = f(arr_x)
  return -arr_gewicht

def calculateTrapezium(arr_lengte, dic_bh, huiddikte):
  """
  functie bepaalt de verdeelde belasting van de tankschotten.
  Inputs: 
  arr_lengte: array met de lengtewaardes van het schip per centimeter
  dic_schot: de dictionary met de waarden uit het BHData bestand
  Returns:
  arr_gewicht: array met de verdeelde belasting van de tankschotten op elke centimeter lengte
  """
  arr_gewicht = np.zeros(len(arr_lengte))
  for x in dic_bh:
    xmin = dic_bh[x][4]
    xmax = dic_bh[x][5]
    lcg = dic_bh[x][1]
    A = dic_bh[x][0]*WEIGHT_STAAL*huiddikte
    ixb = int(round(xmin*100)-100*arr_lengte[0])
    ixe = int(round(xmax*100)-100*arr_lengte[0])
    lcg_l = lcg - xmin
    if lcg == xmin + (xmax-xmin)/2:
      a = A/(xmax-xmin)
      b = A/(xmax-xmin)
    elif lcg == xmin + (xmax-xmin)/3:
      a = A/(xmax-xmin)*2
      b = 0
    elif lcg == xmin + 2*(xmax-xmin)/3:
      a = 0
      b = A/(xmax-xmin)*2
    elif lcg < xmin + (xmax-xmin)/3 or lcg > xmin + 2*(xmax-xmin)/3:
      print(f"error: object moet opgedeeld worden")
      exit
    elif lcg < xmin + (xmax-xmin)/2:
      a = 4*A/(xmax-xmin) -  6*A*lcg_l/(xmax-xmin)**2
      b = 6*A*lcg_l/(xmax-xmin)**2-2*A/(xmax-xmin)
    else:
      a = 4*A/(xmax-xmin) -  6*A*lcg_l/(xmax-xmin)**2
      b = 6*A*lcg_l/(xmax-xmin)**2-2*A/(xmax-xmin)
    arr = np.linspace(a,b,ixe-ixb)
    for i in range(len(arr)):
      arr_gewicht[ixb+i] = arr_gewicht[ixb+i]+arr[i]
  return -arr_gewicht

def parabolischProfielKraan(zwaartepunt_tp, totaal_kracht, lengte_in_cm, straal_kraanhuis):
    """
    Nog te bepalen: straal kraanhuis als argument, lokale variabele bepaald binnen de functie of global variable.

    De functie bepaalt de verdeelde belasting van de kraan op het dek tijdens de hijsoperatie (dus inclusief een tussenstuk in de kraan)
    Imputs:
    zwaartepunt_tp: x-coördinaat van het aangrijpingspunt van het gewicht van het kraanhuis op het dek (float)
    totaal_kracht: het totale gewicht van de kraan en kraanlast samen (float)
    lengte_in_cm: een array van x-coördinaten voor elke centimeter van het schip. Deze array heeft dus 14901 elementen en loopt van -9 tot 140.
    Returns:
    kracht: een array met de verdeelde belasting op het dek ten gevolge van de kraan op elke centimeter van het schip. Deze array heeft dus 14901 elementen.
    """
    start = lengte_in_cm[0]
    eind_len = lengte_in_cm[-1]
    begin = max(zwaartepunt_tp - straal_kraanhuis, start)
    eind = min(zwaartepunt_tp + straal_kraanhuis, eind_len)
    #conversion to distance from stern instead of from achterloodlijn
    idx_begin = int((begin - start))
    idx_eind = int((eind - start))

    bereik = np.arange(idx_begin, idx_eind + 0.01, 0.01)
    afstanden = (bereik + start) - zwaartepunt_tp
    x_norm = afstanden / straal_kraanhuis
    profiel = np.clip(1 - x_norm**2, 0, None)
    profiel /= profiel.sum()
    profiel *= totaal_kracht
    kracht = np.zeros(len(lengte_in_cm))
    for i in range(len(bereik)):
      kracht[int(bereik[0]*100)+i] = profiel[i]
    return kracht

def berekenKrachtVerdeling(lading_posities, massas, lengte_in_cm, straal):
    """hier maakt hij eerst een krachten verdeling van 0 over de lengte. dan maakt hij van de massa van de TPs het gewicht van de TPs.
    doormiddel van de functie parabolischProfielTP voegt hij deze kracht verdeling toe op de eerst  zero-array over de lengte."""
    krachtverdeling = np.zeros(len(lengte_in_cm))
    for pos in lading_posities:
        krachtverdeling += calcParaboolFunctie(pos, massas[0], lengte_in_cm, straal)
    return krachtverdeling

def calcParaboolFunctie(locatie, totaal_gewicht, arr_lengte, straal):
  """
  Functie stelt een paraboolvormige verdeelde belasting op voor een belasting dat een cirkelvormig contactoppervlak heeft met het dek en 
  een homogene masseverdeling heeft.
  Inputs:
  locatie: de x-coördinaat van het zwaartepunt van de last in m (float/int)
  totaal_gewicht: het gewicht van de last in N (float)
  straal: straal van het contactoppervlak in m (float)
  arr_lengte: array met de x-coördinaat met van elke centimeter lengte van het schip (np.array)
  """
  n_points = 2 * straal * 100 + 1
  x = np.linspace(-straal, straal, n_points)

  #Hertzian pressure distribution: q(x) = q0 * sqrt(1 - (2x/L)^2)
  #Totale last = (π/4) * q0 * L → solve for q0
  q0 = (4 / np.pi) * totaal_gewicht / (2*straal)
  q = q0 * np.sqrt(1 - (2 * x / (2*straal))**2)

  #Kleine negatieve waarden corrigeren
  q = np.where(q <= 0, q, 0)

  #Op de juiste plaats in array zetten
  i_start = int((locatie - straal - arr_lengte[0])*100)
  q_out = np.zeros(len(arr_lengte))
  for i in range(len(q)):
    q_out[i_start+i] = q[i]
  return q_out

def calcNeutraleAs(lengte_schip, tussenstappen_lengte, hoogte_neutrale_as):
    volledig = ip.interp1d(tussenstappen_lengte, hoogte_neutrale_as, kind="quadratic", fill_value="extrapolate")
    volledig2 = volledig(lengte_schip)
    return volledig2

def calcKiel(lengte_schip, tussenstappen_lengte, hoogte_kiel):
    geinterpoleerd = ip.interp1d(tussenstappen_lengte, hoogte_kiel, kind="quadratic", fill_value="extrapolate")
    geinterpoleerd2 = geinterpoleerd(lengte_schip)
    return geinterpoleerd2 

def calcVezelafstand(centroid_cm, kiel_cm):
    vezelafstand= centroid_cm - kiel_cm
    return vezelafstand

def sterkteMain(d1, d2, d3, dbh1, dbh2, dbh, msp, dha, dic_shell_csa, dic_csa_tank1, dic_csa_tank2, dic_csa_tank3, cob, h, bouyant_volume, length_schip, it, l_shell, i_x_shell, bouyant_csa, lcgs_tp, lengte_cm, straal_tp, rest_thickness, transom_bhd_thickness, kraan_lcg, swlmax, straal_kraanhuis, weight_kraan_totaal, weights_tp, tussenstappen_lengte, hoogte_neutrale_as, hoogte_kiel):
    scaling = ((len(lengte_cm)-1)/(lengte_cm[-1] - lengte_cm[0]))
    opwaartse_Kracht = opwaartseKracht(bouyant_csa, lengte_cm) * scaling
    traag = traagheidsmomentAsymptoot(i_x_shell, l_shell, lengte_cm, rest_thickness)
    Kracht_Ballast = ballastwaterKracht(dic_csa_tank1, dic_csa_tank2, dic_csa_tank3, lengte_cm, scaling)
    kracht_TP = berekenKrachtVerdeling(lcgs_tp, -weights_tp, lengte_cm, straal_tp)
    kracht_kraan = calcParaboolFunctie(kraan_lcg, weight_kraan_totaal, lengte_cm, straal_kraanhuis)
    neerwaartse_kracht_1 = calculateSpiegel(lengte_cm, dha, transom_bhd_thickness)
    neerwaartse_kracht_2 = calculateTrapezium(lengte_cm, dbh, transom_bhd_thickness)
    neerwaartse_kracht_3 = calculateHuid(lengte_cm, 1, dic_shell_csa)
    q = opwaartse_Kracht + Kracht_Ballast + kracht_kraan + kracht_TP + neerwaartse_kracht_2 + neerwaartse_kracht_3 + neerwaartse_kracht_1
    #plotten van q
    dwars_kracht = dwarskracht(q, lengte_cm)
    #numpy masking is onze keuze voor randwaardes
    buigend_moment = buigendMoment(dwars_kracht, lengte_cm)
    lengte_zonder_rand = calcGarbageValues(lengte_cm)
    reduct_m = reducMoment(buigend_moment, traag)
    #plotten van het gereduceerde moment.
    hoekverdraai_accent = hoekverdraaiingAcc(reduct_m, lengte_zonder_rand)
    doorbuig_acc = doorbuigingAcc(hoekverdraai_accent, lengte_zonder_rand)
    # hoekverdraaing (phi) = phi_accent + C
    # Doorbuiging (w) = w_acc +C
    # Dus C berekenen:
    c = doorbuig_acc[-1]/length_schip
    hoekverdraai = hoekverdraaiing(hoekverdraai_accent, lengte_zonder_rand, c)
    doorbuig = doorbuiging(doorbuig_acc, lengte_zonder_rand, c)
    centroid_z_in_cm = calcNeutraleAs(lengte_cm, tussenstappen_lengte, hoogte_neutrale_as)
    kiel_z_in_cm = calcKiel(lengte_cm, tussenstappen_lengte, hoogte_kiel)
    vezelafstand_in_cm = calcVezelafstand(centroid_z_in_cm, kiel_z_in_cm)
    spanning = calcGarbageValues(buigend_moment * vezelafstand_in_cm) / traag    
    maximale_spanning = max(spanning)
    return maximale_spanning, q, dwars_kracht, buigend_moment, centroid_z_in_cm, spanning, reduct_m, hoekverdraai_accent, doorbuig_acc, hoekverdraai, doorbuig, traag
