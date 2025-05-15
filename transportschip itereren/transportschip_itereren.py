# -*- coding: utf-8 -*-
"""
Created on Wed May 14 13:51:35 2025

@author: randy
"""

from importGrasshopperFiles import *
from bibliotheek import *
import matplotlib.pyplot as plt
from output_code import *

def funcPlotFill(x_plot, y_plot, x_naam, y_naam, titel_naam, functie_naam, kleur_functie):
    plt.figure(figsize=(8,5))
    plt.plot(x_plot, y_plot, label=f"{functie_naam}", color=f'{kleur_functie}')
    plt.fill_between(x_plot, y_plot, alpha=0.3, color=f'{kleur_functie}')
    plt.xlabel(f"{x_naam}")
    plt.ylabel(f"{y_naam}")
    plt.title(f"{titel_naam}")
    plt.legend()
    plt.grid(True)
    plt.show()
    plt.close()
    return None

def funcPlot(x_plot, y_plot, x_naam, y_naam, titel_naam, functie_naam, kleur_functie):
    plt.figure(figsize=(8,5))
    plt.plot(x_plot, y_plot, label=f"{functie_naam}", color=f'{kleur_functie}')
    plt.xlabel(f"{x_naam}")
    plt.ylabel(f"{y_naam}")
    plt.title(f"{titel_naam}")
    plt.legend()
    plt.grid(True)
    plt.show()
    plt.close()
    return None

def interpolerenLocatie(dictionary_ballasttank, vulling_tank, tanknummer):
    """
    Deze functie bepaalt van het water een ballasttank het zwaartepunt. Als input neemt hij de dictionary waarin de zwaartepunten
    van de tank bij gegeven vullingen staat, de werkelijke vulling, en het tanknummer. Door interpolatie worden het zwaartepunt
    bepaald en teruggegeven als array.
    """
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

def calculateWeightKraan(Krachten, Posities, H, kraan_lcg, SWLMax):
    """
    Deze functie heeft als doel aan twee lijsten, een met floats die krachten representeren, en aan een ander van arrays die
    elk een positie in het xyz vlak representeren, respectievelijk de zwaartekrachten en hun aangrijpingspunten toe te voegen.
    Ook het gewicht van de deklading (ZwaarteWindmolen) wordt toegevoegd. De aangevulde lijsten worden teruggegeven.
    """
    ZwaarteWindmolen = -WEIGHT_TRANSITION_PIECES
    arrayPositieWindmolen = np.array([40, -2, H+10])
    Posities.append(arrayPositieWindmolen)
    Krachten.append(ZwaarteWindmolen)
    return Krachten, Posities

def calculateOpdrijvendeKracht(gewicht_water, onderwater_volume):
    """
    deze functie berekent de opdrijvende kracht op basis van het onderwatervolume en de dichtheid van water.
    """
    opdrijvende_kracht = gewicht_water * onderwater_volume
    return opdrijvende_kracht

def positiesmetkrachtenlijst1(dictionary_bulkheads, locatie3, kracht3, H, COB, Staalgewicht, Plaatdikte, kraan_lcg, SWLMax, dictionary_hull, Plaatdikte2, opdrijvende_kracht):
    """
    Deze functie doet exact hetzelfde als de bovenstaande functie, behalve dat hier het gewicht en zwaartepunt van tank 1
    niet als arguments worden gevraagd. Deze functie genereert dus lijsten waarmee een resultant transversaal moment kan worden
    berekend dat gelijk gecorrigeerd moet worden door de vulling van tank 1.
    """
    posities = []
    krachten = []
    posities1 = []
    krachten1 = []
    for key, value in dictionary_bulkheads.items():
        posities.append(value[1:4])
        krachten.append(float(-value[0]*Staalgewicht*Plaatdikte))
    for key, value in dictionary_hull.items():
        x = float(value[1])
        y = float(value[2])
        z = float(value[3])
        posities.append(np.array([x, y, z]))
        if key == "Transom Area ":
            krachten.append(float(-value[0]*Staalgewicht*Plaatdikte))
        else:
            krachten.append(float(-value[0]*Staalgewicht*Plaatdikte2))
    krachten1, posities1 = calculateWeightKraan(krachten, posities, H, kraan_lcg, SWLMax)
    krachten1.append(float(-kracht3))
    krachten1.append(opdrijvende_kracht)
    posities1.append(locatie3)
    posities1.append(COB)
    return krachten1, posities1

