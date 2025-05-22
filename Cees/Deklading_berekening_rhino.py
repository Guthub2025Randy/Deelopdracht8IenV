# -*- coding: utf-8 -*-
"""
Created on Fri May 16 11:13:33 2025

@author: CWMaz
"""

import os

ghdoc_path = ghenv.Component.OnPingDocument().FilePath

if ghdoc_path:
    folder = os.path.dirname(ghdoc_path)
    filename = f"Positie_Deklading_v{int(version):02d}.txt"
    full_path = os.path.join(folder, filename)

    if Pt and len(Pt) >= 5:
        lines = []
        centroid_x = 0
        centroid_y = 0
        centroid_z = 0

        for i, pt in enumerate(Pt[:5]):
            if i < 4:
                label = f"TP{i+1}"
                # Sommeer voor centroid
                centroid_x += pt.X
                centroid_y += pt.Y
                centroid_z += pt.Z
            else:
                label = "kraan"
            lines.append(f"{label}: {pt.X},{pt.Y},{pt.Z}")

        # Bereken zwaartepunt van TP1 t/m TP4
        centroid_x /= 4
        centroid_y /= 4
        centroid_z /= 4

        lines.append(f"zwaartepunt: {centroid_x},{centroid_y},{centroid_z}")

        content = "\n".join(lines)

        with open(full_path, "w") as f:
            f.write(content)
    else:
        print("⚠️ Zorg dat er minstens 5 punten zijn ingevoerd.")
else:
    print("⚠️ Sla eerst je Grasshopper-bestand op!")
