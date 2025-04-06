# -*- coding: utf-8 -*-
"""main_functie_n.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1lW_Rbh4Vg4WO8VRZGbDbs0z4qzZ_RaCS
"""

from bibliotheek import *
import matplotlib.pyplot as plt
from schip_functies import *
from output_1 import output_1
from output_kraan import output_kraan
# Begin Deelopdracht 7
#Tank 3: er wordt een waarde gekozen voor het volume van tank 3. Vervolgens wordt hiervan het gewicht en
#het zwaartepunt bepaald
volume_t3 = d3["vol_3"][4]+643
kracht_t3 = volume_t3*WEIGHT_WATER
locatie_t3 = interpolerenLocatie(d3, volume_t3, 3)
#Tank 1: om de vulling van tank 1 te bepalen worden alle momenten bij elkaar opgeteld. Eerst worden er lijsten
#met de gewichten en aangrijpingspunten van de zwaartekrachten van alle massa's opgesteld met behulp van de
#functie "positiesmetkrachtenlijst2". Vervolgens worden alle momenten bij elkaar opgeteld met de functie
#"momentensom1". Voor meer informatie over deze functies, zie de docstrings in de functiebestanden.
krachten, posities = positiesmetkrachtenlijst1(dbh1, locatie_t3, kracht_t3, H, COB, WEIGHT_STAAL,
                                               transom_bhd_thickness, kraan_lcg, swlmax, dha, rest_thickness,
                                               calculateOpdrijvendeKracht(WEIGHT_WATER, buoyant_volume))
momentensom1_ = calculateMomentensom(posities, krachten)

#Tank 1: op basis van het berekende transversale moment wordt de vulling en gewicht van de vulling van het water
#in tank 1 bepaald.
volume_t1 = calculateVullingT1(d1['vol_1'], d1['tcg_1'], momentensom1_, d1['vulling_%_1'][:7],
                               WEIGHT_WATER)
kracht_t1 = volume_t1*WEIGHT_WATER
locatie_t1 = interpolerenLocatie(d1, volume_t1, 1)
#Tank 2: om het nieuwe krachtevenwicht en het longitudinale momentevenwicht te bepalen moeten
#het gewicht en zwaartepunt van het water in tank 1 worden toegevoegd aan de lijsten met krachten en posities.
#Dit wordt gedaan met de functie "positiemetkrachtenlijst1". Op basis van deze lijsten wordt de vulling en
#het gewicht van tank 2 bepaald.
krachten2, posities2 = positiesmetkrachtenlijst2(dbh, locatie_t1, kracht_t1, locatie_t3, kracht_t3, H, COB,
                                                 WEIGHT_STAAL, transom_bhd_thickness, kraan_lcg, swlmax, dha,
                                                 rest_thickness, calculateOpdrijvendeKracht(WEIGHT_WATER, buoyant_volume))
krachtensom = calculateKrachtensom1(krachten2)
volume_t2 = calculateVullingT2(krachtensom, WEIGHT_WATER)[0]
kracht_t2 = volume_t2*WEIGHT_WATER
#Tank 2: voor het longitudinale evenwicht is er een nieuwe momentensom nodig, waar wel de vulling van tank 1
#is inbegrepen maar niet de tankschotten van tank 2. De functie momentensom2 voegt de momenten veroorzaakt
#door de vulling van tank 1 toe aan de eerdere momentensom. Vervolgens wordt de ligging van het zwaartepunt
#van tank 2 bepaald.
krachten_bh1, posities_bh1 = positiesmetkrachtenlijst2(dbh1, locatie_t1, kracht_t1, locatie_t3, kracht_t3, H, COB,
                                                 WEIGHT_STAAL, transom_bhd_thickness, kraan_lcg, swlmax, dha,
                                                 rest_thickness, calculateOpdrijvendeKracht(WEIGHT_WATER, buoyant_volume))
