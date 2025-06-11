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

def calculateOpdrijvendeKracht(gewicht_water, onderwater_volume):
    """
    deze functie berekent de opdrijvende kracht op basis van het onderwatervolume en de dichtheid van water.
    """
    opdrijvende_kracht = gewicht_water * onderwater_volume
    return opdrijvende_kracht

def positiesMetKrachtenLijst1(dictionary_bulkheads, locatie3, kracht3, h, cob, STAALGEWICHT, plaatdikte, kraan_lcg, swlmax, dictionary_hull, plaatdikte2, opdrijvende_kracht, weight_transition_pieces):
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
        krachten.append(float(-value[0]*STAALGEWICHT*plaatdikte))
    for key, value in dictionary_hull.items():
        x = float(value[1])
        y = float(value[2])
        z = float(value[3])
        posities.append(np.array([x, y, z]))
        if key == "Transom Area ":
            krachten.append(float(-value[0]*STAALGEWICHT*plaatdikte))
        else:
            krachten.append(float(-value[0]*STAALGEWICHT*plaatdikte2))
    krachten1, posities1 = calculateWeightKraan(krachten, posities, h, kraan_lcg, swlmax, weight_transition_pieces)
    krachten1.append(float(-kracht3))
    krachten1.append(opdrijvende_kracht)
    posities1.append(locatie3)
    posities1.append(cob)
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

def positiesmetkrachtenlijst2(dic_bulk, positie_w_t1, kracht_w_t1, positie_w_t3, kracht_w_t3, h, cob, staalgewicht, plaatdikte_bh, kraan_lcg, swlmax, dic_hull, plaatdikte_romp,  opwaartse_kracht, weight_transition_pieces):
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
  positie.append(cob)
  positie.append(positie_w_t1)
  krachten2, posities2 = calculateWeightKraan(krachten, positie, h, kraan_lcg, swlmax, weight_transition_pieces)
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

def removeBuoyantForce(lijst_positie, lijst_krachten, center_buoyancy, kracht_opdrijvend):
  """
  Deze functie haalt de COB en de opdrijvende kracht uit de lijsten met alle massa's en alle posities,
  zodat hiermee de totale zwaartepunten kunnen worden bepaald.
  """
  lijst_positie = [arr for arr in lijst_positie if not np.array_equal(arr, center_buoyancy)]
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


def eersteMoment(d3, bouyant_volume, transom_bhd_thickness, dha, rest_thickness, kraan_lcg, cob, dbh1, h, swlmax, weight_transition_pieces):
    #Tank 3: er wordt een waarde gekozen voor het volume van tank 3. Vervolgens wordt hiervan het gewicht en
    #het zwaartepunt bepaald
    volume_t3 = d3["vol_3"][4] - 625
    kracht_t3 = volume_t3*WEIGHT_WATER
    locatie_t3 = interpolerenLocatie(d3, volume_t3, 3)
    #Tank 1: om de vulling van tank 1 te bepalen worden alle momenten bij elkaar opgeteld. Eerst worden er lijsten
    #met de gewichten en aangrijpingspunten van de zwaartekrachten van alle massa's opgesteld met behulp van de
    #functie "positiesmetkrachtenlijst2". Vervolgens worden alle momenten bij elkaar opgeteld met de functie
    #"momentensom1". Voor meer informatie over deze functies, zie de docstrings in de functiebestanden.
    krachten, posities = positiesMetKrachtenLijst1(dbh1, locatie_t3, kracht_t3, h, cob, WEIGHT_STAAL,
                                                   transom_bhd_thickness, kraan_lcg, swlmax, dha, rest_thickness,
                                                   calculateOpdrijvendeKracht(WEIGHT_WATER, bouyant_volume), weight_transition_pieces)
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

def tankTwee(krachten2, dbh1, locatie_t1, kracht_t1, locatie_t3, kracht_t3, h, cob, transom_bhd_thickness, kraan_lcg, swlmax, dha, rest_thickness, bouyant_volume, dbh2, d2, weight_transition_pieces):
    krachtensom = calculateKrachtensom1(krachten2)
    volume_t2 = calculateVullingT2(krachtensom, WEIGHT_WATER)[0]
    kracht_t2 = volume_t2*WEIGHT_WATER
    #Tank 2: voor het longitudinale evenwicht is er een nieuwe momentensom nodig, waar wel de vulling van tank 1
    #is inbegrepen maar niet de tankschotten van tank 2. De functie momentensom2 voegt de momenten veroorzaakt
    #door de vulling van tank 1 toe aan de eerdere momentensom. Vervolgens wordt de ligging van het zwaartepunt
    #van tank 2 bepaald.
    krachten_bh1, posities_bh1 = positiesmetkrachtenlijst2(dbh1, locatie_t1, kracht_t1, locatie_t3, kracht_t3, h, cob,
                                                     WEIGHT_STAAL, transom_bhd_thickness, kraan_lcg, swlmax, dha,
                                                     rest_thickness, calculateOpdrijvendeKracht(WEIGHT_WATER, bouyant_volume), weight_transition_pieces)
    TweedeMomentensom = calculateMomentensom(posities_bh1, krachten_bh1)
    TweedeKrachtensom = calculateKrachtsom2(krachtensom, dbh2, transom_bhd_thickness, WEIGHT_STAAL)
    vcgt2 = interpolerenLocatie(d2, volume_t2, 2)[2]
    positie_t2 = np.array([lcgTank2(TweedeMomentensom,TweedeKrachtensom)[0], 0, vcgt2])
    print("De langscheepse positie van tank 2 moet zijn:")
    print(positie_t2[0])
    return volume_t2, kracht_t2, positie_t2

