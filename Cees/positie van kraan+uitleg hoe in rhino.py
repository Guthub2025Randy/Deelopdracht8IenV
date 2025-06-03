# -*- coding: utf-8 -*-
"""
Created on Mon Jun  2 15:49:35 2025

@author: CWMaz
params --> point --> rechtermuisklik --> set one point --> klik center van onderste cirkel kraan
maths--> scripts--> python 3 script
-->voeg die script toe aan de python script (rechtermuisklik--> open script editor--> crtl c + ctrl v)

noem eerste input "Pt_Kraan" en de 2de version 

verbind point met Pr_Kraan en version met version

het is wel van belang dat als we kraan verplaatsen dat het punt wat via point aangeklikt is mee beweegt en dus gegrouped is in rhino. 




"""

import os
import rhinoscriptsyntax as rs

ghdoc_path = ghenv.Component.OnPingDocument().FilePath

if ghdoc_path:
    folder = os.path.dirname(ghdoc_path)
    filename = f"Kraanpositie_V{int(version):2d}.0.txt"
    full_path = os.path.join(folder, filename)

    if Pt_Kraan:
        point = rs.coerce3dpoint(Pt_Kraan)  # Zet Guid om naar Point3d

        if point:
            content = f"{point.X},{point.Y},{point.Z}"

            with open(full_path, "w") as f:
                f.write(content)
        else:
            print("Het geselecteerde object is geen punt.")
    else:
        print("Er is geen punt ingevoerd voor de kraanpositie.")
else:
    print("Het Grasshopper-bestand is nog niet opgeslagen.")