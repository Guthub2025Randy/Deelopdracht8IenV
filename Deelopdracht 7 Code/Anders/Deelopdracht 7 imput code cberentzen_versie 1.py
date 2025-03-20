# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 14:37:02 2025

@author: cbere
"""
import pandas as pd
import numpy as np

versienummer = 1

df_tv1 = pd.read_csv("data/Tank1_Diagram_Volume_Gr22_V{0}.0.txt".format(versienummer), header=2)
df_twp1 = pd.read_csv("data/Tank1_Diagram_Waterplane_Gr22_V{0}.0.txt".format(versienummer), header=2)
df_tv2 = pd.read_csv("data/Tank2_Diagram_Volume_Gr22_V{0}.0.txt".format(versienummer), header=2)
df_twp2 = pd.read_csv("data/Tank2_Diagram_Waterplane_Gr22_V{0}.0.txt".format(versienummer), header=2)
df_tv3 = pd.read_csv("data/Tank3_Diagram_Volume_Gr22_V{0}.0.txt".format(versienummer), header=2)
df_twp3 = pd.read_csv("data/Tank3_Diagram_Waterplane_Gr22_V{0}.0.txt".format(versienummer), header=2)
df_bhd = pd.read_csv("data/TankBHD_Data_Gr22_V{0}.0.txt".format(versienummer), header=1)
df_had = pd.read_csv("data/HullAreaData_Gr22_V{0}.0.txt".format(versienummer))
msp = "data/MainShipParticulars_Gr22_V{0}.0.txt".format(versienummer)


df_t1 = pd.concat([df_tv1, df_twp1])
df_t2 = pd.concat([df_tv2, df_twp2])
df_t3 = pd.concat([df_tv3, df_twp3])

df_t1["tanknummer"] = [1]*len(df_t1)
df_t2["tanknummer"] = [2]*len(df_t2)
df_t3["tanknummer"] = [3]*len(df_t3)
df_bhd = df_bhd.drop(columns=[" x_min [m]", " x_max [m]"], axis=1)

def datatanks (df_t):
    dic = {}
    dic["vulling_%_{0}".format(df_t.iloc[0,13])] = df_t.iloc[:,1].to_numpy()
    dic["vol_{0}".format(df_t.iloc[0,13])] = df_t.iloc[:7,2].to_numpy()
    dic["lcg_{0}".format(df_t.iloc[0,13])] = df_t.iloc[:7,3].to_numpy()
    dic["tcg_{0}".format(df_t.iloc[0,13])] = df_t.iloc[:7,4].to_numpy()
    dic["vcg_{0}".format(df_t.iloc[0,13])] = df_t.iloc[:7,5].to_numpy()
    dic["inertia_{0}".format(df_t.iloc[0,13])] = df_t.iloc[7:,10].to_numpy()
    return dic

d1 = datatanks(df_t1)
d2 = datatanks(df_t2)
d3 = datatanks(df_t3)

def databh (df):
    dic ={}
    for i in range(len(df)):
        dic["bulkhead_{0}".format(i+1)] = df.iloc[i,:].to_numpy()
    return dic

dbh = databh(df_bhd)

def file_to_dic (path):
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

msp = file_to_dic(msp)

df_had = df_had.rename(columns={" vca [m]":"tcg", " tca [m] Group 22; Version 1.0":"vca"})

def dataha(df):
    dic = {}
    for i in range(len(df)):
        k = df.iloc[i,0]
        v = df.iloc[i,1:].to_numpy()
        dic[k] = v
    return dic

dha = dataha(df_had)

    