def calculateMoment(positie,kracht):
    """
    deze functie berekent het kruisproduct tussen twee vectoren (in de vorm van arrays) en geeft een array terug die gelijk is
    aan dit kruisproduct. Als een krachtvector en positievector als arguments worden opgegeven berekent de functie dus het moment.
    """
    Moment = np.cross(positie, kracht)
    return Moment

def calculateMomentensom(posities, krachten):
    """
    Deze functie ontvangt twee lijsten aan input. De lijst van posities hoort te bestaan uit arrays met drie elementen: de lcg,
    tcg en vcg van elke massa (in het geval van de opdrijvende kracht het COB). De lijst van krachten bestaat uit floats die gelijk
    zijn aan de grootte van de corresponderende (zwaarte)krachten. Door middel van een for loop en de eerder geschreven momentfunctie
    worden de momenten van alle krachten bij elkaar opgeteld. Vervolgens wordt dit in de vorm van een array die de resultante
    momentvector bevat teruggegeven (dus drie elementen overeenkomend met resp. moment rond de x-as, y-as en z-as.
    """
    if len(posities) != len(krachten):
        print("Error, niet gelijke hoeveelheden krachten gekregen voor de eerste momentensom")
        return None
    momentensom = np.array([0.0,0.0,0.0])
    for i in range(len(krachten)):
        positie_1 = posities[i][0]
        positie_2 = posities[i][1]
        positie_3 = posities[i][2]
        momentensom += calculateMoment(np.array([positie_1,positie_2,positie_3]), np.array([0, 0, krachten[i]]))
    return momentensom

def calculateVullingT1(arr_volume, arr_tcg, moment_som, arr_vulling_pc, watergewicht):
  """Deze functie berekent het volume van tank 1 aan de hand van het transversale moment door een volume te
  kiezen dat dit moment compenseert. Eerst wordt er op basis van de arrays met de waarden voor het
  volume en het tcg op de bekende vullingsgraden een array met de momenten op die vullingsgraden opgesteld.
  Vervolgens wordt deze array geïnterpoleerd en uitgezet tegenover het volume. Ten slotte wordt de volumewaarde
  die correspondeert met het opgegeven transversale moment (moment_som[0]) bepaald en teruggegeven. Ook wordt
  er een grafiek geplot waarin het volume van tank 1 wordt uitgezet tegen de vullingsgraad."""
  arr_moment = arr_volume*arr_tcg*watergewicht
  f = ip.interp1d(arr_moment,arr_volume, kind="cubic")
  volume_acc = f(moment_som[0])
  #grafiek
  f2 = ip.interp1d(arr_vulling_pc, arr_volume, kind="cubic")
  xnew = np.linspace(arr_vulling_pc[0], arr_vulling_pc[-1], 10000)
  ynew = f2(xnew)
  plt.figure(figsize=(8,5))
  plt.plot(xnew, ynew, linestyle='-', color = "b", label='Tankvolume vs moment Tank 1')
  plt.plot(arr_vulling_pc, arr_volume,'o', color='r')
  plt.xlabel("Vullingspercentage (%)")
  plt.ylabel("Volume (m³)")
  plt.title("Verband tussen vullingspercentage en volume in tank 1")
  plt.legend()
  plt.grid(True)
  plt.show()
  plt.close()
  return volume_acc

