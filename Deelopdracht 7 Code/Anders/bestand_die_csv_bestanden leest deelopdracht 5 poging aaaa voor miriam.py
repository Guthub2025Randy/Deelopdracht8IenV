# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 17:18:33 2024

@author: gijsl
"""

## QUICK NOTE
## Dit is echt een tyfusbende van een programma, ook zijn de x en y waardes grotendeels door elkaar gegaan ofzo
## Gebruik dit programma in de toekomst niet om functies te maken


#Kraanlast = 2x transition piece van 230 ton want dan kan de kraan met een giekhoek van 0 graden opereren.

import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import interp1d


# beginwaarden

SWLmax = 230/0.94
dichtheid_staal = 7850
Loa = 115
Lpp = 107.4643
boomlengte = 32  # voor 4 2x2 transition pieces gerekend. (dus 16 pieces)

aantal_transition_pieces = 8
vulpercentage_tank3 = 80


# waarden uit TANK 2 TABEL.csv uitlezen

bestand2 = "Tank2_Diagram_Volume_Gr1_V12.33.txt"

tf2 = np.genfromtxt(fname=bestand2,               #vulpercentage tank 2
                    delimiter=',',
                    skip_header=3,
                    usecols=1,
                    filling_values=np.NaN)

tankvolume_tank2 = np.genfromtxt(fname=bestand2,  #tankvolume tank 2
                                 delimiter=',',
                                 skip_header=3,
                                 usecols=2,
                                 filling_values=np.NaN)

lcb_tank2 = np.genfromtxt(fname=bestand2,         # dit spreekt vrij voor zich denk ik
                          delimiter=',',
                          skip_header=3,
                          usecols=3,
                          filling_values=np.NaN)

tcb_tank2 = np.genfromtxt(fname=bestand2,         #zie commentaar regel 27
                          delimiter=',',
                          skip_header=3,
                          usecols=4,
                          filling_values=np.NaN)

vcb_tank2 = np.genfromtxt(fname=bestand2,         #zie commentaar regel 33
                          delimiter=',',
                          skip_header=3,
                          usecols=5,
                          filling_values=np.NaN)

# Interpolatie tank 2 grafiek data
tf2_new = np.linspace(min(tf2), max(tf2), 500)  # 500 is nauwkeurigheid interpolatie (aantal plots tussen min en max ofzo)

tankvolume_interp2 = interp1d(tf2, tankvolume_tank2, kind='cubic', fill_value="extrapolate")
# lcb_interp2 = interp1d(tf2, lcb_tank2, kind='cubic', fill_value="extrapolate")
# vcb_interp2 = interp1d(tf2, vcb_tank2, kind='cubic', fill_value="extrapolate")
# tcb_interp2 = interp1d(tf2, tcb_tank2, kind='cubic', fill_value="extrapolate")

# Plot for Tank 2
fig, ax1 = plt.subplots()

plt.title("Interpolated Data Tank 2")

ax1.set_xlabel('Fill Percentage')
ax1.set_ylabel('Tank Volume', color='r')
ax1.plot(tf2_new, tankvolume_interp2(tf2_new), color='r', label='Tank Volume')

ax2 = ax1.twinx()
ax2.set_ylabel('LCB / VCB / TCB') 
# ax2.plot(tf2_new, lcb_interp2(tf2_new), color='g', label='LCB')
# ax2.plot(tf2_new, vcb_interp2(tf2_new), color='b', label='VCB')
# ax2.plot(tf2_new, tcb_interp2(tf2_new), color='y', label='TCB')

fig.tight_layout()
plt.legend()
plt.show()

# Load data from Tank 3

bestand3 = "Tank3_Diagram_Volume_Gr1_V12.33.txt"

tf3 = np.genfromtxt(fname=bestand3, #tank fill percentage tank 3
                    delimiter=',',
                    skip_header=3,
                    usecols=1,
                    filling_values=np.NaN)

tankvolume_tank3 = np.genfromtxt(fname=bestand3, #tank volume tank 3
                                 delimiter=',',
                                 skip_header=3,
                                 usecols=2,
                                 filling_values=np.NaN)

lcb_tank3 = np.genfromtxt(fname=bestand3,
                          delimiter=',',
                          skip_header=3,
                          usecols=3,
                          filling_values=np.NaN)

tcb_tank3 = np.genfromtxt(fname=bestand3,
                          delimiter=',',
                          skip_header=3,
                          usecols=4,
                          filling_values=np.NaN)

vcb_tank3 = np.genfromtxt(fname=bestand3,
                          delimiter=',',
                          skip_header=3,
                          usecols=5,
                          filling_values=np.NaN)

# Interpolation for Tank 3 data
tf3_new = np.linspace(min(tf3), max(tf3), 500)  # new fill percentage values for smoother curve

tankvolume_interp3 = interp1d(tf3, tankvolume_tank3, kind='cubic', fill_value="extrapolate")
lcb_interp3 = interp1d(tf3, lcb_tank3, kind='cubic', fill_value="extrapolate")
vcb_interp3 = interp1d(tf3, vcb_tank3, kind='cubic', fill_value="extrapolate")
tcb_interp3 = interp1d(tf3, tcb_tank3, kind='cubic', fill_value="extrapolate")

# Plot for Tank 3
fig, ax1 = plt.subplots()

plt.title("Interpolated Data Tank 3")

ax1.set_xlabel('Fill Percentage')
ax1.set_ylabel('Tank Volume', color='r')
ax1.plot(tf3_new, tankvolume_interp3(tf3_new), color='r', label='Tank Volume')

ax2 = ax1.twinx()
ax2.set_ylabel('LCB / VCB / TCB') 
ax2.plot(tf3_new, lcb_interp3(tf3_new), color='g', label='LCB')
ax2.plot(tf3_new, vcb_interp3(tf3_new), color='b', label='VCB')
ax2.plot(tf3_new, tcb_interp3(tf3_new), color='y', label='TCB')

fig.tight_layout()
plt.legend()
plt.show()

# waarden uit TANK 1 TABEL.csv uitlezen
bestand1 = "Tank1_Diagram_Volume_Gr1_V12.33.txt"


tf1 = np.genfromtxt(fname=bestand1,               #vulpercentage tank 1
                    delimiter=',',
                    skip_header=3,
                    usecols=1,
                    filling_values=np.NaN)

tankvolume_tank1 = np.genfromtxt(fname=bestand1,  #tankvolume tank 1
                                 delimiter=',',
                                 skip_header=3,
                                 usecols=2,
                                 filling_values=np.NaN)

lcb_tank1 = np.genfromtxt(fname=bestand1,         # dit spreekt vrij voor zich denk ik
                          delimiter=',',
                          skip_header=3,
                          usecols=3,
                          filling_values=np.NaN)

tcb_tank1 = np.genfromtxt(fname=bestand1,         #zie commentaar regel 27
                          delimiter=',',
                          skip_header=3,
                          usecols=4,
                          filling_values=np.NaN)

vcb_tank1 = np.genfromtxt(fname=bestand1,         #zie commentaar regel 33
                          delimiter=',',
                          skip_header=3,
                          usecols=5,
                          filling_values=np.NaN)

# Interpolatie tank 1 grafiek data
tf1_new = np.linspace(min(tf1), max(tf1), 500)  # 500 is nauwkeurigheid interpolatie (aantal plots tussen min en max ofzo)

tankvolume_interp1 = interp1d(tf1, tankvolume_tank1, kind='cubic', fill_value="extrapolate")
lcb_interp1 = interp1d(tf1, lcb_tank1, kind='cubic', fill_value="extrapolate")
vcb_interp1 = interp1d(tf1, vcb_tank1, kind='cubic', fill_value="extrapolate")
tcb_interp1 = interp1d(tf1, tcb_tank1, kind='cubic', fill_value="extrapolate")

# Plot for Tank 1
fig, ax1 = plt.subplots()

plt.title("Interpolated Data Tank 1")

ax1.set_xlabel('Fill Percentage')
ax1.set_ylabel('Tank Volume', color='r')
ax1.plot(tf1_new, tankvolume_interp1(tf1_new), color='r', label='Tank Volume')

ax2 = ax1.twinx()
ax2.set_ylabel('LCB / VCB / TCB') 
ax2.plot(tf1_new, lcb_interp1(tf1_new), color='g', label='LCB')
ax2.plot(tf1_new, vcb_interp1(tf1_new), color='b', label='VCB')
ax2.plot(tf1_new, tcb_interp1(tf1_new), color='y', label='TCB')

fig.tight_layout()
plt.legend()
plt.show()


#momenten tank 1 (geinterpoleerd)
rho = 1025
g = 9.81
aantalrows = 7
momentx = np.zeros(aantalrows)
i = 0

while i < aantalrows:
    momentx[i] = rho * tankvolume_tank1[i] * g * tcb_tank1[i]    #in Nm (dwarsscheepsmoment)
    i += 1

momentx_interp1 = interp1d(tf1, momentx, kind='cubic', fill_value="extrapolate" )

k = 0
momenty = np.zeros(aantalrows)

while k < aantalrows:
    momenty[k] = rho * tankvolume_tank1[k] * g * lcb_tank1[k]    #in Nm (dwarsscheepsmoment)
    k += 1


momenty_interp1 = interp1d(tf1, momenty, kind='cubic', fill_value="extrapolate" )

j = 0
momentz = np.zeros(aantalrows)

while j < aantalrows:
    momentz[j] = rho * tankvolume_tank1[j] * g * vcb_tank1[j]    #in Nm (dwarsscheepsmoment)
    j += 1


momentz_interp1 = interp1d(tf1, momentz, kind='cubic', fill_value="extrapolate" )

fig, gm1 = plt.subplots()
gm1.set_xlabel('Fill Percentage')
gm1.set_ylabel('Moment tank 1 (Nm)')
gm1.plot(tf1_new, momentx_interp1(tf1_new), color='r', label='Moment X')
gm1.plot(tf1_new, momenty_interp1(tf1_new), color='b', label='Moment Y')
gm1.plot(tf1_new, momentz_interp1(tf1_new), color='g', label='Moment Z')
gm1.legend()






#momenten tank 2 (geinterpoleerd)
# rho = 1025
# g = 9.81
# aantalrows = 9
# momentx2 = np.zeros(aantalrows)
# ii = 0

# while ii < 9:
#     momentx2[ii] = rho * tankvolume_tank2[ii] * g * tcb_tank2[ii]    #in Nm (dwarsscheepsmoment)
#     ii += 1

# momentx2_interp1 = interp1d(tf1, momentx2, kind='cubic', fill_value="extrapolate" )

# kk = 0
# momenty2 = np.zeros(aantalrows)

# while kk < 9:
#     momenty2[kk] = rho * tankvolume_tank2[kk] * g * lcb_tank2[kk]    #in Nm (dwarsscheepsmoment)
#     kk += 1


# momenty2_interp1 = interp1d(tf1, momenty2, kind='cubic', fill_value="extrapolate" )

# jj = 0
# momentz2 = np.zeros(aantalrows)

# while jj < 9:
#     momentz2[jj] = rho * tankvolume_tank2[jj] * g * vcb_tank2[jj]    #in Nm (dwarsscheepsmoment)
#     jj += 1


# momentz2_interp1 = interp1d(tf1, momentz2, kind='cubic', fill_value="extrapolate" )

# fig, gm2 = plt.subplots()
# gm2.set_xlabel('Fill Percentage')
# gm2.set_ylabel('Moment tank 2 (Nm)')
# gm2.plot(tf1_new, momentx2_interp1(tf1_new), color='r', label='Moment X')
# gm2.plot(tf1_new, momenty2_interp1(tf1_new), color='b', label='Moment Y')
# gm2.plot(tf1_new, momentz2_interp1(tf1_new), color='g', label='Moment Z')
# gm2.legend()








#momenten tank 3 (geinterpoleerd)
rho = 1025
g = 9.81
aantalrows = 7
momentx3 = np.zeros(aantalrows)
iii = 0

while iii < aantalrows:
    momentx3[iii] = rho * tankvolume_tank3[iii] * g * tcb_tank3[iii]    #in Nm (dwarsscheepsmoment)
    iii += 1

momentx3_interp1 = interp1d(tf1, momentx3, kind='cubic', fill_value="extrapolate" )

kkk = 0
momenty3 = np.zeros(aantalrows)

while kkk < aantalrows:
    momenty3[kkk] = rho * tankvolume_tank3[kkk] * g * lcb_tank3[kkk]    #in Nm (dwarsscheepsmoment)
    kkk += 1


momenty3_interp1 = interp1d(tf1, momenty3, kind='cubic', fill_value="extrapolate" )

jjj = 0
momentz3 = np.zeros(aantalrows)

while jjj < aantalrows:
    momentz3[jjj] = rho * tankvolume_tank3[jjj] * g * vcb_tank3[jjj]    #in Nm (dwarsscheepsmoment)
    jjj += 1


momentz3_interp1 = interp1d(tf1, momentz3, kind='cubic', fill_value="extrapolate" )

fig, gm3 = plt.subplots()
gm3.set_xlabel('Fill Percentage')
gm3.set_ylabel('Moment tank 3 (Nm)')
gm3.plot(tf1_new, momentx3_interp1(tf1_new), color='r', label='Moment X')
gm3.plot(tf1_new, momenty3_interp1(tf1_new), color='b', label='Moment Y')
gm3.plot(tf1_new, momentz3_interp1(tf1_new), color='g', label='Moment Z')
gm3.legend()





#Moment dwarsscheeps uitrekenen

boomy = 0.5 * boomlengte * 0.5 # hoek van 90 graden
ladingy = boomlengte * 0.5
# dekladingy = 0
huisy = 0
Fhuis = 0.34 *SWLmax *1000 * 9.81
Fboom = 0.17 * SWLmax *1000 * 9.81
Fkraanhaaklading = (0.06*SWLmax + 230) * 1000 *9.81
# Fdeklading = (4*230*1000*9.81)

moment_tank3_dwarsscheeps = momentx3_interp1(vulpercentage_tank3)  

moment_tank1_dwarsscheeps = moment_tank3_dwarsscheeps + boomy * Fboom + ladingy * Fkraanhaaklading + huisy * Fhuis #Geen deklading want deky = 0
print(moment_tank1_dwarsscheeps)

omrekenendinges = interp1d(momentx, tf1, kind='cubic', fill_value="extrapolate" )
print("De vulgraad van tank 1 is",omrekenendinges(abs(moment_tank1_dwarsscheeps)),"%")

# fig, omr = plt.subplots()


# omr.plot(momenty, omrekenendinges(momenty))
# omr.set_xlabel("Moment dwarsscheeps (Nm)")
# omr.set_ylabel("Vulgraad Tank 1 (%)")

# plt.show



## Som van Fz = 0

## opwaartse kracht
volume_romp_diepgang10 = 8674.7351  ## volgens MAIN DIMENSIONS txt 7670.4383
Fb = rho * g * volume_romp_diepgang10

#alle krachten naar beneden
F_kraan_totaal = Fhuis + Fboom + Fkraanhaaklading

F_deklading = aantal_transition_pieces * (230 * 1000 * g)

F_achterschotten = (311.4398 * dichtheid_staal * g * 0.01) * 2.1    ##TBD Group 98
F_middenschotten = (391.8931 * dichtheid_staal * g * 0.01) * 2.1    ##TBD Group 98
F_voorschotten =   (183.7974 * dichtheid_staal * g * 0.01) * 2.1    ##TBD Group 98
F_tussenschot1  =   (62.5143    * dichtheid_staal * g * 0.01) * 2.1    ##TBD Group 98
F_tussenschot2  =   (62.5143 * dichtheid_staal * g * 0.01) * 2.1    ##TBD Group 98

#oppervlakte_romp_zonder_spiegel = 4534.91153 - 119.666135       ## Berekend met rhino
#F_romp = (oppervlakte_romp_zonder_spiegel * dichtheid_staal * g * 0.02) * 2.1

F_transom   = 55.8617 * 0.01 * dichtheid_staal * g * 2.1
F_shell     = 3371.4524 * 0.02 * dichtheid_staal * g * 2.1
F_deck      = 2299.6945 * 0.02 * dichtheid_staal * g  * 2.1

#oppervlakte_spiegel = 119.666135        ## Berekend met rhino
#F_spiegel = (oppervlakte_spiegel * 0.01 * dichtheid_staal * g) * 2.1

F_tank1evenwicht = (tankvolume_interp1(omrekenendinges(abs(moment_tank1_dwarsscheeps))) * rho * g)
F_tank3evenwicht = 3622.4919 * rho * g

F_tank2 = Fb - F_kraan_totaal - F_deklading - 2*F_achterschotten - 2*F_middenschotten - 2*F_voorschotten - F_tussenschot1 - F_tussenschot2 -  F_tank1evenwicht - F_tank3evenwicht - F_transom - F_shell - F_deck
print(F_tank2, "(kracht tank 2 in newton)")


#naar vulpercentage

tankvulpercentage_interp2 = interp1d(tankvolume_tank2, tf2, kind='cubic', fill_value="extrapolate")
tank2vulpercentage = tankvulpercentage_interp2((F_tank2/(rho*g)))
print(tank2vulpercentage,"Vulpercentage tank 2")


## Moment Langscheeps uitrekenen (gerekend om de LPP heen)

Moment_tank3_langscheeps = momenty3_interp1(vulpercentage_tank3)          # 3622.4919 * rho * g * 30.9981

Moment_tank1_langscheeps = momenty_interp1(omrekenendinges(abs(moment_tank1_dwarsscheeps)))

print("test langscheeps moment tank 1",Moment_tank1_langscheeps)

## arm van de romp
                       
#rompx = 35.405514 - (Loa - Lpp)        ## 35.405514 berekend met rhino (zonder spiegel)

transomx = -6.8594
shellx   = 51.6808
deckx    = 49.8562
## armen van de tussenschotten (per 2 want symetrisch, op de tussenwanden tank 2 na)
## Waarden uit TBD Group 98 gehaald

achterschottenx = 22.5026
middenschottenx = 56.6748
voorschottenx   = 85.2177
tussenschot1x   = 46.0932
tussenschot2x   = 67.2564
spiegelx        = -6.8594

## arm van het volume van het volledige schip

armFbx = 53.9096   ## berekend met MAIN DIMENSIONS TXT

## armen kraan en deklading

kraantotaalx = 80

dekladingx = 80

## Momenten
Moment_achterschottenlpp = achterschottenx * F_achterschotten * 2
Moment_middenschottenlpp = middenschottenx * F_middenschotten * 2
Moment_voorschottenlpp   = voorschottenx   * F_voorschotten   * 2
Moment_tussenschot1lpp   = tussenschot1x   * F_tussenschot1
Moment_tussenschot2lpp   = tussenschot2x   * F_tussenschot2

#Moment_romplpp           = rompx           * F_romp
#Moment_spiegellpp        = spiegelx        * F_spiegel

Moment_transomlpp        = transomx        * F_transom
Moment_shelllpp          = shellx          * F_shell
Moment_decklpp           = deckx           * F_deck

Moment_Fblpp             = armFbx          * Fb

Moment_kraantotaallpp    = kraantotaalx    * F_kraan_totaal
Moment_dekladinglpp      = dekladingx      * F_deklading

## Momentensom

Moment_tank2_langscheeps = Moment_tank3_langscheeps + Moment_tank1_langscheeps + Moment_achterschottenlpp + Moment_middenschottenlpp + Moment_voorschottenlpp + Moment_tussenschot1lpp + Moment_tussenschot2lpp + Moment_transomlpp + Moment_shelllpp + Moment_decklpp - Moment_Fblpp  + Moment_kraantotaallpp + Moment_dekladinglpp 

print(Moment_tank2_langscheeps, "(Moment die tank 2 moet tegenwerken)")

## arm = M/F

arm_tank2x = -Moment_tank2_langscheeps/F_tank2

print(arm_tank2x,"afstand van het midden van tank 2 tot de Lpp lijn (m)")