TweedeMomentensom = calculateMomentensom(posities_bh1, krachten_bh1)
TweedeKrachtensom = calculateKrachtsom2(krachtensom, dbh2, transom_bhd_thickness, WEIGHT_STAAL)
vcgt2 = interpolerenLocatie(d2, volume_t2, 2)[2]
positie_t2 = np.array([lcg_tank2(TweedeMomentensom,TweedeKrachtensom)[0], 0, vcgt2])
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
posities3, krachten3 = removeBuoyantForce(posities2, krachten2, COB, calculateOpdrijvendeKracht(WEIGHT_WATER, buoyant_volume))
lcg_schip, tcg_schip, vcg_schip = calculateZwaartepuntschip(posities3, krachten3)
G_M = calculateG_M(buoyant_volume, SIt, vcg_schip, COB[2], it)
output_1(4, str(entrance_angle), Rtot_14knp, G_M, 20, msp["Loa  [m]"], msp["B [m]"], H, msp["T moulded [m]"], 
         0, 0, STAALGEWICHT, WATERDICHTHEID, calculateKrachtensom1(krachten3)[0], lcg_schip, tcg_schip, vcg_schip, 
         buoyant_volume*WEIGHT_WATER, COB[0], COB[1], COB[2], 
         calculateKrachtensom1(krachten3)[0]+(buoyant_volume*WEIGHT_WATER), (calculateKrachtensom1(krachten3)[0]*(lcg_schip - COB[0])), 
         (calculateKrachtensom1(krachten3)[0]*(tcg_schip - COB[1])), 4, -gewicht_transition_piece*g, lcg_tp, tcg_tp, vcg_tp)
output_kraan(swlmax, -gewicht_transition_piece*g, lengte_kraan_fundatie, Draaihoogte_kraan, jib_length, Zwenkhoek, 
             Giekhoek, LCG_TP, TCG_TP, VCG_TP, LCG_kraanhuis, TCG_kraanhuis, VCG_kraanhuis, LCG_kraanboom, TCG_kraanboom, 
             VCG_kraanboom, LCG_heisgerei, TCG_heisgerei, VCG_heisgerei)

momentdic = d1['vol_1'] * d1['tcg_1'] * WEIGHT_WATER
vulperc1dic = d1['vulling_%_1'][:7]
vulperc1ip = ip.interp1d(momentdic,vulperc1dic, kind = "cubic")
vulperc1 = vulperc1ip(momentensom1_[0])
vulperc2ip = ip.interp1d(d2['vol_2'], d2['vulling_%_2'][:7], kind = "cubic")
vulperc2 = vulperc2ip(volume_t2)
vulperc3ip = ip.interp1d(d3['vol_3'], d3['vulling_%_3'][:7], kind = "cubic")
vulperc3 = vulperc3ip(volume_t3)
# Eind deelopdracht 7
# Begin deelopdracht 8
Opwaartse_kracht = Opwaartse_kracht(B_CSA2, g)
I = traagheidsmoment_over_lengte(I_x_shell, L_shell)
I[-1] = 0.0000000000000001 # Anders krijgen we een gedeeld door 0 error bij M/(E*I)
Kracht_Ballast = ballastwater_kracht(dic_csa_tank1, dic_csa_tank2, dic_csa_tank3, g)

q = Kracht_Ballast + Opwaartse_kracht # De netto belasting
lengte_cm = np.linspace(-9, 141, 15000)
plt.plot(lengte_cm, q, color='black', label='Netto load')
plt.fill_between(lengte_cm, q, alpha=0.2, color='black')
plt.xlabel("Lengte van het schip (L) in [m]")
plt.ylabel("Netto verdeelde belasting (q) in [N]")
plt.title("De netto verdeelde belasting")
plt.legend()
plt.grid(True)
plt.show()
plt.close()
V = dwarskracht(q, lengte_cm)

M = Buigend_Moment(V, lengte_cm)

Reduct_M = M/(E*I)

plt.plot(lengte_cm, Reduct_M, color='c', label='Gereduceerde moment')
plt.fill_between(lengte_cm, Reduct_M, alpha=0.2, color='black')
plt.xlabel("Lengte van het schip (L) in [m]")
plt.ylabel("Gereduceerde moment (M/(E*I)) in [Nm]")
plt.title("De netto verdeelde belasting")
plt.legend()
plt.grid(True)
plt.show()
plt.close()

hoekverdraai_accent = hoekverdraaiing_acc(M, lengte_cm)

doorbuig_acc = doorbuiging_acc(hoekverdraai_accent, lengte_cm)

# hoekverdraaing (phi) = phi_accent + C
# Doorbuiging (w) = w_acc +C
# Dus C berekenen:

C = []
for i in range(len(doorbuig_acc)):
    C.append(- (doorbuig_acc[i]/Lengte_schip))

doorbuig = doorbuiging(doorbuig_acc, lengte_cm, C)