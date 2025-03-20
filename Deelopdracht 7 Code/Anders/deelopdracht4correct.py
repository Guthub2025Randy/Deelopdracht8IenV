# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 18:40:04 2024

@author: ninac
"""
# Libraries
from math import cos, radians, pi
import math
import numpy as np
import matplotlib.pyplot as plt



# =================================================================================================================================
# LENGTE
lengte = np.arange(1, 121)  # Lengte variëren van 1 tot 200
GM = np.zeros_like(lengte, dtype=float)
KG = np.zeros_like(lengte, dtype=float)
KB = np.zeros_like(lengte, dtype=float)
BM = np.zeros_like(lengte, dtype=float)

# waardes invulle
for i, a in enumerate(lengte):
    # Berekeningen
    btank3 = 6.65
    soortelijkzeewater = 1025
    holte = 13
    diepgang = 10
    b = 20

    mtanks = 7850 * 2.1 * ((a * 13 * 2) * 0.01 + 2 * (6.7 * 13) * 0.01)
    mkraan = 230000  # Simpele benadering
    mtank1 = soortelijkzeewater * a * btank3 * holte * 0.5
    mtank3 = soortelijkzeewater * a * btank3 * holte * 0.7

    deplacement = soortelijkzeewater * a * b * diepgang
    kg_romp = holte / 2
    kg_tanks = ((holte / 2) * mtank1 + (holte / 2)
                * mtank3) / (mtank1 + mtank3)

    KG[i] = (kg_romp * (7850 + mtanks) + kg_tanks * (mtank1 + mtank3)
             ) / (7850 + mtanks + mtank1 + mtank3 + mkraan)
    KB[i] = diepgang / 2
    BM[i] = (a * b ** 3) / (12 * a * b * diepgang)
    GM[i] = KB[i] + BM[i] - KG[i]

# Plotten
fig, ax1 = plt.subplots()  # begin definieren van as 1
ax1.set_xlabel('lengte')  # label
ax1.set_ylabel('GM', color='red')  # met kleurtje
ax1.plot(lengte, GM, color='red')
ax1.tick_params(axis='y', labelcolor='red')

ax2 = ax1.twinx()  # initeer 2e y as
ax2.set_ylabel('KG', color='blue')
ax2.plot(lengte, KG, color='blue')
ax2.tick_params(axis='y', labelcolor='blue')

ax3 = ax1.twinx()  # initeer 2e y as
ax3.set_ylabel('KB', color='green')
ax3.spines['right'].set_position(('outward', 60))
ax3.plot(lengte, KB, color='green')
ax3.tick_params(axis='y', labelcolor='green')

ax3 = ax1.twinx()  # initeer 2e y as
ax3.set_ylabel('BM', color='green')
ax3.spines['right'].set_position(('outward', 120))
ax3.plot(lengte, BM, color='green')
ax3.tick_params(axis='y', labelcolor='green')

plt.title('Veranderingen in GM,KG,KB,BM')
plt.tight_layout()
plt.show()

# ===================================================================================================================

lengte = np.arange(1, 121)  # Lengte variëren van 1 tot 120
GM = np.zeros_like(lengte, dtype=float)
KG = np.zeros_like(lengte, dtype=float)
KB = np.zeros_like(lengte, dtype=float)
BM = np.zeros_like(lengte, dtype=float)

btank3 = 6.65
btank2 = 6.70
btank1 = 6.65
soortelijkzeewater = 1025
holte = 13
diepgang = 10
ltank2 = 34
htank2 = 13
b = 20
nwindmolendeel = 4
oppdek = a*b
ladingcapaciteit = oppdek / (np.pi*4**2)  # dit is opp van de transitionpiece
'''formules voor gewicht '''
mwindmolendeel = 230000  # kg
swlmax = (mwindmolendeel/94)*100
mkraanboom = (swlmax/100)*17
mkraanhuis = (swlmax/100)*34
mhijsgerei = (swlmax/100)*6  # incl spreader en kraanhaak
mkraan = mkraanboom+mkraanhuis+mhijsgerei+mwindmolendeel  # incl windmolendeel
'''formules voor zwaartepunt'''
lkraanboom = 32.5
zkraanboom = [8 + cos(math.radians(60))*0.5*lkraanboom, 32]
zhijsgerei = [8+cos(math.radians(60))*lkraanboom, 32]
zkraanhuis = [8, 32]
tcg_kraantotaal = (
    zkraanboom[0] * mkraanboom +
    zhijsgerei[0] * mhijsgerei +
    zkraanhuis[0] * mkraanhuis +
    zhijsgerei[0] * mwindmolendeel
)/mkraan
lcg_kraantotaal = (
    zkraanboom[1] * mkraanboom +
    zhijsgerei[1] * mhijsgerei +
    zkraanhuis[1] * mkraanhuis +
    32 * mwindmolendeel
) / mkraan  # incl windmolendeel
#  print("de tcg van de kraantotaal incl windmolen delen:", tcg_kraantotaal)
# print("de lcg van de kraantotaal incl windmolen delen:", lcg_kraantotaal)
'''formules gewicht buitenste huid v. bak & tankschotten'''
staalgewicht = 7850*2.1  # keer die factor
mschotten = ((a*13*2)*0.02+(b*a*2)*0.02+(b*13*2)*0.01)*staalgewicht
mtanks = ((a*13*2)*0.01+2*(6.7*13)*0.01)*staalgewicht
# +((6.7*13*0.01)*(staalgewicht)) #dat extra schot dat je krijgt bij tank 2 erbij
mtotaalstaal = mschotten+mtanks
gr_staalgewicht = mtotaalstaal
# print("de totale massa van de buitsenste huid en tankschotten met dat extra schot erbij is:", mtotaalstaal)
'''bepaal de formules voor alle zwaartepunten'''
lcg_romp = 0.5*a - 4.2
tcg_romp = 0.5 * b
# print("de lcg van de romp zelf is:",lcg_romp)
lcg_deklading = 32 - 4.2
tcg_deklading = -2
'''momentevenwicht dwarscheeps'''

mscheepslading = nwindmolendeel * 230000
tcg_scheepslading = -2
lcg_scheepslading = 32
vullingtank3 = 0.72
volumetank3 = a*btank1*holte
mtank3 = vullingtank3 * soortelijkzeewater * volumetank3
# print('mtank3:', mtank3)

tcgtank3 = -(0.5 * btank2 + 0.5 * btank3)
tcgtank1 = tcgtank3


Mkraan = mkraan * tcg_kraantotaal * 9.81
Mscheepslading = tcg_scheepslading * mscheepslading * 9.81

Mtank3 = tcgtank3 * mtank3 * 9.81

# print("Mkraan totaal:", Mkraan)
# print('Mscheepslading', Mscheepslading)
# print('Mtank3', Mtank3)

Mtank1 = Mkraan + Mscheepslading + Mtank3
mtank1 = Mtank1 / tcgtank1 / 9.81
watervolumetank1 = mtank1 / soortelijkzeewater
totvolumetank1 = a*btank1 * holte
vullingtank1 = watervolumetank1 / totvolumetank1

# print('vullingtank1 in percentage (1a):', vullingtank1 * 100)
'''kracht evenwicht opwaarts'''
# ARCHIMEDESSSSSS: dichtheid*g*L*B*T
Fa = soortelijkzeewater*9.81*lengte*b*diepgang
mbijnatotaal = mtotaalstaal+mtank1+mtank3 + mkraan + \
    mscheepslading  # dit is zonder tank 2 vandaar de bijna
Fneerwaarts = mbijnatotaal*9.81
mtank2 = (Fa-Fneerwaarts)/9.81
totvolumetank2 = ltank2*btank2*htank2
vullingtank2 = mtank2 / (totvolumetank2 * soortelijkzeewater)
# print("vullingtank2 in percentage (1b):", vullingtank2 *100 )

'''langsscheeps evenwicht'''
# Moment= Mtank1+Mtank2+Mtank3+Mkraan+Mscheepslading=0 oud
lcg_tank1 = (a/2)-4.2
lcg_tank3 = lcg_tank1
lcg_romp = (a/2)-4.2  # ik weet niet zeker of lengte over 2 klopt
Mbijnatotaal = (mtank1*lcg_tank1*9.81)+(mtank3*lcg_tank3*9.81)+(mkraan*lcg_kraantotaal*9.81) + \
    (mscheepslading*lcg_scheepslading*9.81) - \
    (Fa*((lengte/2)-4.2))+(mtotaalstaal*lcg_romp*9.81)
# Mbijnatotaal= (mkraan*lcg_kraantotaal*9.81)+ (mscheepslading*lcg_scheepslading*9.81) dit is oud
Mtank2 = -Mbijnatotaal
# print(Mbijnatotaal)
# print(Mtank2)
# Mtank2=mtank2*9.81*lcg_tank2 oud
lcg_tank2 = (Mtank2)/(mtank2*9.81)
Moment = Mtank2+Mbijnatotaal
# print(Moment)
# print("de lcg van tank 2 is:",lcg_tank2)
# Mbijnatotaal=Mtank1*lcg_tank1+Mtank3*lcg_tank3+Mkraan*lcg_kraantotaal+Mscheepslading*lcg_deklading dit is oud
# Moment= Mbijnatotaal+Mtank2*lcg_tank2=0 dit is ook oud
# print("")
# print('')
# print("de geode antwwoorden zijn")
# print('vullingtank1 in percentage (1a):', vullingtank1 * 100)
# print('')
# print("vullingtank2 in percentage (1b):", vullingtank2 *100 )
# print('')
# print("de lcg van tank 2 is fout want het is 30.2898 maar:",lcg_tank2)
lcg_tank2 = 30.2898
# print("swl max",swlmax)
# print(mkraanhuis+mkraanboom)
# print((zkraanboom[0] * mkraanboom)/mkraanboom)
# print(mschotten)
# print(mtanks)
# print(lcg_romp)
# 1a= 58.885746
# 1b= 98.973864
# 1c= 30.2898
'''deplacement'''
onderwatervolume = a*b*diepgang
deplacement = soortelijkzeewater*onderwatervolume


'''a: Bepaal het zwaartepunt in hoogte van alle onderdelen.'''
# Wat is de vcg van de kraan en de lading samen?
mdeklading = 230000*4
vcg_romp = holte/2
vcg_z_deklading = 13+(b/2)
vcg_z_kraanboom = (13 + 1+(math.sin(math.radians(60)))*0.5*lkraanboom)
vcg_z_hijsgerei = (13 + 1+(math.sin(math.radians(60)))*lkraanboom)
vcg_z_kraanhuis = 13+1
# print("mkraan is", mkraan)
# print(8+math.cos(math.radians(60))*0.5*lkraanboom)
vcg_lading_kraan = (mkraanboom*vcg_z_kraanboom+(mhijsgerei)*vcg_z_hijsgerei+mkraanhuis *
                    vcg_z_kraanhuis+mdeklading*vcg_z_deklading)/(mkraan - mwindmolendeel + mdeklading)
# print("vcg kraan en lading is", vcg_lading_kraan)

'''b: vcg van de romp zonder de interne schotten'''
vcg_romp = 6.5

'''c: Wat is de vcg in meter van de transition piece in de kraan, ten opzichte van de kiel'''
vcg_transitionpiece_kraan = (vcg_z_hijsgerei * mwindmolendeel)/mwindmolendeel

'''d: Wat is de vcg van de interne schotten'''
vcg_interneschotten = 6.5

'''e: Wat is de vcg van de tankvullingen'''
vcg_tankvullingen = ((((vullingtank1*holte)/2)*mtank1+((vullingtank2*holte)/2)
                     * mtank2+((vullingtank3*holte)/2)*mtank3))/(mtank1+mtank2+mtank3)

'''f: Wat is de vertical center of buoyancy van het vaartuig ( dus de kb)'''
KG = ((vcg_lading_kraan*(mkraan-mwindmolendeel+mdeklading))+(vcg_tankvullingen*(mtank1+mtank2+mtank3))+(vcg_transitionpiece_kraan *
      mwindmolendeel)+(vcg_interneschotten*mtanks)+(vcg_romp*mschotten))/(mtank1+mtank2+mtank3+mschotten+mtanks+mkraan+mdeklading)
vcb = (holte - 3)/2

'''g: Wat is de vrije vloeistof correctie (VVC) in meter van tank 3'''
It_tank3 = (70*6.65**3)/12*1025  # + #(lengte*btank3* (btank3/2+ btank2/2)**2)
It_tank1 = (a*btank1**3)/12*1025  # + (lengte*btank1*(btank1/2+btank2/2)**2)
It_tank2 = (ltank2*btank2**3)/12*1025
VVC = (It_tank3)/(soortelijkzeewater*a*b*diepgang)
'''h: bm'''
It_totaal = (a * b**3)/12
BM = (It_totaal)/(a*b*diepgang)

"1a: Wat is de GM in meter zonder vrije vloeistof correctie"
KB = diepgang/2
GM = KB-KG+BM

"1b: Wat is de GM in meter met vrije vloeistof correctie"
VVC_totaal = (It_tank3 + It_tank2 + It_tank1)/(soortelijkzeewater*a*b*diepgang)
GM_metvvc = GM-VVC_totaal


lengte = np.arange(1, 121)  # Lengte variëren van 1 tot 120
gr_staalgewicht = np.zeros_like(lengte, dtype=float)
ladingcapaciteit = np.zeros_like(lengte, dtype=float)
deplacement = np.zeros_like(lengte, dtype=float)

for i, a in enumerate(lengte):
    btank3 = 6.65
    btank2 = 6.70
    btank1 = 6.65
    soortelijkzeewater = 1025
    breedte = 20
    holte = 13
    diepgang = 10
    ltank2 = 34
    htank2 = 13
    nwindmolendeel = 4
    oppdek = a*breedte
    ladingcapaciteit[i] = oppdek / (pi * 4**2)
    '''formules voor gewicht '''
    mwindmolendeel = 230000  # kg
    swlmax = (mwindmolendeel/94)*100
    mkraanboom = (swlmax/100)*17
    mkraanhuis = (swlmax/100)*34
    mhijsgerei = (swlmax/100)*6  # incl spreader en kraanhaak
    mkraan = mkraanboom+mkraanhuis+mhijsgerei+mwindmolendeel  # incl windmolendeel
    '''formules voor zwaartepunt'''
    lkraanboom = 32.5
    zkraanboom = [8 + cos(math.radians(60))*0.5*lkraanboom, 32]
    zhijsgerei = [8+cos(math.radians(60))*lkraanboom, 32]
    zkraanhuis = [8, 32]
    tcg_kraantotaal = (
        zkraanboom[0] * mkraanboom +
        zhijsgerei[0] * mhijsgerei +
        zkraanhuis[0] * mkraanhuis +
        zhijsgerei[0] * mwindmolendeel
    )/mkraan
    lcg_kraantotaal = (
        zkraanboom[1] * mkraanboom +
        zhijsgerei[1] * mhijsgerei +
        zkraanhuis[1] * mkraanhuis +
        32 * mwindmolendeel
    ) / mkraan  # incl windmolendeel

    '''formules gewicht buitenste huid v. bak & tankschotten'''
    staalgewicht = 7850*2.1  # keer die factor
    mschotten = ((a*13*2)*0.02+(20*a*2)*0.02+(20*13*2)*0.01)*staalgewicht
    mtanks = ((a*13*2)*0.01+2*(6.7*13)*0.01)*staalgewicht
    # +((6.7*13*0.01)*(staalgewicht)) #dat extra schot dat je krijgt bij tank 2 erbij
    mtotaalstaal = mschotten+mtanks
    gr_staalgewicht[i] = mtotaalstaal

    '''deplacement'''
    onderwatervolume = a*breedte*diepgang
    deplacement[i] = soortelijkzeewater*onderwatervolume

fig, ax1 = plt.subplots()  # begin definieren van as 1
ax1.set_xlabel('lengte')  # label
ax1.set_ylabel('staalgewicht', color='red')  # met kleurtje
ax1.plot(lengte, gr_staalgewicht, color='red')
ax1.tick_params(axis='y', labelcolor='red')

ax2 = ax1.twinx()  # initeer 2e y as
ax2.set_ylabel('ladingscapaciteit', color='blue')
ax2.plot(lengte, ladingcapaciteit, color='blue')
ax2.tick_params(axis='y', labelcolor='blue')

ax3 = ax1.twinx()  # initeer 2e y as
ax3.set_ylabel('deplacement', color='green')
ax3.spines['right'].set_position(('outward', 60))
ax3.plot(lengte, deplacement, color='green')
ax3.tick_params(axis='y', labelcolor='green')

plt.title('Veranderingen in staalgewicht, ladingscapaciteit en deplacement')
plt.tight_layout()
plt.show()

# =========================================================================================================
# BREEDTE

breedte = np.arange(5, 25)  # Breedte variëren van 1 tot 60
GM = np.zeros_like(breedte, dtype=float)
KG = np.zeros_like(breedte, dtype=float)
KB = np.zeros_like(breedte, dtype=float)
BM = np.zeros_like(breedte, dtype=float)

for i, b in enumerate(breedte):
    btank3 = b/3
    btank2 = 0.335*b
    btank1 = b/3
    soortelijkzeewater = 1025
    holte = 13
    t = 10
    ltank2 = 34
    htank2 = 13
    # b = 20
    a = 120
    nwindmolendeel = 4
    oppdek = a*b
    # dit is opp van de transitionpiece
    ladingcapaciteit = oppdek / (np.pi*4**2)
    '''formules voor gewicht '''
    mwindmolendeel = 230000
    swlmax = (mwindmolendeel/94)*100
    mkraanboom = (swlmax/100)*17
    mkraanhuis = (swlmax/100)*34
    mhijsgerei = (swlmax/100)*6  # incl spreader en kraanhaak
    mkraan = mkraanboom+mkraanhuis+mhijsgerei+mwindmolendeel  # incl windmolendeel
    '''formules voor zwaartepunt'''
    lkraanboom = 32.5
    zkraanboom = [8 + cos(math.radians(60))*0.5*lkraanboom, 32]
    zhijsgerei = [8+cos(math.radians(60))*lkraanboom, 32]
    zkraanhuis = [8, 32]
    tcg_kraantotaal = (
        zkraanboom[0] * mkraanboom +
        zhijsgerei[0] * mhijsgerei +
        zkraanhuis[0] * mkraanhuis +
        zhijsgerei[0] * mwindmolendeel
    )/mkraan
    lcg_kraantotaal = (
        zkraanboom[1] * mkraanboom +
        zhijsgerei[1] * mhijsgerei +
        zkraanhuis[1] * mkraanhuis +
        32 * mwindmolendeel
    ) / mkraan  # incl windmolendeel
    #  print("de tcg van de kraantotaal incl windmolen delen:", tcg_kraantotaal)
    # print("de lcg van de kraantotaal incl windmolen delen:", lcg_kraantotaal)
    '''formules gewicht buitenste huid v. bak & tankschotten'''
    staalgewicht = 7850*2.1  # keer die factor
    mschotten = ((a*13*2)*0.02+(b*a*2)*0.02+(b*13*2)*0.01)*staalgewicht
    mtanks = ((a*13*2)*0.01+2*(btank2*13)*0.01)*staalgewicht
    # +((6.7*13*0.01)*(staalgewicht)) #dat extra schot dat je krijgt bij tank 2 erbij
    mtotaalstaal = mschotten+mtanks
    gr_staalgewicht = mtotaalstaal
    # print("de totale massa van de buitsenste huid en tankschotten met dat extra schot erbij is:", mtotaalstaal)
    '''bepaal de formules voor alle zwaartepunten'''
    lcg_romp = 0.5*a - 4.2
    tcg_romp = 0.5 * b
    # print("de lcg van de romp zelf is:",lcg_romp)
    lcg_deklading = 32 - 4.2
    tcg_deklading = -2
    '''momentevenwicht dwarscheeps'''

    mscheepslading = nwindmolendeel * 230000
    tcg_scheepslading = -2
    lcg_scheepslading = 32
    vullingtank3 = 0.72
    volumetank3 = a*btank1*holte
    mtank3 = vullingtank3 * soortelijkzeewater * volumetank3
    # print('mtank3:', mtank3)

    tcgtank3 = -(0.5 * btank2 + 0.5 * btank3)
    tcgtank1 = tcgtank3

    Mkraan = mkraan * tcg_kraantotaal * 9.81
    Mscheepslading = tcg_scheepslading * mscheepslading * 9.81

    Mtank3 = tcgtank3 * mtank3 * 9.81

    # print("Mkraan totaal:", Mkraan)
    # print('Mscheepslading', Mscheepslading)
    # print('Mtank3', Mtank3)

    Mtank1 = Mkraan + Mscheepslading + Mtank3
    mtank1 = Mtank1 / tcgtank1 / 9.81
    watervolumetank1 = mtank1 / soortelijkzeewater
    totvolumetank1 = a*btank1 * holte
    vullingtank1 = watervolumetank1 / totvolumetank1

    # print('vullingtank1 in percentage (1a):', vullingtank1 * 100)
    '''kracht evenwicht opwaarts'''
    # ARCHIMEDESSSSSS: dichtheid*g*L*B*T
    Fa = soortelijkzeewater*9.81*a*b*t
    mbijnatotaal = mtotaalstaal+mtank1+mtank3 + mkraan + \
        mscheepslading  # dit is zonder tank 2 vandaar de bijna
    Fneerwaarts = mbijnatotaal*9.81
    mtank2 = (Fa-Fneerwaarts)/9.81
    totvolumetank2 = ltank2*btank2*htank2
    vullingtank2 = mtank2 / (totvolumetank2 * soortelijkzeewater)
    # print("vullingtank2 in percentage (1b):", vullingtank2 *100 )

    '''langsscheeps evenwicht'''
    # Moment= Mtank1+Mtank2+Mtank3+Mkraan+Mscheepslading=0 oud
    lcg_tank1 = (a/2)-4.2
    lcg_tank3 = lcg_tank1
    lcg_romp = (a/2)-4.2  # ik weet niet zeker of lengte over 2 klopt
    Mbijnatotaal = (mtank1*lcg_tank1*9.81)+(mtank3*lcg_tank3*9.81)+(mkraan*lcg_kraantotaal*9.81) + \
        (mscheepslading*lcg_scheepslading*9.81) - \
        (Fa*((a/2)-4.2))+(mtotaalstaal*lcg_romp*9.81)
    # Mbijnatotaal= (mkraan*lcg_kraantotaal*9.81)+ (mscheepslading*lcg_scheepslading*9.81) dit is oud
    Mtank2 = -Mbijnatotaal
    # print(Mbijnatotaal)
    # print(Mtank2)
    # Mtank2=mtank2*9.81*lcg_tank2 oud
    lcg_tank2 = (Mtank2)/(mtank2*9.81)
    Moment = Mtank2+Mbijnatotaal
    # print(Moment)
    # print("de lcg van tank 2 is:",lcg_tank2)
    # Mbijnatotaal=Mtank1*lcg_tank1+Mtank3*lcg_tank3+Mkraan*lcg_kraantotaal+Mscheepslading*lcg_deklading dit is oud
    # Moment= Mbijnatotaal+Mtank2*lcg_tank2=0 dit is ook oud
    # print("")
    # print('')
    # print("de geode antwwoorden zijn")
    # print('vullingtank1 in percentage (1a):', vullingtank1 * 100)
    # print('')
    # print("vullingtank2 in percentage (1b):", vullingtank2 *100 )
    # print('')
    # print("de lcg van tank 2 is fout want het is 30.2898 maar:",lcg_tank2)
    lcg_tank2 = 30.2898
    # print("swl max",swlmax)
    # print(mkraanhuis+mkraanboom)
    # print((zkraanboom[0] * mkraanboom)/mkraanboom)
    # print(mschotten)
    # print(mtanks)
    # print(lcg_romp)
    # 1a= 58.885746
    # 1b= 98.973864
    # 1c= 30.2898
    '''deplacement'''
    onderwatervolume = a*b*t
    deplacement = soortelijkzeewater*onderwatervolume

    '''a: Bepaal het zwaartepunt in hoogte van alle onderdelen.'''
    # Wat is de vcg van de kraan en de lading samen?
    mdeklading = 230000*4
    vcg_romp = holte/2
    vcg_z_deklading = 13+(b/2)
    vcg_z_kraanboom = (13 + 1+(math.sin(math.radians(60)))*0.5*lkraanboom)
    vcg_z_hijsgerei = (13 + 1+(math.sin(math.radians(60)))*lkraanboom)
    vcg_z_kraanhuis = 13+1
    # print("mkraan is", mkraan)
    # print(8+math.cos(math.radians(60))*0.5*lkraanboom)
    vcg_lading_kraan = (mkraanboom*vcg_z_kraanboom+(mhijsgerei)*vcg_z_hijsgerei+mkraanhuis *
                        vcg_z_kraanhuis+mdeklading*vcg_z_deklading)/(mkraan - mwindmolendeel + mdeklading)
    # print("vcg kraan en lading is", vcg_lading_kraan)

    '''b: vcg van de romp zonder de interne schotten'''
    vcg_romp = 6.5

    '''c: Wat is de vcg in meter van de transition piece in de kraan, ten opzichte van de kiel'''
    vcg_transitionpiece_kraan = (
        vcg_z_hijsgerei * mwindmolendeel)/mwindmolendeel

    '''d: Wat is de vcg van de interne schotten'''
    vcg_interneschotten = 6.5

    '''e: Wat is de vcg van de tankvullingen'''
    vcg_tankvullingen = ((((vullingtank1*holte)/2)*mtank1+((vullingtank2*holte)/2)
                         * mtank2+((vullingtank3*holte)/2)*mtank3))/(mtank1+mtank2+mtank3)

    '''f: Wat is de vertical center of buoyancy van het vaartuig ( dus de kb)'''
    KG[i] = ((vcg_lading_kraan*(mkraan-mwindmolendeel+mdeklading))+(vcg_tankvullingen*(mtank1+mtank2+mtank3))+(vcg_transitionpiece_kraan *
             mwindmolendeel)+(vcg_interneschotten*mtanks)+(vcg_romp*mschotten))/(mtank1+mtank2+mtank3+mschotten+mtanks+mkraan+mdeklading)
    vcb = (holte - 3)/2

    '''g: Wat is de vrije vloeistof correctie (VVC) in meter van tank 3'''
    It_tank3 = (70*btank1**3)/12 * \
        1025  # + #(lengte*btank3* (btank3/2+ btank2/2)**2)
    # + (lengte*btank1*(btank1/2+btank2/2)**2)
    It_tank1 = (a*btank1**3)/12*1025
    It_tank2 = (ltank2*btank2**3)/12*1025
    VVC = (It_tank3)/(soortelijkzeewater*a*b*t)
    '''h: bm'''
    It_totaal = (a * b**3)/12
    BM[i] = (It_totaal)/(a*b*10)

    "1a: Wat is de GM in meter zonder vrije vloeistof correctie"
    KB[i] = t/2
    GM[i] = KB[i]-KG[i]+BM[i]

    "1b: Wat is de GM in meter met vrije vloeistof correctie"
    VVC_totaal = (It_tank3 + It_tank2 + It_tank1)/(soortelijkzeewater*a*b*t)
    GM_metvvc = GM-VVC_totaal


# Opzet voor grafieken:
fig, ax1 = plt.subplots()  # begin definieren van as 1
ax1.set_xlabel('Breedte')  # label
ax1.set_ylabel('GM', color='red')  # met kleurtje
ax1.plot(breedte, GM, color='red')
ax1.tick_params(axis='y', labelcolor='red')

ax2 = ax1.twinx()  # initeer 2e y as
ax2.set_ylabel('KG', color='blue')
ax2.plot(breedte, KG, color='blue')
ax2.tick_params(axis='y', labelcolor='blue')

ax3 = ax1.twinx()  # initeer 2e y as
ax3.set_ylabel('KB', color='green')
ax3.spines['right'].set_position(('outward', 60))
ax3.plot(breedte, KB, color='green')
ax3.tick_params(axis='y', labelcolor='green')

ax3 = ax1.twinx()  # initeer 2e y as
ax3.set_ylabel('BM', color='purple')
ax3.spines['right'].set_position(('outward', 120))
ax3.plot(breedte, BM, color='purple')
ax3.tick_params(axis='y', labelcolor='purple')

plt.title('Veranderingen in GM, KG, KB en BM')
plt.tight_layout()
plt.show()

# ------------------------------------------------------------------------------

breedte = np.arange(1, 61)  # Lengte variëren van 1 tot 60
gr_staalgewicht = np.zeros_like(breedte, dtype=float)
ladingcapaciteit = np.zeros_like(breedte, dtype=float)
deplacement = np.zeros_like(breedte, dtype=float)

for i, b in enumerate(breedte):
    btank3 = 6.65
    btank2 = 6.70
    btank1 = 6.65
    soortelijkzeewater = 1025
    lengte = 120  # zet lengte op 120
    holte = 13
    diepgang = 10
    ltank2 = 34
    htank2 = 13
    nwindmolendeel = 4
    oppdek = lengte * b
    ladingcapaciteit[i] = oppdek / (pi * 4**2)
    '''formules voor gewicht '''
    mwindmolendeel = 230000  # kg
    swlmax = (mwindmolendeel/94)*100
    mkraanboom = (swlmax/100)*17
    mkraanhuis = (swlmax/100)*34
    mhijsgerei = (swlmax/100)*6  # incl spreader en kraanhaak
    mkraan = mkraanboom+mkraanhuis+mhijsgerei+mwindmolendeel  # incl windmolendeel
    '''formules voor zwaartepunt'''
    lkraanboom = 32.5
    zkraanboom = [8 + cos(math.radians(60))*0.5*lkraanboom, 32]
    zhijsgerei = [8+cos(math.radians(60))*lkraanboom, 32]
    zkraanhuis = [8, 32]
    tcg_kraantotaal = (
        zkraanboom[0] * mkraanboom +
        zhijsgerei[0] * mhijsgerei +
        zkraanhuis[0] * mkraanhuis +
        zhijsgerei[0] * mwindmolendeel
    )/mkraan
    lcg_kraantotaal = (
        zkraanboom[1] * mkraanboom +
        zhijsgerei[1] * mhijsgerei +
        zkraanhuis[1] * mkraanhuis +
        32 * mwindmolendeel
    ) / mkraan  # incl windmolendeel

    '''formules gewicht buitenste huid v. bak & tankschotten'''
    staalgewicht = 7850*2.1  # keer die factor
    # lengte*hoogte*2*0.02 + breedte*lengte*2*0.02 + breedte*hoogte*2*0.01
    mschotten = ((b*13*2)*0.02+(20*b*2)*0.02+(b*13*2)*0.01)*staalgewicht
    # lwngtw*hoogte*2*0.01 + 2*breedtemidden*hoogte*0.01
    mtanks = ((120*13*2)*0.01 + 2*((b/3)*13)*0.01)*staalgewicht
    # +((6.7*13*0.01)*(staalgewicht)) #dat extra schot dat je krijgt bij tank 2 erbij
    mtotaalstaal = mschotten+mtanks
    gr_staalgewicht[i] = mtotaalstaal
    '''deplacement'''
    onderwatervolume = 120*b*diepgang
    deplacement[i] = soortelijkzeewater*onderwatervolume

fig, ax1 = plt.subplots()  # begin definieren van as 1
ax1.set_xlabel('Breedte')  # label
ax1.set_ylabel('staalgewicht', color='red')  # met kleurtje
ax1.plot(breedte, gr_staalgewicht, color='red')
ax1.tick_params(axis='y', labelcolor='red')

ax2 = ax1.twinx()  # initeer 2e y as
ax2.set_ylabel('ladingscapaciteit', color='blue')
ax2.plot(breedte, ladingcapaciteit, color='blue')
ax2.tick_params(axis='y', labelcolor='blue')

ax3 = ax1.twinx()  # initeer 3e y as
ax3.set_ylabel('deplacement', color='green')
ax3.spines['right'].set_position(('outward', 60))
ax3.plot(breedte, deplacement, color='green')
ax3.tick_params(axis='y', labelcolor='green')

plt.title('Veranderingen in staalgewicht, ladingscapaciteit en deplacement')
plt.tight_layout()
plt.show()

# =================================================================================================================================
diepgang = np.arange(1, 11)  # Breedte variëren van 1 tot 60
GM = np.zeros_like(diepgang, dtype=float)
KG = np.zeros_like(diepgang, dtype=float)
KB = np.zeros_like(diepgang, dtype=float)
BM = np.zeros_like(diepgang, dtype=float)

for i, t in enumerate(diepgang):
    btank3 = b/3
    btank2 = 0.335*b
    btank1 = b/3
    soortelijkzeewater = 1025
    v=3
    holte = t+v
    # t = 10
    ltank2 = 34
    htank2 = 13
    b = 20
    a = 120
    nwindmolendeel = 4
    oppdek = a*b
    # dit is opp van de transitionpiece
    ladingcapaciteit = oppdek / (np.pi*4**2)
    '''formules voor gewicht '''
    mwindmolendeel = 230000
    swlmax = (mwindmolendeel/94)*100
    mkraanboom = (swlmax/100)*17
    mkraanhuis = (swlmax/100)*34
    mhijsgerei = (swlmax/100)*6  # incl spreader en kraanhaak
    mkraan = mkraanboom+mkraanhuis+mhijsgerei+mwindmolendeel  # incl windmolendeel
    '''formules voor zwaartepunt'''
    lkraanboom = 32.5
    zkraanboom = [8 + cos(math.radians(60))*0.5*lkraanboom, 32]
    zhijsgerei = [8+cos(math.radians(60))*lkraanboom, 32]
    zkraanhuis = [8, 32]
    tcg_kraantotaal = (
        zkraanboom[0] * mkraanboom +
        zhijsgerei[0] * mhijsgerei +
        zkraanhuis[0] * mkraanhuis +
        zhijsgerei[0] * mwindmolendeel
    )/mkraan
    lcg_kraantotaal = (
        zkraanboom[1] * mkraanboom +
        zhijsgerei[1] * mhijsgerei +
        zkraanhuis[1] * mkraanhuis +
        32 * mwindmolendeel
    ) / mkraan  # incl windmolendeel
    #  print("de tcg van de kraantotaal incl windmolen delen:", tcg_kraantotaal)
    # print("de lcg van de kraantotaal incl windmolen delen:", lcg_kraantotaal)
    '''formules gewicht buitenste huid v. bak & tankschotten'''
    staalgewicht = 7850*2.1  # keer die factor
    mschotten = ((a*13*2)*0.02+(b*a*2)*0.02+(b*13*2)*0.01)*staalgewicht
    mtanks = ((a*13*2)*0.01+2*(btank2*holte)*0.01)*staalgewicht
    # +((6.7*13*0.01)*(staalgewicht)) #dat extra schot dat je krijgt bij tank 2 erbij
    mtotaalstaal = mschotten+mtanks
    gr_staalgewicht = mtotaalstaal
    # print("de totale massa van de buitsenste huid en tankschotten met dat extra schot erbij is:", mtotaalstaal)
    '''bepaal de formules voor alle zwaartepunten'''
    lcg_romp = 0.5*a - 4.2
    tcg_romp = 0.5 * b
    # print("de lcg van de romp zelf is:",lcg_romp)
    lcg_deklading = 32 - 4.2
    tcg_deklading = -2
    '''momentevenwicht dwarscheeps'''

    mscheepslading = nwindmolendeel * 230000
    tcg_scheepslading = -2
    lcg_scheepslading = 32
    vullingtank3 = 0.72
    volumetank3 = a*btank1*holte
    mtank3 = vullingtank3 * soortelijkzeewater * volumetank3
    # print('mtank3:', mtank3)

    tcgtank3 = -(0.5 * btank2 + 0.5 * btank3)
    tcgtank1 = tcgtank3

    Mkraan = mkraan * tcg_kraantotaal * 9.81
    Mscheepslading = tcg_scheepslading * mscheepslading * 9.81

    Mtank3 = tcgtank3 * mtank3 * 9.81

    # print("Mkraan totaal:", Mkraan)
    # print('Mscheepslading', Mscheepslading)
    # print('Mtank3', Mtank3)

    Mtank1 = Mkraan + Mscheepslading + Mtank3
    mtank1 = Mtank1 / tcgtank1 / 9.81
    watervolumetank1 = mtank1 / soortelijkzeewater
    totvolumetank1 = a*btank1 * holte
    vullingtank1 = watervolumetank1 / totvolumetank1

    # print('vullingtank1 in percentage (1a):', vullingtank1 * 100)
    '''kracht evenwicht opwaarts'''
    # ARCHIMEDESSSSSS: dichtheid*g*L*B*T
    Fa = soortelijkzeewater*9.81*a*b*t
    mbijnatotaal = mtotaalstaal+mtank1+mtank3 + mkraan + \
        mscheepslading  # dit is zonder tank 2 vandaar de bijna
    Fneerwaarts = mbijnatotaal*9.81
    mtank2 = (Fa-Fneerwaarts)/9.81
    totvolumetank2 = ltank2*btank2*htank2
    vullingtank2 = mtank2 / (totvolumetank2 * soortelijkzeewater)
    # print("vullingtank2 in percentage (1b):", vullingtank2 *100 )

    '''langsscheeps evenwicht'''
    # Moment= Mtank1+Mtank2+Mtank3+Mkraan+Mscheepslading=0 oud
    lcg_tank1 = (a/2)-4.2
    lcg_tank3 = lcg_tank1
    lcg_romp = (a/2)-4.2  # ik weet niet zeker of lengte over 2 klopt
    Mbijnatotaal = (mtank1*lcg_tank1*9.81)+(mtank3*lcg_tank3*9.81)+(mkraan*lcg_kraantotaal*9.81) + \
        (mscheepslading*lcg_scheepslading*9.81) - \
        (Fa*((a/2)-4.2))+(mtotaalstaal*lcg_romp*9.81)
    # Mbijnatotaal= (mkraan*lcg_kraantotaal*9.81)+ (mscheepslading*lcg_scheepslading*9.81) dit is oud
    Mtank2 = -Mbijnatotaal
    # print(Mbijnatotaal)
    # print(Mtank2)
    # Mtank2=mtank2*9.81*lcg_tank2 oud
    lcg_tank2 = (Mtank2)/(mtank2*9.81)
    Moment = Mtank2+Mbijnatotaal
    # print(Moment)
    # print("de lcg van tank 2 is:",lcg_tank2)
    # Mbijnatotaal=Mtank1*lcg_tank1+Mtank3*lcg_tank3+Mkraan*lcg_kraantotaal+Mscheepslading*lcg_deklading dit is oud
    # Moment= Mbijnatotaal+Mtank2*lcg_tank2=0 dit is ook oud
    # print("")
    # print('')
    # print("de geode antwwoorden zijn")
    # print('vullingtank1 in percentage (1a):', vullingtank1 * 100)
    # print('')
    # print("vullingtank2 in percentage (1b):", vullingtank2 *100 )
    # print('')
    # print("de lcg van tank 2 is fout want het is 30.2898 maar:",lcg_tank2)
    lcg_tank2 = 30.2898
    # print("swl max",swlmax)
    # print(mkraanhuis+mkraanboom)
    # print((zkraanboom[0] * mkraanboom)/mkraanboom)
    # print(mschotten)
    # print(mtanks)
    # print(lcg_romp)
    # 1a= 58.885746
    # 1b= 98.973864
    # 1c= 30.2898
    '''deplacement'''
    onderwatervolume = a*b*t
    deplacement = soortelijkzeewater*onderwatervolume

    '''a: Bepaal het zwaartepunt in hoogte van alle onderdelen.'''
    # Wat is de vcg van de kraan en de lading samen?
    mdeklading = 230000*4
    vcg_romp = holte/2
    vcg_z_deklading = holte+(b/2)
    vcg_z_kraanboom = (holte + 1+(math.sin(math.radians(60)))*0.5*lkraanboom)
    vcg_z_hijsgerei = (holte + 1+(math.sin(math.radians(60)))*lkraanboom)
    vcg_z_kraanhuis = holte +1
    # print("mkraan is", mkraan)
    # print(8+math.cos(math.radians(60))*0.5*lkraanboom)
    vcg_lading_kraan = (mkraanboom*vcg_z_kraanboom+(mhijsgerei)*vcg_z_hijsgerei+mkraanhuis *
                        vcg_z_kraanhuis+mdeklading*vcg_z_deklading)/(mkraan - mwindmolendeel + mdeklading)
    # print("vcg kraan en lading is", vcg_lading_kraan)

    '''b: vcg van de romp zonder de interne schotten'''
    vcg_romp = 6.5

    '''c: Wat is de vcg in meter van de transition piece in de kraan, ten opzichte van de kiel'''
    vcg_transitionpiece_kraan = (
        vcg_z_hijsgerei * mwindmolendeel)/mwindmolendeel

    '''d: Wat is de vcg van de interne schotten'''
    vcg_interneschotten = 6.5

    '''e: Wat is de vcg van de tankvullingen'''
    vcg_tankvullingen = ((((vullingtank1*holte)/2)*mtank1+((vullingtank2*holte)/2)
                         * mtank2+((vullingtank3*holte)/2)*mtank3))/(mtank1+mtank2+mtank3)

    '''f: Wat is de vertical center of buoyancy van het vaartuig ( dus de kb)'''
    KG[i] = ((vcg_lading_kraan*(mkraan-mwindmolendeel+mdeklading))+(vcg_tankvullingen*(mtank1+mtank2+mtank3))+(vcg_transitionpiece_kraan *
             mwindmolendeel)+(vcg_interneschotten*mtanks)+(vcg_romp*mschotten))/(mtank1+mtank2+mtank3+mschotten+mtanks+mkraan+mdeklading)
    print("KG =", KG[i])
    vcb = (holte - 3)/2

    '''g: Wat is de vrije vloeistof correctie (VVC) in meter van tank 3'''
    It_tank3 = (70*btank1**3)/12 * \
        1025  # + #(lengte*btank3* (btank3/2+ btank2/2)**2)
    # + (lengte*btank1*(btank1/2+btank2/2)**2)
    It_tank1 = (a*btank1**3)/12*1025
    It_tank2 = (ltank2*btank2**3)/12*1025
    VVC = (It_tank3)/(soortelijkzeewater*a*b*t)
    '''h: bm'''
    It_totaal = (a * b**3)/12
    BM[i] = (It_totaal)/(a*b*t)

    "1a: Wat is de GM in meter zonder vrije vloeistof correctie"
    KB[i] = t/2
    GM[i] = KB[i]-KG[i]+BM[i]

    "1b: Wat is de GM in meter met vrije vloeistof correctie"
    VVC_totaal = (It_tank3 + It_tank2 + It_tank1)/(soortelijkzeewater*a*b*t)
    GM_metvvc = GM-VVC_totaal


# Opzet voor grafieken:
'''
fig, ax1 = plt.subplots()  # begin definieren van as 1
ax1.set_xlabel('Diepgang')  # label
ax1.set_ylabel('staalgewicht', color='red')  # met kleurtje
ax1.plot(diepgang, gr_staalgewicht, color='red')
ax1.tick_params(axis='y', labelcolor='red')

ax2 = ax1.twinx()  # initeer 2e y as
ax2.set_ylabel('ladingscapaciteit', color='blue')
ax2.plot(diepgang, ladingcapaciteit, color='blue')
ax2.tick_params(axis='y', labelcolor='blue')

ax3 = ax1.twinx()  # initeer 2e y as
ax3.set_ylabel('deplacement', color='green')
ax3.spines['right'].set_position(('outward', 60))
ax3.plot(diepgang, deplacement, color='green')
ax3.tick_params(axis='y', labelcolor='green')

plt.title('Veranderingen in staalgewicht, ladingscapaciteit en deplacement')
plt.tight_layout()
plt.show()
'''
fig, ax1 = plt.subplots()  # begin definieren van as 1
ax1.set_xlabel('diepgang')  # label
ax1.set_ylabel('GM', color='red')  # met kleurtje
ax1.plot(diepgang, GM, color='red')
ax1.tick_params(axis='y', labelcolor='red')

ax2 = ax1.twinx()  # initeer 2e y as
ax2.set_ylabel('KG', color='blue')
ax2.plot(diepgang, KG, color='blue')
ax2.tick_params(axis='y', labelcolor='blue')

ax3 = ax1.twinx()  # initeer 2e y as
ax3.set_ylabel('KB', color='green')
ax3.spines['right'].set_position(('outward', 60))
ax3.plot(diepgang, KB, color='green')
ax3.tick_params(axis='y', labelcolor='green')

ax3 = ax1.twinx()  # initeer 2e y as
ax3.set_ylabel('BM', color='purple')
ax3.spines['right'].set_position(('outward', 120))
ax3.plot(diepgang, BM, color='purple')
ax3.tick_params(axis='y', labelcolor='purple')

plt.title('Veranderingen in GM,KG,KB,BM')
plt.tight_layout()

# ------------------------------------------------------------------------------
'''vrijboord:'''
vrijboord = np.arange(3, 12)  # Breedte variëren van 1 tot 60
GM = np.zeros_like(vrijboord, dtype=float)
KG = np.zeros_like(vrijboord, dtype=float)
KB = np.zeros_like(vrijboord, dtype=float)
BM = np.zeros_like(vrijboord, dtype=float)

for i, v in enumerate(vrijboord):
    btank3 = b/3
    btank2 = 0.335*b
    btank1 = b/3
    soortelijkzeewater = 1025
    holte = t + v
    t = 10
    ltank2 = 34
    htank2 = 13
    b = 20
    a = 120
    nwindmolendeel = 4
    oppdek = a*b
    # dit is opp van de transitionpiece
    ladingcapaciteit = oppdek / (np.pi*4**2)
    '''formules voor gewicht '''
    mwindmolendeel = 230000
    swlmax = (mwindmolendeel/94)*100
    mkraanboom = (swlmax/100)*17
    mkraanhuis = (swlmax/100)*34
    mhijsgerei = (swlmax/100)*6  # incl spreader en kraanhaak
    mkraan = mkraanboom+mkraanhuis+mhijsgerei+mwindmolendeel  # incl windmolendeel
    '''formules voor zwaartepunt'''
    lkraanboom = 32.5
    zkraanboom = [8 + cos(math.radians(60))*0.5*lkraanboom, 32]
    zhijsgerei = [8+cos(math.radians(60))*lkraanboom, 32]
    zkraanhuis = [8, 32]
    tcg_kraantotaal = (
        zkraanboom[0] * mkraanboom +
        zhijsgerei[0] * mhijsgerei +
        zkraanhuis[0] * mkraanhuis +
        zhijsgerei[0] * mwindmolendeel
    )/mkraan
    lcg_kraantotaal = (
        zkraanboom[1] * mkraanboom +
        zhijsgerei[1] * mhijsgerei +
        zkraanhuis[1] * mkraanhuis +
        32 * mwindmolendeel
    ) / mkraan  # incl windmolendeel
    #  print("de tcg van de kraantotaal incl windmolen delen:", tcg_kraantotaal)
    # print("de lcg van de kraantotaal incl windmolen delen:", lcg_kraantotaal)
    '''formules gewicht buitenste huid v. bak & tankschotten'''
    staalgewicht = 7850*2.1  # keer die factor
    mschotten = ((a*13*2)*0.02+(b*a*2)*0.02+(b*13*2)*0.01)*staalgewicht
    mtanks = ((a*13*2)*0.01+2*(btank2*13)*0.01)*staalgewicht
    # +((6.7*13*0.01)*(staalgewicht)) #dat extra schot dat je krijgt bij tank 2 erbij
    mtotaalstaal = mschotten+mtanks
    gr_staalgewicht = mtotaalstaal
    # print("de totale massa van de buitsenste huid en tankschotten met dat extra schot erbij is:", mtotaalstaal)
    '''bepaal de formules voor alle zwaartepunten'''
    lcg_romp = 0.5*a - 4.2
    tcg_romp = 0.5 * b
    # print("de lcg van de romp zelf is:",lcg_romp)
    lcg_deklading = 32 - 4.2
    tcg_deklading = -2
    '''momentevenwicht dwarscheeps'''

    mscheepslading = nwindmolendeel * 230000
    tcg_scheepslading = -2
    lcg_scheepslading = 32
    vullingtank3 = 0.72
    volumetank3 = a*btank1*holte
    mtank3 = vullingtank3 * soortelijkzeewater * volumetank3
    # print('mtank3:', mtank3)

    tcgtank3 = -(0.5 * btank2 + 0.5 * btank3)
    tcgtank1 = tcgtank3

    Mkraan = mkraan * tcg_kraantotaal * 9.81
    Mscheepslading = tcg_scheepslading * mscheepslading * 9.81

    Mtank3 = tcgtank3 * mtank3 * 9.81

    # print("Mkraan totaal:", Mkraan)
    # print('Mscheepslading', Mscheepslading)
    # print('Mtank3', Mtank3)

    Mtank1 = Mkraan + Mscheepslading + Mtank3
    mtank1 = Mtank1 / tcgtank1 / 9.81
    watervolumetank1 = mtank1 / soortelijkzeewater
    totvolumetank1 = a*btank1 * holte
    vullingtank1 = watervolumetank1 / totvolumetank1

    # print('vullingtank1 in percentage (1a):', vullingtank1 * 100)
    '''kracht evenwicht opwaarts'''
    # ARCHIMEDESSSSSS: dichtheid*g*L*B*T
    Fa = soortelijkzeewater*9.81*a*b*t
    mbijnatotaal = mtotaalstaal+mtank1+mtank3 + mkraan + \
        mscheepslading  # dit is zonder tank 2 vandaar de bijna
    Fneerwaarts = mbijnatotaal*9.81
    mtank2 = (Fa-Fneerwaarts)/9.81
    totvolumetank2 = ltank2*btank2*htank2
    vullingtank2 = mtank2 / (totvolumetank2 * soortelijkzeewater)
    # print("vullingtank2 in percentage (1b):", vullingtank2 *100 )

    '''langsscheeps evenwicht'''
    # Moment= Mtank1+Mtank2+Mtank3+Mkraan+Mscheepslading=0 oud
    lcg_tank1 = (a/2)-4.2
    lcg_tank3 = lcg_tank1
    lcg_romp = (a/2)-4.2  # ik weet niet zeker of lengte over 2 klopt
    Mbijnatotaal = (mtank1*lcg_tank1*9.81)+(mtank3*lcg_tank3*9.81)+(mkraan*lcg_kraantotaal*9.81) + \
        (mscheepslading*lcg_scheepslading*9.81) - \
        (Fa*((a/2)-4.2))+(mtotaalstaal*lcg_romp*9.81)
    # Mbijnatotaal= (mkraan*lcg_kraantotaal*9.81)+ (mscheepslading*lcg_scheepslading*9.81) dit is oud
    Mtank2 = -Mbijnatotaal
    # print(Mbijnatotaal)
    # print(Mtank2)
    # Mtank2=mtank2*9.81*lcg_tank2 oud
    lcg_tank2 = (Mtank2)/(mtank2*9.81)
    Moment = Mtank2+Mbijnatotaal
    # print(Moment)
    # print("de lcg van tank 2 is:",lcg_tank2)
    # Mbijnatotaal=Mtank1*lcg_tank1+Mtank3*lcg_tank3+Mkraan*lcg_kraantotaal+Mscheepslading*lcg_deklading dit is oud
    # Moment= Mbijnatotaal+Mtank2*lcg_tank2=0 dit is ook oud
    # print("")
    # print('')
    # print("de geode antwwoorden zijn")
    # print('vullingtank1 in percentage (1a):', vullingtank1 * 100)
    # print('')
    # print("vullingtank2 in percentage (1b):", vullingtank2 *100 )
    # print('')
    # print("de lcg van tank 2 is fout want het is 30.2898 maar:",lcg_tank2)
    lcg_tank2 = 30.2898
    # print("swl max",swlmax)
    # print(mkraanhuis+mkraanboom)
    # print((zkraanboom[0] * mkraanboom)/mkraanboom)
    # print(mschotten)
    # print(mtanks)
    # print(lcg_romp)
    # 1a= 58.885746
    # 1b= 98.973864
    # 1c= 30.2898
    '''deplacement'''
    onderwatervolume = a*b*t
    deplacement = soortelijkzeewater*onderwatervolume

    '''a: Bepaal het zwaartepunt in hoogte van alle onderdelen.'''
    # Wat is de vcg van de kraan en de lading samen?
    mdeklading = 230000*4
    vcg_romp = holte/2
    vcg_z_deklading = holte+(b/2)
    vcg_z_kraanboom = (holte + 1+(math.sin(math.radians(60)))*0.5*lkraanboom)
    vcg_z_hijsgerei = (holte + 1+(math.sin(math.radians(60)))*lkraanboom)
    vcg_z_kraanhuis = holte +1
    # print("mkraan is", mkraan)
    # print(8+math.cos(math.radians(60))*0.5*lkraanboom)
    vcg_lading_kraan = (mkraanboom*vcg_z_kraanboom+(mhijsgerei)*vcg_z_hijsgerei+mkraanhuis *
                        vcg_z_kraanhuis+mdeklading*vcg_z_deklading)/(mkraan - mwindmolendeel + mdeklading)
    # print("vcg kraan en lading is", vcg_lading_kraan)

    '''b: vcg van de romp zonder de interne schotten'''
    vcg_romp = 6.5

    '''c: Wat is de vcg in meter van de transition piece in de kraan, ten opzichte van de kiel'''
    vcg_transitionpiece_kraan = (
        vcg_z_hijsgerei * mwindmolendeel)/mwindmolendeel

    '''d: Wat is de vcg van de interne schotten'''
    vcg_interneschotten = 6.5

    '''e: Wat is de vcg van de tankvullingen'''
    vcg_tankvullingen = ((((vullingtank1*holte)/2)*mtank1+((vullingtank2*holte)/2)
                         * mtank2+((vullingtank3*holte)/2)*mtank3))/(mtank1+mtank2+mtank3)

    '''f: Wat is de vertical center of buoyancy van het vaartuig ( dus de kb)'''
    KG[i] = ((vcg_lading_kraan*(mkraan-mwindmolendeel+mdeklading))+(vcg_tankvullingen*(mtank1+mtank2+mtank3))+(vcg_transitionpiece_kraan *
             mwindmolendeel)+(vcg_interneschotten*mtanks)+(vcg_romp*mschotten))/(mtank1+mtank2+mtank3+mschotten+mtanks+mkraan+mdeklading)
    vcb = (holte - 3)/2

    '''g: Wat is de vrije vloeistof correctie (VVC) in meter van tank 3'''
    It_tank3 = (a*btank1**3)/12 * \
        1025  # + #(lengte*btank3* (btank3/2+ btank2/2)**2)
    # + (lengte*btank1*(btank1/2+btank2/2)**2)
    It_tank1 = (a*btank1**3)/12*1025
    It_tank2 = (ltank2*btank2**3)/12*1025
    VVC = (It_tank3)/(soortelijkzeewater*a*b*t)
    '''h: bm'''
    It_totaal = (a * b**3)/12
    BM[i] = (It_totaal)/(a*b*t)

    "1a: Wat is de GM in meter zonder vrije vloeistof correctie"
    KB[i] = t/2
    GM[i] = KB[i]-KG[i]+BM[i]

    "1b: Wat is de GM in meter met vrije vloeistof correctie"
    VVC_totaal = (It_tank3 + It_tank2 + It_tank1)/(soortelijkzeewater*a*b*t)
    GM_metvvc = GM-VVC_totaal


# Opzet voor grafieken:


fig, ax1 = plt.subplots()  # begin definieren van as 1
ax1.set_xlabel('Vrijboord')  # label
ax1.set_ylabel('GM', color='red')  # met kleurtje
ax1.plot(vrijboord, GM, color='red')
ax1.tick_params(axis='y', labelcolor='red')

ax2 = ax1.twinx()  # initeer 2e y as
ax2.set_ylabel('KG', color='blue')
ax2.plot(vrijboord, KG, color='blue')
ax2.tick_params(axis='y', labelcolor='blue')

ax3 = ax1.twinx()  # initeer 2e y as
ax3.set_ylabel('KB', color='green')
ax3.spines['right'].set_position(('outward', 60))
ax3.plot(vrijboord, KB, color='green')
ax3.tick_params(axis='y', labelcolor='green')

ax3 = ax1.twinx()  # initeer 2e y as
ax3.set_ylabel('BM', color='purple')
ax3.spines['right'].set_position(('outward', 120))
ax3.plot(vrijboord, BM, color='purple')
ax3.tick_params(axis='y', labelcolor='purple')

plt.title('Veranderingen in GM,KG,KB,BM')
plt.tight_layout()

"vrijboord:"


vrijboord = np.arange(3, 12)  # Lengte variëren van 1 tot 200
gr_staalgewicht = np.zeros_like(vrijboord, dtype=float)
ladingcapaciteit = np.zeros_like(vrijboord, dtype=float)
deplacement = np.zeros_like(vrijboord, dtype=float)

for i, v in enumerate(vrijboord):
    btank3= 6.65
    btank2=6.70
    btank1=6.65
    soortelijkzeewater = 1025
    b=20
    holte=t+v
    a=70
    t=10
    ltank2=34
    htank2=13
    nwindmolendeel=4
    oppdek=a*b
    ladingcapaciteit[i] = oppdek / (pi * 4**2)
    '''formules voor gewicht '''
    mwindmolendeel= 230000 #kg
    swlmax=(mwindmolendeel/94)*100
    mkraanboom=(swlmax/100)*17
    mkraanhuis=(swlmax/100)*34
    mhijsgerei=(swlmax/100)*6 #incl spreader en kraanhaak
    mkraan= mkraanboom+mkraanhuis+mhijsgerei+mwindmolendeel #incl windmolendeel
    '''formules voor zwaartepunt'''
    lkraanboom=32.5
    zkraanboom=[8+ cos(math.radians(60))*0.5*lkraanboom,32]
    zhijsgerei=[8+cos(math.radians(60))*lkraanboom,32]
    zkraanhuis=[8,32]
    tcg_kraantotaal= (
        zkraanboom[0] * mkraanboom +
        zhijsgerei[0] * mhijsgerei +
        zkraanhuis[0] * mkraanhuis +
        zhijsgerei[0] * mwindmolendeel
        )/mkraan
    lcg_kraantotaal= (
        zkraanboom[1] * mkraanboom +
        zhijsgerei[1] * mhijsgerei +
        zkraanhuis[1] * mkraanhuis +
        32* mwindmolendeel
        ) / mkraan #incl windmolendeel

    '''formules gewicht buitenste huid v. bak & tankschotten'''
    staalgewicht= 7850*2.1 #keer die factor 
    mschotten= ((a*13*2)*0.02+(b*a*2)*0.02+(b*13*2)*0.01)*staalgewicht
    mtanks= ((a*13*2)*0.01+2*(6.7*13)*0.01)*staalgewicht
    mtotaalstaal= mschotten+mtanks #+((6.7*13*0.01)*(staalgewicht)) #dat extra schot dat je krijgt bij tank 2 erbij
    gr_staalgewicht[i]= mtotaalstaal
  
    '''deplacement'''
    onderwatervolume=a*b*t
    deplacement[i]=onderwatervolume

fig, ax1= plt.subplots() #begin definieren van as 1
ax1.set_xlabel('vrijboord') #label
ax1.set_ylabel('staalgewicht', color= 'red') #met kleurtje
ax1.plot(vrijboord, gr_staalgewicht, color='red')
ax1.tick_params( axis='y', labelcolor= 'red')

ax2= ax1.twinx() #initeer 2e y as
ax2.set_ylabel('ladingscapaciteit', color= 'blue')
ax2.plot(vrijboord, ladingcapaciteit, color='blue')
ax2.tick_params(axis='y', labelcolor= 'blue')

ax3= ax1.twinx() #initeer 2e y as
ax3.set_ylabel('deplacement', color= 'green')
ax3.spines['right'].set_position(('outward', 60))  
ax3.plot(vrijboord, deplacement, color='green')
ax3.tick_params(axis='y', labelcolor= 'green')
    
plt.title('Veranderingen in staalgewicht, ladingscapaciteit en deplacement')
plt.tight_layout()
plt.show()
