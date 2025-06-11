# -*- coding: utf-8 -*-
"""
Created on Wed Jun 11 12:03:48 2025

@author: randy
"""
import numpy as np
import matplotlib.pyplot as plt
versies = np.array([1,2,3])
# Op breedte 24m en diepgang 8m gaat lengte van 150m naar 110m in 8 stappen van 5m
lengtes = np.array([(150/150)*100, (145/150)*100, (140/150)*100, (135/150)*100, (130/150)*100, (125/150)*100, (120/150)*100, (115/150)*100, (110/150)*100])
gm_en_lengtes = np.array([2.5906070866876174, 2.512634261539001, 2.425990040243293, 2.3086809977153067, 2.172850055672193, 2.019172468751024, 1.843512664519088, 1.6396117336721652, 1.3979797657346669])
weerstanden_lengtes = np.array([470550.31263808085, 471026.5013250574, 472256.7819833167, 474319.0923626467, 477329.4567149492, 481495.75441586965, 487140.1151660433, 494595.81914087007, 503934.5567325815])
# Op lengte 150m en diepgang 8m gaat breedte van 24m naar 23m in 2 stappen van 0.5m
breedtes = np.array([(24/24)*100, (23.5/24)*100, (23/24)*100])
gm_en_breedtes = np.array([2.5906070866876174, 2.2855958196115598, 1.9802653094479734])
weerstanden_breedtes = np.array([470550.31263808085, 465259.2588756564, 459903.2857414512])
# Op lengte 150m en breedte 24m gaat diepgang van 8m naar 9m in 2 stappen van 0.5m
diepgangen = np.array([(8/8)*100, (8.5/8)*100, (9/8)*100])
gm_en_diepgangen = np.array([2.5906070866876174, 2.4451017228457457, 2.1395631946210716])
weerstanden_diepgangen = np.array([470550.31263808085, 508934.3087764771, 566803.5222911664])
# Op lengte 150m en breedte 24m gaat vrijboord van 7m naar 3m in 8 stappen van 0.5 meter
vrijboorden = np.array([(15/15)*100, (14.5/15)*100, (14/15)*100, (13.5/15)*100, (13/15)*100])
gm_en_vrijboorden = np.array([2.5906070866876174, 2.704295076833025, 2.760370949635864, 2.7611392111401822, 2.707958418676082])
weerstanden_vrijboorden = np.array([470550.31263808085, 475921.2159713482, 494019.88564553135, 515416.8585181488, 539138.0872526139])

plt.plot(lengtes, gm_en_lengtes, label="G_M lengte variatie")
plt.plot(breedtes, gm_en_breedtes, label="G_M breedte variatie")
plt.plot(diepgangen, gm_en_diepgangen, label="G_M diepgang variatie")
plt.plot(vrijboorden, gm_en_vrijboorden, label="G_M vrijboord variatie")
plt.xlabel("Variatiewaardes [% van start]")
plt.ylabel("Stabiliteitswaarde: G_M [m]")
plt.grid()
plt.legend()
plt.show()
plt.close()

plt.plot(lengtes, weerstanden_lengtes, label="Weerstand lengte variatie")
plt.plot(breedtes, weerstanden_breedtes, label="Weerstand breedte variatie")
plt.plot(diepgangen, weerstanden_diepgangen, label="Weerstand diepgang variatie")
plt.plot(vrijboorden, weerstanden_vrijboorden, label="Weerstand vrijboord variatie")
plt.xlabel("Variatiewaardes [% van start]")
plt.ylabel("Weerstanden [N]")
plt.grid()
plt.legend()
plt.show()
plt.close()