# -*- coding: utf-8 -*-
"""
Created on Tue Mar  4 17:26:44 2025

@author: randy
"""
from bibliotheek import np
from bulkheads_splitsen import bulkhead2
from Kraanfunctie_krachten_en_posities import Kraanfunctie

def positiesmetkrachtenlijst1(dic_bulk, positie_w_t1, kracht_w_t1, positie_w_t3, kracht_w_t3, h, COB, staalgewicht, plaatdikte_bh, kraan_lcg, SWLMax, dic_hull, plaatdikte_romp,  opwaartse_kracht):
  """
  Het doel van deze functie is twee lijsten te creëeren: een met alle krachten en een met de corresponderende posities.
  de krachten lijst bestaat uit floats terwijl de positielijst uit lijsten bestaat. Deze lijsten bevatten steeds drie elementen, respectievelijk de lcg, tcg en vcg van de massa.
  """
  krachten = []
  positie = []
  for x in dic_bulk:
    krachten.append(-dic_bulk[x][0]*staalgewicht*plaatdikte_bh)
    positie.append(dic_bulk[x][1:4])
  for x in dic_hull:
    if x == "Transom Area ":
      krachten.append(-float(dic_hull[x][0]*staalgewicht*plaatdikte_bh))
      positie.append(dic_hull[x][1:4])
    else:
      krachten.append(-dic_hull[x][0]*staalgewicht*plaatdikte_romp)
      positie.append(dic_hull[x][1:4])
  krachten.append(-kracht_w_t3)
  krachten.append(opwaartse_kracht)
  krachten.append(-kracht_w_t1)
  positie.append(positie_w_t3)
  positie.append(COB)
  positie.append(positie_w_t1)
  krachten2, posities2 = Kraanfunctie(krachten, positie, h, kraan_lcg, SWLMax)
  return krachten2, posities2


def positiesmetkrachtenlijst2(dictionary_bulkheads, locatie3, kracht3, H, COB, Staalgewicht, Plaatdikte, kraan_lcg, SWLMax, dictionary_hull, Plaatdikte2, opdrijvende_kracht):
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
        if key == ["Transom Area "]:
            krachten.append(float(-value[0]*Staalgewicht*Plaatdikte))
        else:
            krachten.append(float(-value[0]*Staalgewicht*Plaatdikte2))
    krachten1 = Kraanfunctie(krachten, posities, H, kraan_lcg, SWLMax)[0]
    posities1 = Kraanfunctie(krachten, posities, H, kraan_lcg, SWLMax)[1]
    krachten1.append(float(-kracht3))
    krachten1.append(opdrijvende_kracht)
    posities1.append(locatie3)
    posities1.append(COB)
    return krachten1, posities1