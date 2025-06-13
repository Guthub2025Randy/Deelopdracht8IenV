# -*- coding: utf-8 -*-
"""
Created on Mon May 12 13:21:19 2025

@author: randy
"""
from importGrasshopperFiles import *
from bibliotheek import *
import matplotlib.pyplot as plt
from schipFuncties import *
from outputCode import *

# Begin deelopdracht 8
def opwaartseKracht(dictio_csa, lengte_schip):
    """
    functie bepaalt de verdeelde belasting tgv de opwaartse kracht op elke cm van het schip
    Inputs:
    dictio_csa (dictionary): data van crosssectionareas van het onderwaterschip
    lengte_schip (np.array): x-coördinaten op elke centimeter van het schip
    Returns:
    opwaartse_kracht_cm (np.array): verdeelde belasting tgv de opwaartse kracht op elke cm van het schip in N/m
    """
    oppervlakte = dictio_csa[" crossarea_in_m2"]
    lps = dictio_csa["x_in_m"]
    oppervlakteInterp = ip.interp1d(lps, oppervlakte, kind='quadratic', fill_value='extrapolate')
    oppervlakte_cm = oppervlakteInterp(lengte_schip)
    onderwater_volume = []
    for i in range(len(oppervlakte_cm)-1):
        dx = lengte_schip[i+1]-lengte_schip[i]
        onderwater_volume.append(oppervlakte_cm[i]*dx)
    onderwater_volume.append(0)
    opwaartse_kracht_cm = np.array(onderwater_volume)*WEIGHT_WATER
    return opwaartse_kracht_cm

def traagheidsmomentOverLengte(traagheidsmoment_csa_shell, lengte_schip_csa_shell, lengte_schip):
    """
    functie bepaalt het traagheidsmoment op elke cm van het schip
    traagheidsmoment_csa_shell (np.array): traagheidsmoment van de romp op een aantal x-coördinaten
    lengte_schip_csa_shell (np.array): x-coördinaten overeenkomend met de traagheidsmomenten in traagheidsmoment_csa_shell
    lengte_schip (np.array): x-coördinaten op elke centimeter van het schip    
    Returns:
    traagheidsmoment_csa_shell_cm (np.array): traagheidsmoment op elke cm van het schip
    """
    interpoleerNaarCm = ip.interp1d(lengte_schip_csa_shell, traagheidsmoment_csa_shell, kind='cubic')
    traagheidsmoment_csa_shell_cm = interpoleerNaarCm(lengte_schip)
    return traagheidsmoment_csa_shell_cm

def ballastLoop(x_in_m, opp, lengte_schip):
    """
    functie bepaalt de verdeelde belasting tgv het gewicht van de vulling van een ballasttank
    Inputs:
    x_in_m (np.array): x-coördinaten op een aantal plekken op het schip
    opp (np.array): de oppervlaktes van de doorsneden van de tankvulling op de x-coördinaten van x_in_m
    Returns:
    neerwaartse_kracht (np.array): de verdeelde belasting tgv het gewicht van de vulling van de ballasttank
    """
    leng_scale = int(((x_in_m[-1] - x_in_m[0])*(len(lengte_schip)/(lengte_schip[-1] - lengte_schip[0]))))
    donnot = np.array([0.0])
    rescaling_length = np.linspace(x_in_m[0], x_in_m[-1], leng_scale)
    oppervlakteInterp = ip.interp1d(x_in_m, opp, kind='quadratic', fill_value=donnot)
    oppervlakte_cm = oppervlakteInterp(rescaling_length)
    water_volume = []
    for i in range(len(oppervlakte_cm)-1):
        dx = rescaling_length[i+1] - rescaling_length[i]
        water_volume.append(oppervlakte_cm[i]*dx)
    water_volume.append(0)
    neerwaartse_kracht_pre = np.array(water_volume)*WEIGHT_WATER
    neerwaartse_kracht = np.interp(lengte_schip, rescaling_length, neerwaartse_kracht_pre, left=0, right=0)
    return neerwaartse_kracht