def positiesmetkrachtenlijst2(dic_bulk, positie_w_t1, kracht_w_t1, positie_w_t3, kracht_w_t3, h, COB, staalgewicht, plaatdikte_bh, kraan_lcg, SWLMax, dic_hull, plaatdikte_romp,  opwaartse_kracht):
  """
  Het doel van deze functie is twee lijsten te creëeren: een met alle krachten en een met de corresponderende posities. Alleen
  het gewicht van tank 2 wordt nog niet gevraagd als argument, zodat dat met deze lijsten kan worden berekend.
  De krachten lijst bestaat uit floats terwijl de positielijst uit lijsten bestaat. Deze lijsten bevatten steeds drie elementen,
  respectievelijk de lcg, tcg en vcg van de massa (of het COB in het geval van de opdrijvende kracht). Hiervoor wordt er geïtereerd
  over de dictionaries waar de gegevens van de romp en schotten instaan, om daar de oppervlakten en zwaartepunten uit te halen. De
  oppervlakten worden met het staalgewicht en de dikte vermenigvuldigd om de massa te krijgen. Vervolgens worden de zwaartekrachten
  van de vullingen van tank 1 en tank 3 toegevoegd en de opdrijvende kracht, alsook hun zwaartepunten. Tot slot worden de gegevens
  kraan toegevoegd door middel van de kraanfunctie, die de zwaartekracht en zwaartepunt van de kraan bepaalt.
  """
  krachten = []
  positie = []
  for x in dic_bulk:
    krachten.append(-dic_bulk[x][0]*staalgewicht*plaatdikte_bh)
    positie.append(dic_bulk[x][1:])
  for x in dic_hull:
    if x == "Transom Area ":
      krachten.append(-dic_hull[x][0]*staalgewicht*plaatdikte_bh)
      positie.append(dic_hull[x][1:])
    else:
      krachten.append(-dic_hull[x][0]*staalgewicht*plaatdikte_romp)
      positie.append(dic_hull[x][1:])
  krachten.append(-kracht_w_t3)
  krachten.append(opwaartse_kracht)
  krachten.append(-kracht_w_t1)
  positie.append(positie_w_t3)
  positie.append(COB)
  positie.append(positie_w_t1)
  krachten2, posities2 = calculateWeightKraan(krachten, positie, h, kraan_lcg, SWLMax)
  return krachten2, posities2

def calculateKrachtensom1(krachten):
    """
    deze functie maakt van een lijst met krachten een float die gelijk is aan de som van al die krachten en geeft deze terug
    """
    krachtensom = 0
    for i in range(len(krachten)):
        krachtensom += np.sum(np.array([0,0, krachten[i]]), axis=0, keepdims=True)
    return krachtensom

def calculateVullingT2(Krachtensom, watergewicht):
    """
    Deze functie genereert uit de resultante kracht het volume van het water in tank twee en geeft deze terug. Beide deze
    variabelen zijn floats.
    """
    Volume_T2 = Krachtensom / watergewicht
    return Volume_T2

def calculateKrachtsom2(krachtsom1, dic, plaatdikte, staalgewicht):
  """
  Deze functie neemt de eerste krachtsom en voegt hier het gewicht van de bulkheads van tank 2 aan toe.
  """
  oppervlakte_bh_tank2 = 0
  for x in dic:
    oppervlakte_bh_tank2 += dic[x][0]
  tweedekrachtsom = krachtsom1 + (oppervlakte_bh_tank2*plaatdikte*staalgewicht)
  return tweedekrachtsom

def lcgTank2(momentensom2,krachtensom2):
    """
    deze functie haalt uit het het resultante moment rond de y-as en de resultante kracht de arm van tank 2. De resultante kracht
    in dit geval is het totale gewicht van tank 2 (dus water+tankschotten), berekend door alle andere gewichten bij elkaar op te
    tellen en daar de opdrijvende kracht van af te trekken.
    """
    lcgt2 = momentensom2[1]/-krachtensom2
    return lcgt2

def calculateIttanks(Dictionary_Traagheidsmoment1, Dictionary_Traagheidsmoment2, Dictionary_Traagheidsmoment3, Dictionary_vulling1, Dictionary_vulling2, Dictionary_vulling3, tankvulling1, tankvulling2, tankvulling3):
    """
    Deze functie neemt als arguments arrays met de traagheidsmomenten op verschillende volumes en arrays met de correspoderende
    volumes van elke aan. Ook neemt hij de werkelijke volumes per tank aan. Vervolgens wordt met interpolatie het werkelijke
    traagheidsmoment van het wateroppervlak per tank bepaald. Deze worden bij elkaar opgeteld en teruggegeven als float.
    (de lokale variabelen heten "dictionary" omdat de arrays in dictionaries staan, maar de daadwerkelijk gevraagde inputs zijn
    arrays)
    """
    TraagheidsmomentT1_dmv_tankfillingper = ip.interp1d(Dictionary_vulling1, Dictionary_Traagheidsmoment1, kind='cubic')
    TraagheidsmomentT2_dmv_tankfillingper = ip.interp1d(Dictionary_vulling2, Dictionary_Traagheidsmoment2, kind='cubic')
    TraagheidsmomentT3_dmv_tankfillingper = ip.interp1d(Dictionary_vulling3, Dictionary_Traagheidsmoment3, kind='cubic')
    Traagheidsmoment1x = TraagheidsmomentT1_dmv_tankfillingper(tankvulling1)
    Traagheidsmoment2x = TraagheidsmomentT2_dmv_tankfillingper(tankvulling2)
    Traagheidsmoment3x = TraagheidsmomentT3_dmv_tankfillingper(tankvulling3)
    SIt = Traagheidsmoment1x + Traagheidsmoment2x + Traagheidsmoment3x
    return SIt

