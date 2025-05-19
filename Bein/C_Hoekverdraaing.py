# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 15:01:23 2025

@author: beinv
"""
from scipy.integrate import cumulative_trapezoid as cumtrapz
import matplotlib.pyplot as plt
import numpy as np



# hoekverdraaing (phi) = phi_accent + C
# Doorbuiging (w) = w_acc +C
# Dus C berekenen:

C = - (doorbuiging_acc(Lengte_schip) / Lengte_schip)

#phi
def hoekverdraaiing(phi_acc, Lengte_schip, C):
    phi = phi_acc + C
    phi[0]=0
    phi[-1]=0
    plt.plot(Lengte_schip, phi, label="hoekverdraaiing", color='yellow')
    plt.fill_between(Lengte_schip, phi, alpha=0.3, color='yellow')
    plt.set_xlabel("Lengte van het schip L [m]")
    plt.set_ylabel(" φ(x) [deg]")
    plt.set_title("Hoek in graden")
    plt.legend()
    plt.grid()
    plt.show()
    return phi