def ballastwaterKracht(dic_tank, dic_tank_2, dic_tank_3, lengte_schip, scaling):
    """
    functie bepaalt de verdeelde belasting tgv het gewicht van de vullingen van alle ballasttanks samen
    Inputs:
    dic_tank (dictionary): data van tank 1
    dic_tank_2 (dictionary): data van tank 2
    dic_tank_3 (dictionary): data van tank 3
    lengte_schip (np.array): x-coördinaten op elke centimeter van het schip    
    Returns:
    neerwaartse_kracht_cm (np.array): de verdeelde belasting tgv het gewicht van de vullingen van de ballasttanks samen op elke cm in N/m
    """
    oppervlakte1 = dic_tank[" crossarea_in_m2"]
    lps1 = dic_tank["x_in_m"]
    oppervlakte2 = dic_tank_2[" crossarea_in_m2"]
    lps2 = dic_tank_2["x_in_m"]
    oppervlakte3 = dic_tank_3[" crossarea_in_m2"]
    lps3 = dic_tank_3["x_in_m"]
    neerwaartse_kracht1 = ballastLoop(lps1, oppervlakte1, lengte_schip)
    neerwaartse_kracht2 = ballastLoop(lps2, oppervlakte2, lengte_schip)
    neerwaartse_kracht3 = ballastLoop(lps3, oppervlakte3, lengte_schip)
    neerwaartse_kracht_cm = (neerwaartse_kracht1 + neerwaartse_kracht2 + neerwaartse_kracht3) * scaling
    return -neerwaartse_kracht_cm

def dwarskracht(q_x, lengte_schip):
    """
    functie bepaalt de dwarkrachtlijn
    q_x (np.array): de totale verdeelde belasting op elke cm van het schip in N/m
    lengte_schip (np.array): x-coördinaten op elke centimeter van het schip    
    Returns:
    dwarskracht (np.array): de dwarkracht op elke cm van het schip in N
    """
    dwarskracht = cumtrapz(q_x, lengte_schip, initial=0)
    dwarskracht[0]= 0
    dwarskracht[-1]= 0
    return dwarskracht

def buigendMoment(dwars_kracht, lengte_schip):
    """
    functie bepaalt momentenlijn
    dwars_kracht (np.array): de dwarkracht op elke cm van het schip in N
    lengte_schip (np.array): x-coördinaten op elke centimeter van het schip    
    Returns:
    buigend_moment (np.array): buigend moment op elke centimeter van het schip Nm
    """
    buigend_moment = cumtrapz(dwars_kracht, lengte_schip, initial=0)
    buigend_moment[0]= 0
    buigend_moment[-1]= 0
    return buigend_moment

def reducMoment(buigend_moment, i_traag):
    """
    functie bepaalt het gereduceerd moment
    Inputs:
    buigend_moment (np.array): buigend moment op elke centimeter van het schip in Nm
    i_traag (np.array): het traagheidsmoment van de romp op elke cm van het schip in m⁴
    Returns:
    gereduceerd_moment (np.array): het gereduceerde moment op elke cm van het schip
    """
    gereduceerd_moment = calcGarbageValues(buigend_moment)/(E*i_traag)
    return gereduceerd_moment


# door het gereduceerde moment de integreren krijg je de verdraaiing accent (phi accent)
def hoekverdraaiingAcc(gereduceerd_moment_uitkomst, lengte_schip):
    """
    Functie bepaalt de hoekverdraaiing phi'
    Inputs:
    gereduceerd_moment_uitkomst (np.array): gereduceerd moment op elke centimeter lengte van het schip
    lengte schip (np.array): array met de lengtewaardes van het schip per centimeter
    Returns:
    phi_accent (np.array): phi' op elke centimeter lengte van het schip
    """
    phi_accent_1 = cumtrapz(lengte_schip, gereduceerd_moment_uitkomst, initial = 0)
    phi_accent_1[0]=0
    phi_accent = phi_accent_1
    return phi_accent


# door de verdraaing accent (phi accent) te integreren krijg je de doorbuiging accent (w')

def doorbuigingAcc(phi_accent, lengte_schip):
    """
    Functie bepaalt de doorbuiging w'
    Inputs:
    phi_accent (np.array): phi' op elke centimeter lengte van het schip
    lengte schip (np.array): array met de lengtewaardes van het schip per centimeter
    Returns:
    w_acc (np.array): w' op elke centimeter lengte van het schip
    """
    w_acc = cumtrapz(lengte_schip, phi_accent, initial = 0)
    return w_acc

#phi
def hoekverdraaiing(phi_acc, lengte_schip, c):
    """
    Functie bepaalt de hookverdraaiing phi
    Inputs:
    phi_acc (np.array): phi' op elke centimeter lengte van het schip
    lengte_schip (np.array): array met de lengtewaardes van het schip per centimeter
    c (float): integratieconstante
    Returns:
    phi (np.array): hoekverdraaiing phi op elke centimeter lengte van het schip
    """
    phi_1 = phi_acc + c
    phi = phi_1
    return phi