def removeBuoyantForce(lijst_positie, lijst_krachten, Center_buoyancy, kracht_opdrijvend):
  """
  Deze functie haalt de COB en de opdrijvende kracht uit de lijsten met alle massa's en alle posities,
  zodat hiermee de totale zwaartepunten kunnen worden bepaald.
  """
  lijst_positie = [arr for arr in lijst_positie if not np.array_equal(arr, Center_buoyancy)]
  for element in lijst_krachten:
    if element == kracht_opdrijvend:
      lijst_krachten.remove(element)
      break
  return lijst_positie, lijst_krachten

def calculateZwaartepuntschip(posities, krachten):
    """
    Deze functie berekent het totale zwaartepunt van het schip op basis van lijsten met de zwaartekrachten en zwaartepunten van
    elk onderdeel van het schip. De individuele zwaartekrachten en producten van zwaartekrachten met hun locatie worden in een for-
    loop bij elkaar opgeteld. Vervolgens wordt elk van de  gedeeld door de totale zwaartekracht gedeeld om het lcg, tcg, en
    vcg te bepalen. Als output geeft de functie een tuple van drie floats.
    """
    krachtenopgeteld = 0
    lcg_krachten_en_posities_vermenigvuldigd = 0
    tcg_krachten_en_posities_vermenigvuldigd = 0
    vcg_krachten_en_posities_vermenigvuldigd = 0
    for i in range(len(krachten)):
        if len(krachten) != len(posities):
            print("Error, ongelijke hoeveelheden krachten en posities")
            return None
        else:
            x = posities[i][0]
            y = posities[i][1]
            z = posities[i][2]
            krachtenopgeteld += krachten[i]
            lcg_krachten_en_posities_vermenigvuldigd += x*krachten[i]
            tcg_krachten_en_posities_vermenigvuldigd += y*krachten[i]
            vcg_krachten_en_posities_vermenigvuldigd += z*krachten[i]
    lcg = lcg_krachten_en_posities_vermenigvuldigd/krachtenopgeteld
    tcg = tcg_krachten_en_posities_vermenigvuldigd/krachtenopgeteld
    vcg = vcg_krachten_en_posities_vermenigvuldigd/krachtenopgeteld
    return lcg, tcg, vcg

def calculateG_M(onderwatervolume, SIt, KG, KB, It):
    """
    Deze functie bepaalt het G'M op basis van de inputs onderwatervolume, de som van de traagheidsmomenten van de wateroppervlakten
    van de ballastanks, KG, KB en het traagheidsmoment van de waterlijn. Eerst wordt de GM bepaald, vervolgens wordt de
    vrijevloeistofcorrectie toegepast. Bij de vrijevloeistofcorrectie is ervan uitgegaan dat de dichtheid van de water in de
    ballasttanks gelijk zijn aan het water verplaatst door de romp. Alle inputs horen floats te zijn, net als return g'm.
    """
    gm = KB - KG + It/onderwatervolume
    gnulg = SIt/onderwatervolume
    g_m = gm - gnulg
    return g_m
# Begin deelopdracht 8
def opwaartseKracht(dictio_CSA, lengte_schip):
    oppervlakte = dictio_CSA[" crossarea_in_m2"]
    lps = dictio_CSA["x_in_m"]
    oppervlakteInterp = ip.interp1d(lps, oppervlakte, kind='cubic', fill_value='extrapolate')
    oppervlakte_cm = oppervlakteInterp(lengte_schip)
    Onderwater_volume = []
    for i in range(len(oppervlakte_cm)-1):
        dx = lengte_schip[i+1]-lengte_schip[i]
        Onderwater_volume.append(oppervlakte_cm[i]*dx)
    Onderwater_volume.append(0)
    opwaartse_kracht_cm = np.array(Onderwater_volume)*WEIGHT_WATER
    funcPlotFill(lengte_schip, -opwaartse_kracht_cm, "Lengte van het schip (L) [m]", "Opwaartse kracht (p) in [N]", "De opwaartse kracht (p) in [N] over de lengte van het schip (L) [m]", "Opwaartse kracht (p) in [N]", 'b')
    return opwaartse_kracht_cm

