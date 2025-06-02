# -*- coding: utf-8 -*-
"""
Created on Mon Jun  2 15:41:29 2025

@author: CWMaz

deze functie moet in je invoeren in grasshopper. 

eerst params --> point
dan maths--> script --> python 3 script
noem de eerste input  "Pt_TP" en de 2de "version"
klik met rechter muisklik op "list acces"
klik op point--> set mulitiple points--> klik op alle transition pieces het midden van alle onderkanten de cilinder

verbind als de point param met Pt_TP en de version met de version uit de originele grasshopper

klik op de python 3 script met je rechter muisklik op "open script editor"
en voeg onderstaand script toe. 

BELANGRIJK: het is wel van belang dat als we TPs verplaatsen dat de punten die via point aangeklikt is mee beweegen
 en dus gegrouped zijn in rhino. 
"""

import os

ghdoc_path = ghenv.Component.OnPingDocument().FilePath

if ghdoc_path:
    folder = os.path.dirname(ghdoc_path)
    filename = f"tpdata_V{int(version):2d}.0.txt"
    full_path = os.path.join(folder, filename)

    if Pt_TP and len(Pt_TP) == 4:
        lines = []
        centroid_x = 0
        centroid_y = 0
        centroid_z = 0

        for i, pt in enumerate(Pt_TP):
            lines.append(f"{pt.X},{pt.Y},{pt.Z}")
            centroid_x += pt.X
            centroid_y += pt.Y
            centroid_z += pt.Z

        centroid_x /= 4
        centroid_y /= 4
        centroid_z /= 4
        lines.append(f"{centroid_x},{centroid_y},{centroid_z}")

        with open(full_path, "w") as f:
            f.write("\n".join(lines))
    else:
        print("Voer exact 4 punten in voor de Transition Pieces.")
else:
    print("Sla eerst het Grasshopper-bestand op.")