#w
def doorbuiging(w_acc, lengte_schip, c):
    """
    Functie bepaalt de doorbuiging w op elke centimeter lengte van het schip
    Inputs:
    w_acc (np.array): w' op elke centimter lengte van het schip
    lengte_schip (np.array): array met de lengtewaardes van het schip per centimeter
    c (float): integratieconstante
    Returns:
    w (np.array): doorbuiging w op elke centimeter lengte van het schip
    """
    w = w_acc + c*(lengte_schip - lengte_schip[0])
    return w

def traagheidsmomentAsymptoot(traag_shell, l_shell, lengte_in_cm, huiddikte):
    """
    Het traagheidsmoment loopt bij de punt van het schip richting nul. Om een deel door nul fout te voorkomen worden de waardes 
    afgekapt. Dat doet deze functie.
    Inputs:
    traag_shell (np.array): traagheidsmoment van de romp op een aantal x-coördinaten
    l_shell (np.array): x-coördinaten overeenkomend met de traagheidsmomenten in traagheidsmoment_csa_shell
    lengte_in_cm (np.array): x-coördinaten op elke centimeter van het schip  
    huiddikte (float): in m
    Returns:
    traag2 (np.array): het afgesneden traagheidsmoment op elke cm van het schip in m⁴
    """
    traag1 = traagheidsmomentOverLengte(traag_shell, l_shell, lengte_in_cm) 
    traag2 = calcGarbageValues(traag1)
    return traag2

def parabolischProfielTP(zwaartepunt_tp, totaal_kracht, lengte_in_cm, straal_tp):
    """
    functie bepaalt de paraboolvormige verdeelde belasting van een transition piece
    Inputs:
    zwaartepunt_tp (float): lcg van de transition piece
    totaal_kracht (float): het gewicht van de transition piece in N
    lengte_in_cm (np.array): x-coördinaten op elke centimeter van het schip  
    straal_tp (float): straal van de transition piece in m
    Returns:
    kracht (np.array): verdeelde belansting tgv het gewicht van de transition piece op elke cm van het schip
    """
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

def calculateSpiegel(arr_lengte, dic, huiddikte):
    """
    functie bepaalt de verdeelde belasting tgv het gewicht van de spiegel
    Inputs: 
    arr_lengte (np.array): x-coördinaten op elke centimeter van het schip
    dic (dictionary): data van de romp
    huiddikte (float): in m
    Returns:
    arr_gewicht (array): verdeelde belasting tgv het gewicht van de spiegel op elke cm van het schip in N/m
    """
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
    arr_gewicht: een array met de waarden van de verdeelde belasting tgv het gewicht van de huid in N/m op elke centimeter van de lengte. 
    """
    x = dic_shell["X [m]"]
    w = np.zeros(len(arr_x))
    w = dic_shell["CROSS SECTION AREA OF SHELL PLATING [m2]"]*WEIGHT_STAAL*huiddikte
    f = ip.interp1d(x,w, kind='cubic')
    arr_gewicht = f(arr_x)
    return -arr_gewicht

def calculateTrapezium(arr_lengte, dic_bh, huiddikte):
    """
    functie bepaalt de verdeelde belasting van de tankschotten op basis van een trapeziumvorminge benadering. 
    Inputs: 
    arr_lengte (np.array): array met de lengtewaardes van het schip per centimeter
    dic_schot (dictionary): de dictionary met de waarden uit het BHData bestand
    Returns:
    arr_gewicht (np.array): array met de verdeelde belasting van de tankschotten op elke centimeter lengte
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
    De functie bepaalt de verdeelde belasting van de kraan op het dek tijdens de hijsoperatie (dus inclusief een tussenstuk in de kraan)
    Imputs:
    zwaartepunt_tp (float): x-coördinaat van het aangrijpingspunt van het gewicht van het kraanhuis op het dek
    totaal_kracht (float): het totale gewicht van de kraan en kraanlast samen in N
    lengte_in_cm (np.array): een array van x-coördinaten voor elke centimeter van het schip. 
    straal_kraanhuis (float): in m
    Returns:
    kracht (np.array): een array met de verdeelde belasting op het dek ten gevolge van de kraan op elke centimeter van het schip in N/m
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
    """
    functie bepaalt de gezamenlijke verdeelde belasting van meerdere transition pieces
    Inputs:
    lading_posities (lijst): de lcg's van alle transition pieces
    massas (lijst): de gewichten van de transition pieces in N
    lengte_in_cm (np.array): een array van x-coördinaten voor elke centimeter van het schip. 
    straal (float): de straal van de transition pieces in m
    Returns:
    krachtverdeling (np.array): de gezamenlijke verdeelde belasting van meerdere transition pieces in N/m
    """
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
    Returns:
    q_out (np.array): verdeelde belasting van de cirkelvormige belasting in N/m
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
    """
    functie bepaalt de hoogte van de neutrale as van de romp op elke cm lengte van het schip
    Inputs:
    lengte_schip (np.array): een array van x-coördinaten voor elke centimeter van het schip. 
    tussenstappen_lengte (np.array): x-coördinaten van verschillende plekken op het schip
    hoogte_neutrale_as (np.array): waarden voor de hoogte van de neutrale as op de x-coördinaten in tussenstappen_lengte in m
    Returns:
    volledig2 (np.array): hoogte van de neutrale as van de romp op elke cm lengte van het schip in m
    """
    volledig = ip.interp1d(tussenstappen_lengte, hoogte_neutrale_as, kind="quadratic", fill_value="extrapolate")
    volledig2 = volledig(lengte_schip)
    return volledig2