def traagheidsmomentOverLengte(traagheidsmoment_csa_shell, Lengte_schip_csa_shell, lengte_schip):
    Interpoleer_naar_cm = ip.interp1d(Lengte_schip_csa_shell, traagheidsmoment_csa_shell)
    traagheidsmoment_csa_shell_cm = Interpoleer_naar_cm(lengte_schip)
    funcPlotFill(lengte_schip, traagheidsmoment_csa_shell_cm, "Lengte van het schip (L) [m]", "Traagheidsmoment I [m4]", "Het traagheidsmoment I [m4] over de lengte van het schip L [m]", "Traagheidsmoment I [m4]", 'purple')
    return traagheidsmoment_csa_shell_cm

def ballastwaterKracht(dic_tank, dic_tank_2, dic_tank_3, lengte_schip):
    donnot = np.array([0.0])
    oppervlakte1 = dic_tank[" crossarea_in_m2"]
    lps1 = dic_tank["x_in_m"]
    oppervlakteInterp1 = ip.interp1d(lps1, oppervlakte1, kind='cubic', fill_value=donnot)
    oppervlakte1_cm = oppervlakteInterp1(lengte_schip)
    Water_volume1 = []
    oppervlakte2 = dic_tank_2[" crossarea_in_m2"]
    lps2 = dic_tank_2["x_in_m"]
    oppervlakteInterp2 = ip.interp1d(lps2, oppervlakte2, kind='cubic', fill_value=donnot)
    oppervlakte2_cm = oppervlakteInterp2(lengte_schip)
    Water_volume2 = []
    oppervlakte3 = dic_tank_3[" crossarea_in_m2"]
    lps3 = dic_tank_3["x_in_m"]
    oppervlakteInterp3 = ip.interp1d(lps3, oppervlakte3, kind='cubic', fill_value=donnot)
    oppervlakte3_cm = oppervlakteInterp3(lengte_schip)
    Water_volume3 = []
    for i in range(len(oppervlakte1_cm)-1):
        dx1 = lengte_schip[i+1]-lengte_schip[i]
        Water_volume1.append(oppervlakte1_cm[i]*dx1)
    for i in range(len(oppervlakte2_cm)-1):
        dx2 = lengte_schip[i+1]-lengte_schip[i]
        Water_volume2.append(oppervlakte2_cm[i]*dx2)
    for i in range(len(oppervlakte3_cm)-1):
        dx3 = lengte_schip[i+1]-lengte_schip[i]
        Water_volume3.append(oppervlakte3_cm[i]*dx3)
    Water_volume1.append(0)
    Water_volume2.append(0)
    Water_volume3.append(0)
    Neerwaartse_kracht1 = np.array(Water_volume1)*WEIGHT_WATER
    Neerwaartse_kracht2 = np.array(Water_volume2)*WEIGHT_WATER
    Neerwaartse_kracht3 = np.array(Water_volume3)*WEIGHT_WATER
    Neerwaartse_kracht_cm = Neerwaartse_kracht1 + Neerwaartse_kracht2 + Neerwaartse_kracht3
    funcPlotFill(lengte_schip, Neerwaartse_kracht_cm, "Lengte van het schip (L) [m]", "Neerwaartse kracht (Ballast) [N]", "De verdeelde belasting van het ballastwater over de lengte van het schip", "Ballast belasting [N]", 'r')
    return -Neerwaartse_kracht_cm

def dwarskracht(q_x, lengte_schip):
    dwarskracht = cumtrapz(q_x, lengte_schip, initial=0)
    dwarskracht[0]= 0
    dwarskracht[-1]= 0
    funcPlotFill(lengte_schip, dwarskracht, "Lengte van het schip L [m]", "Dwarskracht V(x) [N]", "De dwarskracht V(x) [N] over de lengte van het schip L [m]", "Dwarskracht V(x)", 'orange')
    return dwarskracht

