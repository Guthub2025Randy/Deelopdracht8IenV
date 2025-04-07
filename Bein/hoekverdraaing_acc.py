# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 18:57:28 2025

@author: beinv
"""

from scipy.integrate import cumulative_trapezoid as cumtrapz
import matplotlib.pyplot as plt
import numpy as np

# door het gereduceerde moment de integreren krijg je de verdraaiing accent (phi accent)
def hoekverdraaiing_acc(Buigend_moment, Lengte_schip):
    phi_accent = cumtrapz(Lengte_schip, Buigend_moment, initial=0)
    phi_accent[0]=0
    phi_accent[-1]=0
    plt.plot(Lengte_schip, phi_accent, label="hoekverdraaiing accent", color='green')
    plt.fill_between(Lengte_schip, phi_accent, alpha=0.3, color='green')
    plt.set_xlabel("Lengte van het schip L [m]")
    plt.set_ylabel(" φ(x)' [deg]")
    plt.set_title("Hoek in graden")
    plt.legend()
    plt.grid()
    plt.show()
    return phi_accent