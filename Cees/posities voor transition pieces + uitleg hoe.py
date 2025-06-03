"""
Hoe stel ik dit op in Rhino en grasshopper?

1) maak in punt op het punt dat je wil hebben in je txt bestand (in dit geval dus de transitionpieces)
2) group dit punt met zijn object, zodat als je een tp verplaatst dit punt ook mee beweegt. 
3) in grasshopper: params-->point-->rechtermuis op point-->set multiple points--> klik al je gemaakte punten aan-->enter
4) in grasshopper: maths--> scripts-->python 3 script
5) voeg de onderstaande code toe aan dit script(rechtermuis --> open script editor)
6) noem de bovenste input "Pt_TP" en de onderste "version"
7) connect je point met Pt_TP en version met version
8) rechter muisklik op Pt_TP en klik "list acces"

in de txt file krijg je nu eerst van elke TP de LCG,VCG en TCG en het laatste getal is altijd het zwaartepunt van alle TPs



"""


import os
import rhinoscriptsyntax as rs

ghdoc_path = ghenv.Component.OnPingDocument().FilePath

if ghdoc_path:
    folder = os.path.dirname(ghdoc_path)

    version_value = version[0] if isinstance(version, list) else version
    filename = f"tpdata_V{int(version_value):2d}.0.txt"
    full_path = os.path.join(folder, filename)

    if Pt_TP and len(Pt_TP) >= 1:
        lines = []
        sum_x = 0
        sum_y = 0
        sum_z = 0
        valid_points = 0

        for i, pt_guid in enumerate(Pt_TP):
            pt = rs.coerce3dpoint(pt_guid)
            if pt:
                lines.append(f"{pt.X},{pt.Y},{pt.Z}")
                sum_x += pt.X
                sum_y += pt.Y
                sum_z += pt.Z
                valid_points += 1
            else:
                print(f"Punt {i + 1} is geen geldig puntobject.")

        if valid_points > 0:
            centroid_x = sum_x / valid_points
            centroid_y = sum_y / valid_points
            centroid_z = sum_z / valid_points
            lines.append(f"{centroid_x},{centroid_y},{centroid_z}")

            with open(full_path, "w") as f:
                f.write("\n".join(lines))
        else:
            print("Geen geldige punten gevonden.")
    else:
        print("Voer ten minste één punt in voor de Transition Pieces.")
else:
    print("Sla eerst het Grasshopper-bestand op.")