def buigendMoment(F_x, lengte_schip):
    buigend_moment = cumtrapz(F_x, lengte_schip, initial=0)
    buigend_moment[0]= 0
    buigend_moment[-1]= 0
    funcPlotFill(lengte_schip, buigend_moment, "Lengte van het schip L [m]", "Buigend moment M(x) [Nm]", "Het buigend moment M(x) [Nm] over de lengte van het schip L [m]", "Buigend moment M(x)", 'yellow')
    return buigend_moment

# door het gereduceerde moment de integreren krijg je de verdraaiing accent (phi accent)
def hoekverdraaiingAcc(buigend_moment_uitkomst, lengte_schip):
    phi_accent = cumtrapz(lengte_schip, buigend_moment_uitkomst, initial=0)
    phi_accent[0]=0
    funcPlotFill(lengte_schip, phi_accent, "Lengte van het schip L [m]", "φ(x)' [deg]", "De hoekverdraaiing in graden φ(x)' [deg] over de lengte van het schip L [m]", "De hoekverdraaiing φ(x)' [deg]", 'green')
    return phi_accent


# door de verdraaing accent (phi accent) te integreren krijg je de doorbuiging accent (w')

def doorbuigingAcc(phi_accent, lengte_schip):
    w_acc = cumtrapz(lengte_schip, phi_accent, initial =0 )
    w_acc[0]=0
    funcPlotFill(lengte_schip, w_acc, "Lengte van het schip L [m]", "Doorbuiging w'(x) [m]", "Doorbuiging w'(x) [m] over de lengte van het schip L [m]", "Doorbuiging w'(x) [m]", 'brown')
    return w_acc

#phi
def hoekverdraaiing(phi_acc, lengte_schip, C):
    phi = phi_acc + C
    funcPlotFill(lengte_schip, phi, "Lengte van het schip L [m]", "φ(x) [deg]", "Relatieve hoek in graden over de lengte van het schip", "Hoekverdraaiing φ(x) [deg]", "y")
    return phi

#w
def doorbuiging(w_acc, lengte_schip, C):
    w = w_acc + C
    w[0]=0
    w[-1]=0
    funcPlotFill(lengte_schip, w, "Lengte van het schip L [m]", "Relatieve Doorbuiging w(x) [m]", "De relatieve doorbuiging over de lengte van het schip", "Doorbuiging w(x) [m]", "b")
    return w
# x_plot, y_plot, x_naam, y_naam, titel_naam, functie_naam

def parabolischProfielTP(zwaartepunt_tp, totaal_kracht, lengte_in_cm, STRAAL_TP):
    """de input van deze functie is het zwaartepunt van één Transition Piece, de totale kracht van alle transition pieces
    en een array over de lengte van het schip die te vinden is in de main. dan maakt hij eerst het bereik waar het parabolisch profiel van de TP's
    te vinden is. dan maakt hij van de fysieke positie een index in een array. in het 2de deel van de functie bereidt hij parabool waarden voor.
    x_norm zijn dan de genormaliseerde afstanden tov het zwaartepunt. in het laatste deel maakt hij het parabolisch profiel en alle negatieve waardes op 0. 
    en dan zorgt hij ervoor dat de som gelijk is aan de totale kracht."""
    start = lengte_in_cm[0]
    eind = lengte_in_cm[-1]
    begin = max(zwaartepunt_tp - STRAAL_TP, start)
    eind = min(zwaartepunt_tp + STRAAL_TP, eind)
    idx_begin = int(begin - start)
    idx_eind = int(eind - start)

    bereik = np.arange(idx_begin, idx_eind + 1)
    afstanden = (bereik + start) - zwaartepunt_tp
    x_norm = afstanden / STRAAL_TP

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
  fg_per_cm = fg_totaal/50
  arr_gewicht = np.zeros(len(arr_lengte))
  for i in range(50):
    arr_gewicht[i] += fg_per_cm
  return -arr_gewicht

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
  f = ip.interp1d(x,w)
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
        krachtverdeling += parabolischProfielKraan(pos, massas[0], lengte_in_cm, straal)
    return krachtverdeling


