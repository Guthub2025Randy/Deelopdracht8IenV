# -*- coding: utf-8 -*-
"""
Created on Tue Mar  4 13:38:41 2025

@author: randy
"""

from bibliotheek import *
from lcg_tcg_vcg_Deelopdracht_7 import locatie_interpoleren
from input_code import *
from bulkheads_splitsen import bulkhead2
from VullingT1functie import Vulling1
from VullingT2functie import VullingT2
from lcg_tank2 import lcg_tank2
from Momentensom1functie import Momentensom1
from Krachtensom1functie import Krachtensom1
from moment_functie import moment
from posities_en_krachten_lijsten import positiesmetkrachtenlijst1, positiesmetkrachtenlijst2
from Kraanfunctie_krachten_en_posities import Kraanfunctie
from Traagheidsmomenten_Ballasttanks_Functie import traagheidsmomenten_ballasttanks
from Zwaartepunt_schip_functie import Zwaartepuntschip
from G_M_Functie import G_M
from opdrijvende_kracht import *

T3Volumevariatie = d3["vol_3"][4]-200
T3Kracht = T3Volumevariatie*Weight_water
locatie_tank3 = locatie_interpoleren(d3, T3Volumevariatie, 3)
Krachten, Posities = positiesmetkrachtenlijst2(dbh1, locatie_tank3, T3Kracht, H, COB, Weight_staal, 
                                               Transom_BHD_Thickness, kraan_lcg, SWLMax, dha, Rest_Thickness, 
                                               opdrijvende_kracht(Weight_water, Buoyant_volume))
Momentensom1 = Momentensom1(Posities,Krachten)
vullingt1 = Vulling1(Momentensom1, d1["inertia_1"], d1["vol_1"][:7])
T1Kracht = vullingt1*Weight_water
locatie_tank1 = locatie_interpoleren(d1, vullingt1, 1)
Krachten2, Posities2 = positiesmetkrachtenlijst1(dbh, locatie_tank1, T1Kracht, locatie_tank3, T3Kracht, H, COB, 
                                                 Weight_staal, Transom_BHD_Thickness, kraan_lcg, SWLMax, dha, 
                                                 Rest_Thickness, opdrijvende_kracht(Weight_water, Buoyant_volume))
krachtensom_input = Krachten2
Krachtensom = Krachtensom1(krachtensom_input)
vullingT2 = VullingT2(Krachtensom)[0]
KrachtT2 = vullingT2*Weight_water
TweedeMomentensom = Momentensom1 + np.cross(np.array(locatie_tank1), np.array([0, 0, -T1Kracht]))
TweedeKrachtensom = Krachtensom + float(dbh["bulkhead_5"][0]*Transom_BHD_Thickness*Staalgewicht) + float(dbh["bulkhead_7"][0]*Transom_BHD_Thickness*Staalgewicht) + float(dbh["bulkhead_8"][0]*Transom_BHD_Thickness*Staalgewicht)
vcgt2 = locatie_interpoleren(d2, vullingT2, 2)[2]
positie_tank2 = np.array([lcg_tank2(TweedeMomentensom,TweedeKrachtensom)[0], 0, vcgt2])
SIt = traagheidsmomenten_ballasttanks(d1["inertia_1"], d2["inertia_2"], d3["inertia_3"], d1["vol_1"], 
                                      d2["vol_2"], d3["vol_3"], vullingt1, vullingT2, T3Volumevariatie)
Krachten2.append(-KrachtT2)
Posities2.append(positie_tank2)
lcg_schip = Zwaartepuntschip(Posities2, Krachten2)[0]
tcg_schip = Zwaartepuntschip(Posities2, Krachten2)[1]
vcg_schip = Zwaartepuntschip(Posities2, Krachten2)[2]
G_M = G_M(Buoyant_volume, SIt, vcg_schip, COB[2], It)





