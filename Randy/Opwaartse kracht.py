# -*- coding: utf-8 -*-
"""
Created on Thu Mar 20 14:24:08 2025

@author: randy
"""
from bibliotheek import np, sm, plt

def Opwaartse_kracht(dic_CSA, zwaartekracht):
    oppervlakte = dic_CSA["crossarea_in_m2"]
    lps = dic_CSA["x_in_m"]
    Onderwater_volume = [0]
    for i in range(len(oppervlakte)-1):
        dx = lps[i+1]-lps[i]
        Onderwater_volume.append(((oppervlakte[i]*dx)+(oppervlakte[i+1]*dx))/2)
    Opwaartse_kracht = -np.array(Onderwater_volume)*zwaartekracht
    plt.figure(figsize=(8,5))
    plt.plot(lps, Opwaartse_kracht, color='b', label='Opwaartse kracht')
    plt.xlabel("Lengte van het schip (L) in [m]")
    plt.ylabel("Opwaartse kracht (p) in [N]")
    plt.title("De verdeelde opwaartse kracht")
    plt.legend()
    plt.grid(True)
    return None
g = 9.81
dictionary_Cross = {"x_in_m" : np.array([-9,
                                         -1.8571,
                                         5.2857,
                                         12.4286,
                                         19.5714,
                                         26.7143,
                                         33.8571,
                                         41,
                                         48.1429,
                                         55.2857,
                                         62.4286,
                                         69.5714,
                                         76.7143,
                                         83.8571,
                                         91,
                                         98.1429,
                                         105.2857,
                                         112.4286,
                                         119.5714,
                                         126.7143,
                                         133.8571,
                                         141,
                                         148.1429
                                         ]),
                    "crossarea_in_m2":np.array([2.0457
                                                ,41.5719
                                                ,82.4958
                                                ,120.3785
                                                ,153.6468
                                                ,179.4824
                                                ,191.3709
                                                ,191.5296
                                                ,191.5296
                                                ,191.5296
                                                ,191.5296
                                                ,191.5296
                                                ,191.5296
                                                ,191.5296
                                                ,191.5296
                                                ,191.5296
                                                ,191.4224
                                                ,189.2984
                                                ,181.4377
                                                ,158.3371
                                                ,114.5233
                                                ,0
                                                ,0
                                                ])}
Opwaartse_kracht(dictionary_Cross, g)