def stabilitietsMain(versienummer, transom_bhd_thickness, rest_thickness, kraan_lcg, d1, d2, d3, dbh1, dbh2, dbh, msp, dha, dic_shell_csa, dic_csa_tank1, dic_csa_tank2, dic_csa_tank3, cob, h, bouyant_volume, swlmax, weight_transition_pieces, it, entrance_angle, r_14knp, weight_transition_piece, lcg_tp, tcg_tp, vcg_tp, lengte_kraan_fundatie, draaihoogte_kraan, zwenkhoek, giekhoek, jib_length, lcg_kraanhuis, tcg_kraanhuis, vcg_kraanhuis, lcg_kraanboom, tcg_kraanboom, vcg_kraanboom, lcg_heisgerei, tcg_heisgerei, vcg_heisgerei):
    # De eerste momentensom voor het dwarsscheepse momentenevenwicht    
    momentensom1_, kracht_t3, locatie_t3, volume_t3 = eersteMoment(d3, bouyant_volume, transom_bhd_thickness, dha, 
                                                                   rest_thickness, kraan_lcg, cob, dbh1, h, swlmax, weight_transition_pieces)
    #Tank 1: op basis van het berekende transversale moment wordt de vulling en gewicht van de vulling van het water
    #in tank 1 bepaald.
    volume_t1, kracht_t1, locatie_t1 = tankEen(d1, momentensom1_)
    #Tank 2: om het nieuwe krachtevenwicht en het longitudinale momentevenwicht te bepalen moeten
    #het gewicht en zwaartepunt van het water in tank 1 worden toegevoegd aan de lijsten met krachten en posities.
    #Dit wordt gedaan met de functie "positiemetkrachtenlijst1". Op basis van deze lijsten wordt de vulling en
    #het gewicht van tank 2 bepaald.
    krachten2, posities2 = positiesmetkrachtenlijst2(dbh, locatie_t1, kracht_t1, locatie_t3, kracht_t3, h, cob,
                                                     WEIGHT_STAAL, transom_bhd_thickness, kraan_lcg, swlmax, dha,
                                                     rest_thickness, calculateOpdrijvendeKracht(WEIGHT_WATER, bouyant_volume), weight_transition_pieces)
    volume_t2, kracht_t2, positie_t2 = tankTwee(krachten2, dbh1, locatie_t1, kracht_t1, locatie_t3, kracht_t3, h, cob, transom_bhd_thickness, 
                                                kraan_lcg, swlmax, dha, rest_thickness, bouyant_volume, dbh2, d2, weight_transition_pieces)
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
    print("De G_M van het schip is:")
    print(G_M)
    vul1, vul2, vul3 = vullingPercFunc(d1, d2, d3, momentensom1_, volume_t2, volume_t3)
    output1(versienummer, str(entrance_angle), r_14knp, G_M, 20, msp["Loa  [m]"], msp["B [m]"], h, msp["T moulded [m]"], 
            0, 0, STAALGEWICHT, WATERDICHTHEID, calculateKrachtensom1(krachten3)[0], lcg_schip, tcg_schip, vcg_schip, 
            bouyant_volume*WEIGHT_WATER, cob[0], cob[1], cob[2], 
            calculateKrachtensom1(krachten3)[0]+(bouyant_volume*WEIGHT_WATER), (calculateKrachtensom1(krachten3)[0]*(lcg_schip - cob[0])), 
            (calculateKrachtensom1(krachten3)[0]*(tcg_schip - cob[1])), 4, -weight_transition_piece*GRAVITATION_CONSTANT, lcg_tp, tcg_tp, vcg_tp, 0o3)
    outputKraan(swlmax, -weight_transition_piece*GRAVITATION_CONSTANT, lengte_kraan_fundatie, draaihoogte_kraan, jib_length, zwenkhoek, 
                giekhoek, lcg_tp, tcg_tp, vcg_tp, lcg_kraanhuis, tcg_kraanhuis, vcg_kraanhuis, lcg_kraanboom, tcg_kraanboom, 
                vcg_kraanboom, lcg_heisgerei, tcg_heisgerei, vcg_heisgerei, 0o3)
    return G_M
