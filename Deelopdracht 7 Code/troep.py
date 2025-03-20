# -*- coding: utf-8 -*-
"""
Created on Mon Mar 10 21:35:36 2025

@author: randy
"""


krachten2

volume_t1

kraan_lcg

print(kracht_t1, kracht_t2, kracht_t3)

list1 = []
for x in dbh1:
  list1.append(dbh1[x][0]*WEIGHT_STAAL*transom_bhd_thickness)
for x in dha:
  if x == "Transom Area ":
      list1.append(-dha[x][0]*WEIGHT_STAAL*transom_bhd_thickness)
  else:
      list1.append(-dha[x][0]*WEIGHT_STAAL*rest_thickness)
list2 = Kraanfunctie(list1, [], H, kraan_lcg, swlmax)[0]
print(list2)

l = [0]*len(Krachten)
for x in range(len(list2)):
  l[x] = list[x]
for x in range(len(Krachten)):
  print(Krachten[x])
  print(l[x])

for x in range(len(Krachten2)):
  print(Krachten2[x])

print(kracht_t1, kracht_t3)

def tcg(posities, krachten):
  fs = sum(krachten)
  ms = 0
  for i in range(len(posities)):
    ms += posities[i][1]*krachten[i]
  tcg = ms/fs
  return tcg

tcg(Posities2, Krachten2)

print(TweedeMomentensom[0])
print(ms2[0])

print(Krachten)
print(Krachten2)

print(tcg_s_1)
print(kracht_t1)
print(kracht_t1*locatie_t1[1], TweedeMomentensom[0])
print(tcg_s_1*sum_krachten2)

locatie_t3

kracht_t1

print(Posities2)
print(Krachten2)

print(calculateMomentensom_[0])
print(tcg_s_0)
print(sum_krachten, sum_krachten*tcg_s_0)

print(lcg_schip, tcg_schip, vcg_schip)

print(KrachtT2, kracht_t1, kracht_t3)

print(locatie_t1)

print(momentensom1_alt(d1["vol_1"], d1['tcg_1'], calculateMomentensom))

calculateMomentensom[0]

d1['vol_1']*Weight_water*d1['tcg_1']

d3['tcg_3']

print(momentensom1_alt(d1["vol_1"], d1['tcg_1'], np.array([15514398.928126678,0])))

for key, value in dha.items():
  if key == "Transom Area ":
    print(1)
  else:
    print(0)

for key, value in dha.items():
  if key == ["Transom Area "]:
    print(1)
  else:
    print(0)