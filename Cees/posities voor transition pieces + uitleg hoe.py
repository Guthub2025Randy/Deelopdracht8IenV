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




"""


import os
import rhinoscriptsyntax as rs

ghdoc_path = ghenv.Component.OnPingDocument().FilePath

if ghdoc_path:
    folder = os.path.dirname(ghdoc_path)

    # Zorg dat versie een getal is
    version_value = version[0] if isinstance(version, list) else version
    filename = f"tpdata_V{int(version_value):02d}.0.txt"
    full_path = os.path.join(folder, filename)

    if Pt_TP and len(Pt_TP) == 4:
        lines = []
        centroid_x = 0
        centroid_y = 0
        centroid_z = 0

        for i, pt_guid in enumerate(Pt_TP):
            pt = rs.coerce3dpoint(pt_guid)
            if pt:
                lines.append(f"{pt.X},{pt.Y},{pt.Z}")
                centroid_x += pt.X
                centroid_y += pt.Y
                centroid_z += pt.Z
            else:
                print(f"Punt {i + 1} is geen geldig puntobject.")
                break
        else:
            # Alleen als alle 4 succesvol zijn
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
