# -*- coding: utf-8 -*-
"""Remove_buoyancy_functie.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/13qWapaUVkj6Pm3NP0UH2IpNn_ACqd_eE
"""

import numpy as np
def remove_buoyant_force(lijst_positie, lijst_krachten, Center_buoyancy, kracht_opdrijvend):
  """
  Deze functie haalt de COB en de opdrijvende kracht uit de lijsten met alle massa's en alle posities,
  zodat hiermee de totale zwaartepunten kunnen worden bepaald. De COB moet doorgegeven worden als array en de opdrijvende kracht
  als float.
  """
  lijst_positie = [arr for arr in lijst_positie if not np.array_equal(arr, Center_buoyancy)]
  for element in lijst_krachten:
    if element == kracht_opdrijvend:
      lijst_krachten.remove(element)
      break
  return lijst_positie, lijst_krachten