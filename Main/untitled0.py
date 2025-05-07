# -*- coding: utf-8 -*-
"""
Created on Tue May  6 13:13:23 2025

@author: randy
"""

import numpy as np
import matplotlib.pyplot as plt

Cf_over_Cm = np.array([1.098,1.138,1.234,1.347,1.427])
Froude_over_Cm = np.array([0.1,0.3,0.5,0.7,0.9])
myfit = np.polyfit(Froude_over_Cm,Cf_over_Cm, 1)

f = np.poly1d(myfit)
x=np.linspace(0,1,1000)
y = f(x)

plt.figure(figsize=(14,14))
plt.plot(x, y, label="Fitlijn om (1+k) te benaderen", linestyle='dashed')
plt.scatter(Froude_over_Cm, Cf_over_Cm, label="Waardes")
plt.xlabel('Froude')
plt.ylabel('Weerstandsdingen')
plt.grid(True)
plt.legend()
plt.title('(1+k) benaderen')
plt.show()
plt.close()