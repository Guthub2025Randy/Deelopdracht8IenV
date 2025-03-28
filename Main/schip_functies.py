# -*- coding: utf-8 -*-
"""schip_functies_n.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/113A52ub1agy3nAValpof8xL2UkiPONII
"""

from bibliotheek import *
from input_code import *

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
    ZwaarteKheis = -SWLMax
    arrayPositieKheis = np.array([kraan_lcg, 8+(32.5*np.cos(np.deg2rad(60))), (H+1+(32.5*np.sin(np.deg2rad(60))))])
    ZwaarteKboom = -SWLMax*0.17
    arrayPositieKboom = np.array([kraan_lcg, 8+(0.5*32.5*np.cos(np.deg2rad(60))), (H+1+(0.5*32.5*np.sin(np.deg2rad(60))))])
    ZwaarteKhuis = -SWLMax*0.34
    arrayPositieKhuis = np.array([kraan_lcg, 8, H+1])
    ZwaarteWindmolen = -9025200
    arrayPositieWindmolen = np.array([kraan_lcg, -2, H+10])
    Posities.append(arrayPositieKheis)
    Krachten.append(ZwaarteKheis)
    Posities.append(arrayPositieKboom)
    Krachten.append(ZwaarteKboom)
    Posities.append(arrayPositieKhuis)
    Krachten.append(ZwaarteKhuis)
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
  plt.plot(xnew, ynew, "-", linestyle="-", color = "b", label='Tankvolume vs moment Tank 1')
  plt.plot(arr_vulling_pc, arr_volume,'o', color='r')
  plt.xlabel("Vullingspercentage (%)")
  plt.ylabel("Volume (m³)")
  plt.title("Verband tussen vullingspercentage en volume in tank 1")
  plt.legend()
  plt.grid(True)
  plt.show()
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

def lcg_tank2(momentensom2,krachtensom2):
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

def Opwaartse_kracht(dictio_CSA, zwaartekracht):
    oppervlakte = dictio_CSA[" crossarea_in_m2"]
    lps = dictio_CSA["x_in_m"]
    Onderwater_volume = [0]
    for i in range(len(oppervlakte)-1):
        dx = lps[i+1]-lps[i]
        Onderwater_volume.append(((oppervlakte[i]*dx)+(oppervlakte[i+1]*dx))/2)
    opwaartse_kracht = -np.array(Onderwater_volume)*zwaartekracht
    plt.figure(figsize=(8,5))
    plt.plot(lps, opwaartse_kracht, color='b', label='Opwaartse kracht')
    plt.fill_between(lps, opwaartse_kracht, alpha=0.2, color='b')
    plt.xlabel("Lengte van het schip (L) in [m]")
    plt.ylabel("Opwaartse kracht (p) in [N]")
    plt.title("De verdeelde opwaartse kracht")
    plt.legend()
    plt.grid(True)
    return None