def calcKiel(lengte_schip, tussenstappen_lengte, hoogte_kiel):
    """
    functie bepaalt de hoogte van de kiel op elk cm van het schip
    Inputs:
    lengte_schip (np.array): een array van x-coördinaten voor elke centimeter van het schip. 
    tussenstappen_lengte (np.array): x-coördinaten van verschillende plekken op het schip
    hoogte_kiel (np.array): waarden voor de hoogte van de kiel op de x-coördinaten in tussenstappen_lengte in m
    Returns:
    geinterpoleerd2 (np.array): de hoogte van de kiel op elk cm van het schip in m
    """
    geinterpoleerd = ip.interp1d(tussenstappen_lengte, hoogte_kiel, kind="quadratic", fill_value="extrapolate")
    geinterpoleerd2 = geinterpoleerd(lengte_schip)
    return geinterpoleerd2 

def calcVezelafstand(centroid_cm, kiel_cm):
    """
    functie bepaalt de vezelafstand op elke cm van het schip
    Inputs:
    controid_cm (np.array): hoogte van de neutrale as van de romp op elke cm lengte van het schip in m
    kiel_cm (np.array): de hoogte van de kiel op elk cm van het schip in m
    Returns:
    vezelafstand (np.array): vezelafstand op elke cm van het schip in m
    """
    vezelafstand= centroid_cm - kiel_cm
    return vezelafstand

