# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 18:57:28 2025

@author: beinv
"""

from scipy.integrate import cumulative_trapezoid as cumtrapz
import matplotlib.pyplot as plt
import numpy as np

#w
def doorbuiging(w_acc, Lengte_schip):
    w = w_acc + C
    w[0]=0
    w[-1]=0
    plt.plot(Lengte_schip, w_acc, label="doorbuiging", color='red')
    plt.fill_between(Lengte_schip, w, alpha=0.3, color='red')
    plt.set_xlabel("Lengte van het schip L [m]")
    plt.set_ylabel(" Doorbuiging []")
    plt.set_title("Vervorming")
    plt.legend()
    plt.grid()
    plt.show()
    return w_acc




    