def eersteMoment(d3, bouyant_volume, transom_bhd_thickness, dha, rest_thickness, kraan_lcg, cob, h, dbh1):
    #Tank 3: er wordt een waarde gekozen voor het volume van tank 3. Vervolgens wordt hiervan het gewicht en
    #het zwaartepunt bepaald
    volume_t3 = d3["vol_3"][3]
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
    print("De langscheepse positie van tank 2 moet zijn:")
    print(positie_t2[0])
    return volume_t2, kracht_t2, positie_t2

def stabilitietsMain(versienummer, transom_bhd_thickness, rest_thickness, kraan_lcg, d1, d2, d3, dbh1, dbh2, dbh, msp, dha, dic_Shell_CSA, dic_csa_tank1, dic_csa_tank2, dic_csa_tank3, cob, h, bouyant_volume, length_schip, it, l_shell, i_x_shell, B_CSA2, resistance):
    # De eerste momentensom voor het dwarsscheepse momentenevenwicht    
    momentensom1_, kracht_t3, locatie_t3, volume_t3 = eersteMoment(d3, bouyant_volume, transom_bhd_thickness, dha, 
                                                                   rest_thickness, kraan_lcg, cob, h, dbh1)
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
    print("De G_M is:")
    print(G_M)
    Rtot_14knp = str(resistance.loc[8, '  Rtot [N]'])
    entrance_angle = 30
    output_1(versienummer, str(entrance_angle), Rtot_14knp, G_M, 20, msp["Loa  [m]"], msp["B [m]"], h, msp["T moulded [m]"], 
             0, 0, STAALGEWICHT, WATERDICHTHEID, calculateKrachtensom1(krachten3)[0], lcg_schip, tcg_schip, vcg_schip, 
             bouyant_volume*WEIGHT_WATER, cob[0], cob[1], cob[2], 
             calculateKrachtensom1(krachten3)[0]+(bouyant_volume*WEIGHT_WATER), (calculateKrachtensom1(krachten3)[0]*(lcg_schip - cob[0])), 
             (calculateKrachtensom1(krachten3)[0]*(tcg_schip - cob[1])), 16, -WEIGHT_TRANSITION_PIECE*GRAVITATION_CONSTANT, 40, -2, h + 10, versienummer)
    vul1, vul2, vul3 = vullingPercFunc(d1, d2, d3, momentensom1_, volume_t2, volume_t3)
    return

def dic_csa(df):
        """
        Deze functie zet de df van de bouyant_csa om in een dictionary.
        
        Parameters
        ----------
        df : TYPE: dataframe
            DESCRIPTION.
            
        Returns
        -------
        dic : TYPE: dictionary
        DESCRIPTION.

        """
        dic = {}
        dic["x_in_m".format(df.iloc[20,0])] = df.iloc[:,0].to_numpy()
        dic[" crossarea_in_m2".format(df.iloc[20,1])] = df.iloc[:,1].to_numpy()
        return dic

def itereren(versienummers):
    for i in versienummers:
        versienummer = i
        print("Dit is versie:")
        print(versienummer)
        d1, d2, d3, dbh1, dbh2, dbh, msp, dha, dic_Shell_CSA, dic_csa_tank1, dic_csa_tank2, dic_csa_tank3, resistance, df_csa = importGrasshopperFiles(versienummer)
        print("De weerstand op 14 knopen is:")
        print(resistance.loc[8, '  Rtot [N]'])
        cob = msp["COB [m]"]
        transom_bhd_thickness = 0.010 # m
        rest_thickness = 0.020 # m
        h = float(msp["H [m]"])
        bouyant_volume = float(msp["Buoyant Volume [m3]"])
        length_schip = float(msp["Loa  [m]"])
        it = float(msp["Inertia WPA around COF [m4]"][0])
        l_shell = dic_Shell_CSA["X [m]"]
        i_x_shell = dic_Shell_CSA["INERTIA_X[m4]"]
        B_CSA2 = dic_csa(df_csa)
        stabilitietsMain(versienummer, transom_bhd_thickness, rest_thickness, kraan_lcg, d1, d2, d3, dbh1, dbh2, dbh, msp, dha, dic_Shell_CSA, dic_csa_tank1, dic_csa_tank2, dic_csa_tank3, cob, h, bouyant_volume, length_schip, it, l_shell, i_x_shell, B_CSA2, resistance)
    return None

dingen = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])

itereren(dingen)