def sterkteMain(d1, d2, d3, dbh1, dbh2, dbh, msp, dha, dic_shell_csa, dic_csa_tank1, dic_csa_tank2, dic_csa_tank3, cob, h, bouyant_volume, length_schip, it, l_shell, i_x_shell, bouyant_csa, lcgs_tp, lengte_cm, straal_tp, rest_thickness, transom_bhd_thickness, kraan_lcg, swlmax, straal_kraanhuis, weight_kraan_totaal, weights_tp, tussenstappen_lengte, hoogte_neutrale_as, hoogte_kiel):
    """
    Functie voert de stabiliteitsberekeningen uit door eerdere functies aan te roepen
    Inputs:
    versienummer (float)
    
    d1 (dictionary): data van tank 1
    d2 (dictionary): data van tank 2
    d3 (dictionary): data van tank 3
    dbh1 (dictionary): data van tankschotten (zonder die van tank 2)
    dbh2 (dictionary): data van tankschotten van tank 2
    dbh (dictionary): data van alle tankschotten
    msp (dictionary): data van hoofdafmetingen 
    dha (dictionary): data van de romp
    dic_shell_csa (dictionary): data mbt de crossection areas van de romp
    dic_csa_tank1 (dictionary): data mbt de crossection areas van tank 1
    dic_csa_tank2 (dictionary): data mbt de crossection areas van tank 2
    dic_csa_tank3 (dictionary): data mbt de crossection areas van tank 3
    cob (np.array): drukkingspunt
    h (float): holte in m
    bouyant_volume (float): onderwatervolume in m³
    length_schip (float): lengte van het schip in m 
    it (float): traagheidsmoment waterlijn rond de x-as in m⁴
    l_shell (np.array): x-coördinaten overeenkomend met de traagheidsmomenten in traagheidsmoment_csa_shell
    i_x_shell (np.array): traagheidsmoment van de romp op een aantal x-coördinaten in m⁴
    bouyant_csa (dictionary): data van crosssectionareas van het onderwaterschip
    lcgs_tp (lijst): de lcg's van alle transition pieces
    lengte_cm (np.array): x-coördinaten op elke centimeter van het schip 
    straal_tp (float): straal van de transition piece in m
    rest_thickness (float): plaatdikte romp in m
    transom_bhd_thickness (float): plaatdikte schotten en spiegel in m
    kraan_lcg (float): x-coördinaat van zwaartpunt kraan
    swlmax (float): maximale safe working load in N
    straal_kraanhuis (float): in m
    weight_kraan_totaal (float): het totale gewicht van de kraan en kraanlast samen in N
    weights_tp (lijst): gewichten transitionpieces in N
    tussenstappen_lengte (np.array): x-coördinaten van verschillende plekken op het schip
    hoogte_neutrale_as (np.array): waarden voor de hoogte van de neutrale as op de x-coördinaten in tussenstappen_lengte in m
    hoogte_kiel (np.array): waarden voor de hoogte van de kiel op de x-coördinaten in tussenstappen_lengte in m

    Returns:
    maximale_spanning (float): in Pa
    q (np.array): de totale verdeelde belasting op elke cm van het schip in N/m
    dwars_kracht (np.array): de dwarkracht op elke cm van het schip in N
    buigend_moment (np.array): buigend moment op elke centimeter van het schip in Nm
    centroid_z_in_cm (np.array): hoogte van de neutrale as van de romp op elke cm lengte van het schip in m
    spanning (np.array): maximale spanning in de romp op elke cm lengte van het schip in Pa
    reduct_m (np.array): het gereduceerde moment op elke cm van het schip
    hoekverdraai_accent (np.array): phi' op elke centimeter lengte van het schip
    doorbuig_acc (np.array): w' op elke centimter lengte van het schip
    hoekverdraai (np.array): hoekverdraaiing phi op elke centimeter lengte van het schip
    doorbuig (np.array): doorbuiging w op elke centimeter lengte van het schip
    traag (np.array): het afgesneden traagheidsmoment op elke cm van het schip in m⁴
    opwaartse_kracht (np.array): verdeelde belasting tgv de opwaartse kracht op elke cm van het schip in N/m
    neerwaartse_kracht_3 (np.array): een array met de waarden van de verdeelde belasting tgv het gewicht van de huid in N/m op elke centimeter van de lengte. 
    kracht_ballast (np.array): de verdeelde belasting tgv het gewicht van de vullingen van de ballasttanks samen op elke cm in N/m
    neerwaartse_kracht_2 (np.array): array met de verdeelde belasting van de tankschotten op elke centimeter lengte
    neerwaartse_kracht_1 (np.array): verdeelde belasting tgv het gewicht van de spiegel op elke cm van het schip in N/m
    kracht_kraan (np.array): verdeelde belasting van de kraan in N/m
    kracht_tp (np.array): de gezamenlijke verdeelde belasting van meerdere transition pieces in N/m
    """
    scaling = ((len(lengte_cm)-1)/(lengte_cm[-1] - lengte_cm[0]))
    opwaartse_kracht = opwaartseKracht(bouyant_csa, lengte_cm) * scaling
    traag = traagheidsmomentAsymptoot(i_x_shell, l_shell, lengte_cm, rest_thickness)
    kracht_ballast = ballastwaterKracht(dic_csa_tank1, dic_csa_tank2, dic_csa_tank3, lengte_cm, scaling)
    kracht_tp = berekenKrachtVerdeling(lcgs_tp, -weights_tp, lengte_cm, straal_tp)
    kracht_kraan = calcParaboolFunctie(kraan_lcg, weight_kraan_totaal, lengte_cm, straal_kraanhuis)
    neerwaartse_kracht_1 = calculateSpiegel(lengte_cm, dha, transom_bhd_thickness)
    neerwaartse_kracht_2 = calculateTrapezium(lengte_cm, dbh, transom_bhd_thickness)
    neerwaartse_kracht_3 = calculateHuid(lengte_cm, 1, dic_shell_csa)
    q = opwaartse_kracht + kracht_ballast + kracht_kraan + kracht_tp + neerwaartse_kracht_2 + neerwaartse_kracht_3 + neerwaartse_kracht_1
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
    return maximale_spanning, q, dwars_kracht, buigend_moment, centroid_z_in_cm, spanning, reduct_m, hoekverdraai_accent, doorbuig_acc, hoekverdraai, doorbuig, traag, opwaartse_kracht, neerwaartse_kracht_3, kracht_ballast, neerwaartse_kracht_2, neerwaartse_kracht_1, kracht_kraan, kracht_tp
