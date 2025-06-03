# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 14:37:02 2025

@author: cbere
"""
import pandas as pd
import numpy as np

from scipy import interpolate as ip
import matplotlib.pyplot as plt
"""
deze code heeft als doel de data uit de textbestanden te halen en in een vorm te zetten die later bruikbaar is. De meeste
data zal worden geplaatst in dictionaries.
"""
versienummer = 1

df_tv1 = pd.read_csv("Tank1_Diagram_Volume_Gr22_V{0}.0.txt".format(versienummer), header=2)
df_twp1 = pd.read_csv("Tank1_Diagram_Waterplane_Gr22_V{0}.0.txt".format(versienummer), header=2)
df_tv2 = pd.read_csv("Tank2_Diagram_Volume_Gr22_V{0}.0.txt".format(versienummer), header=2)
df_twp2 = pd.read_csv("Tank2_Diagram_Waterplane_Gr22_V{0}.0.txt".format(versienummer), header=2)
df_tv3 = pd.read_csv("Tank3_Diagram_Volume_Gr22_V{0}.0.txt".format(versienummer), header=2)
df_twp3 = pd.read_csv("Tank3_Diagram_Waterplane_Gr22_V{0}.0.txt".format(versienummer), header=2)
df_bhd = pd.read_csv("TankBHD_Data_Gr22_V{0}.0.txt".format(versienummer), header=1)
df_had = pd.read_csv("HullAreaData_Gr22_V{0}.0.txt".format(versienummer))
mainsp = "MainShipParticulars_Gr22_V{0}.0.txt".format(versienummer)
# Bestanden voor deelopdracht 8
df_csa = pd.read_csv("Buoyant_CSA_Gr22_V{0}.0.txt".format(versienummer), header=3)
df_shell_csa = pd.read_csv("Shell_CSA_Gr22_V{0}.0.txt".format(versienummer), header=3)
df_tank1_csa = pd.read_csv("Tank1_CSA_Gr22_V{0}.0.txt".format(versienummer), header=3)
df_tank2_csa = pd.read_csv("Tank2_CSA_Gr22_V{0}.0.txt".format(versienummer), header=3)
df_tank3_csa = pd.read_csv("Tank3_CSA_Gr22_V{0}.0.txt".format(versienummer), header=3)
# Einde bestanden voor deelopdracht 8
resistance =pd.read_csv("ResistanceData_Gr22_V{0}.0.txt".format(versienummer),header=6)


"""
Gegevens van de tanks: er zijn per tank twee csv files: "diagram volume" en "diagram waterplane". Om alle gegevens per tank 
bij elkaar te krijgen worden de dataframes van deze twee soorten csv files bij elkaar gevoegd. Vervolgens wordt er een extra
kolom met het tanknummer toegevoegd en worden de onnodige kolommen verwijderd.
"""

df_t1 = pd.concat([df_tv1, df_twp1])
df_t2 = pd.concat([df_tv2, df_twp2])
df_t3 = pd.concat([df_tv3, df_twp3])

df_t1["tanknummer"] = [1]*len(df_t1)
df_t2["tanknummer"] = [2]*len(df_t2)
df_t3["tanknummer"] = [3]*len(df_t3)

def datatanks(df_t):
    """
    deze functie vraagt een dataframe en plaatst de relevante data in een dictionary en geeft deze vervolgens terug
    """
    dic = {}
    dic["vulling_%_{0}".format(df_t.iloc[0,13])] = df_t.iloc[:,1].to_numpy()
    dic["vol_{0}".format(df_t.iloc[0,13])] = df_t.iloc[:7,2].to_numpy()
    dic["lcg_{0}".format(df_t.iloc[0,13])] = df_t.iloc[:7,3].to_numpy()
    dic["tcg_{0}".format(df_t.iloc[0,13])] = df_t.iloc[:7,4].to_numpy()
    dic["vcg_{0}".format(df_t.iloc[0,13])] = df_t.iloc[:7,5].to_numpy()
    dic["inertia_{0}".format(df_t.iloc[0,13])] = df_t.iloc[7:,10].to_numpy()
    return dic


"""
Ook zijn de gegevens uit de bulkhead data file nodig. 
"""
def databh(df):
    """
    deze functie vraagt om een dataframe en plaatst de relevante bulkhead gegevens in drie verschillende dictionaries: 
    dic bevat alle bulkheads behalve die van tank 2, dic2 bevat alleen de bulkheads van tank 2 en dic3 bevat alle bulkheads.
    de dictionaries hebben als key "bulkhead_" gevolgd door een nummer tussen de 0 en de 12 (er zijn 11 bulkheads) en als value
    een array met de relevante gegevens.
    """
    dic ={}
    dic2 ={}
    dic3 ={}
    for i in range(len(df)):
        if df.iloc[i,2] == 0:
            dic2["bulkhead_{0}".format(i+1)] = df.iloc[i,:].to_numpy()
        else:
            dic["bulkhead_{0}".format(i+1)] = df.iloc[i,:].to_numpy()
        dic3["bulkhead_{0}".format(i+1)] = df.iloc[i,:].to_numpy()
    return dic, dic2, dic3


def file_to_dic(path):
    """
    deze functie heeft als doel uit het bestand MainShipParticulars de data te halen en in een dictionary te zetten. Omdat het 
    bestand ook kopjes bevat, worden alle regels waar geen komma in staat over geslagen. Bevat een regel dat wel, dan worden de
    gegevens aan weerszijde van de komma als key en value van de dictionary gebruikt.
    """
    dic = {}
    with open(path, "r") as file:
        for line in file:
            if "," in line:
                k,v = line.split(",",1)
                k = k.strip()
                v = v.strip()
                if "," in v:
                    v = np.fromstring(v, dtype=float, sep=",")
                dic[k]=v
            else:
                continue
    return dic

"""
tot slot moet de data uit het hullareadata bestand gehaald worden. Eerst moeten de kolomtitels van de vca en tca verwisseld worden,
omdat grasshopper deze niet correct genereert.
"""
df_had = df_had.rename(columns={" vca [m]":"tcg", " tca [m] Group 22; Version 1.0":"vca"})

def dataha(df):
    """
    Deze functie zet de data uit de dataframe van hull area data in een dictionary, waarbij als key het romponderdeel (bv "Transom")
    en als value een array met de gegevens wordt gebruikt.
    """
    dic = {}
    for i in range(len(df)):
        k = df.iloc[i,0]
        v = df.iloc[i,1:].to_numpy()
        dic[k] = v
    return dic

d1 = datatanks(df_t1)
d2 = datatanks(df_t2)
d3 = datatanks(df_t3)
dbh1, dbh2, dbh = databh(df_bhd)
msp = file_to_dic(mainsp)
dha = dataha(df_had)
# Begin deelopdracht 8
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

def traagheidsdic(df_I):
    """
    deze functie vraagt een dataframe en plaatst de relevante data in een dictionary en geeft deze vervolgens terug
    """
    dic = {}
    dic["X [m]".format(df_I.iloc[0,11])] = df_I.iloc[:,0].to_numpy()
    dic["OUTLINE LENGTH [m]".format(df_I.iloc[0,11])] = df_I.iloc[:,1].to_numpy()
    dic["CROSS SECTION AREA OF SHELL PLATING [m2]".format(df_I.iloc[0,11])] = df_I.iloc[:,2].to_numpy()
    dic["CENTROID_X[m]".format(df_I.iloc[0,11])] = df_I.iloc[:,3].to_numpy()
    dic["CENTROID_Y[m]".format(df_I.iloc[0,11])] = df_I.iloc[:,4].to_numpy()
    dic["CENTROID_Z[m]".format(df_I.iloc[0,11])] = df_I.iloc[:,5].to_numpy()
    dic["INERTIA_X[m4]".format(df_I.iloc[0,11])] = df_I.iloc[:,6].to_numpy()
    dic["INERTIA_Y[m4]".format(df_I.iloc[0,11])] = df_I.iloc[:,7].to_numpy()
    dic["INERTIA_Z[m4]".format(df_I.iloc[0,11])] = df_I.iloc[:,8].to_numpy()
    dic["Z_Keel[m]".format(df_I.iloc[0,11])] = df_I.iloc[:,9].to_numpy()
    dic["Z_DECK[m]".format(df_I.iloc[0,11])] = df_I.iloc[:,10].to_numpy()
    return dic

dic_Shell_CSA = traagheidsdic(df_shell_csa)

def dic_csa_ballast_tanks(df_tank):
    """
    Deze functie zet de df van de ballast tanks om in een dictionary.

    Parameters
    ----------
    df : TYPE: dataframe
        DESCRIPTION.

    Returns
    -------
    dic : TYPE: dictionary
        DESCRIPTION.

    """
    dic_tank = {}
    dic_tank["x_in_m".format(df_tank.iloc[7,0])] = df_tank.iloc[:,0].to_numpy()
    dic_tank[" crossarea_in_m2".format(df_tank.iloc[7,1])] = df_tank.iloc[:,1].to_numpy()
    return dic_tank

def calcNeutraleAs(lengte_schip, tussenstappen_lengte, hoogte_neutrale_as):
    volledig = ip.interp1d(tussenstappen_lengte, hoogte_neutrale_as, kind="quadratic", fill_value="extrapolate")
    volledig2 = volledig(lengte_schip)
    return volledig2

def calcKiel(lengte_schip, tussenstappen_lengte, hoogte_kiel):
    geinterpoleerd= ip.interp1d(tussenstappen_lengte, hoogte_kiel, kind="quadratic", fill_value="extrapolate")
    geinterpoleerd2=geinterpoleerd(lengte_schip)
    return geinterpoleerd2 

def calcVezelafstand(centroidCM, kielCM):
    vezelafstand= centroidCM-kielCM
    return vezelafstand


lengte_schip = np.linspace(-9, 141, 150001)
tussenstappen_lengte = dic_Shell_CSA["CENTROID_X[m]"]
hoogte_neutrale_as = dic_Shell_CSA["CENTROID_Z[m]"]
hoogte_kiel=dic_Shell_CSA["Z_Keel[m]"]

centroid_z_in_cm = calcNeutraleAs(lengte_schip, tussenstappen_lengte, hoogte_neutrale_as)
kiel_z_in_cm = calcKiel(lengte_schip, tussenstappen_lengte, hoogte_kiel)
vezelafstand_in_cm = calcVezelafstand(centroid_z_in_cm, kiel_z_in_cm)


plt.plot(lengte_schip, centroid_z_in_cm)
plt.plot(lengte_schip, kiel_z_in_cm)
plt.plot(lengte_schip, vezelafstand_in_cm)