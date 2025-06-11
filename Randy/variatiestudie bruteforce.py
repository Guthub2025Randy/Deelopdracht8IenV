# -*- coding: utf-8 -*-
"""
Created on Wed Jun 11 12:03:48 2025

@author: randy
"""
import numpy as np
import matplotlib.pyplot as plt
versies = np.array([1,2,3])
# Op breedte 24m en diepgang 8m gaat lengte van 150m naar 110m in 2 stappen van 20m
lengtes = np.array([(150/150)*100, (130/150)*100, (110/150)*100])
gm_en_lengtes = np.array([2.5906070866876174, 2.172850055672193, 1.3979797657346669])
weerstanden_lengtes = np.array([470550.31263808085, 477329.4567149492, 503934.5567325815])
# Op lengte 150m en diepgang 8m gaat breedte van 24m naar 23m in 2 stappen van 0.5m
breedtes = np.array([(24/24)*100, (23.5/24)*100, (23/24)*100])
gm_en_breedtes = np.array([2.5906070866876174, 2.2855958196115598, 1.9802653094479734])
weerstanden_breedtes = np.array([470550.31263808085, 465259.2588756564, 459903.2857414512])
# Op lengte 150m en breedte 24m gaat diepgang van 8m naar 9m in 2 stappen van 0.5m
diepgangen = np.array([(8/8)*100, (8.5/8)*100, (9/8)*100])
gm_en_diepgangen = np.array([2.5906070866876174, 2.4451017228457457, 2.1395631946210716])
weerstanden_diepgangen = np.array([470550.31263808085, 508934.3087764771, 566803.5222911664])

plt.plot(lengtes, gm_en_lengtes, label="G_M lengte variatie")
plt.plot(breedtes, gm_en_breedtes, label="G_M breedte variatie")
plt.plot(diepgangen, gm_en_diepgangen, label="G_M diepgang variatie")
plt.xlabel("Variatiewaardes [% van start]")
plt.ylabel("Stabiliteitswaarde: G_M [m]")
plt.grid()
plt.legend()
plt.show()
plt.close()

plt.plot(lengtes, weerstanden_lengtes, label="Weerstand lengte variatie")
plt.plot(breedtes, weerstanden_breedtes, label="Weerstand breedte variatie")
plt.plot(diepgangen, weerstanden_diepgangen, label="Weerstand diepgang variatie")
plt.xlabel("Variatiewaardes [% van start]")
plt.ylabel("Weerstanden [N]")
plt.grid()
plt.legend()
plt.show()
plt.close()