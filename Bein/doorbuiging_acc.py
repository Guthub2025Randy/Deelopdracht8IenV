# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 15:01:11 2025

@author: beinv
"""

from scipy.integrate import cumulative_trapezoid as cumtrapz
import matplotlib.pyplot as plt
import numpy as np


# door de verdraaing accent (phi accent) te integreren krijg je de doorbuigin accent (w')

def doorbuiging_acc(phi_accent, Lengte_schip):
    w_acc = cumtrapz(Lengte_schip, phi_accent, initial =0 )
    w_acc[0]=0
    w_acc[-1]=0
    plt.plot(Lengte_schip, w_acc, label="doorbuiging accent", color='brown')
    plt.fill_between(Lengte_schip, w_acc, alpha=0.3, color='brown')
    plt.set_xlabel("Lengte van het schip L [m]")
    plt.set_ylabel(" Doorbuiging accent []")
    plt.set_title("Vervorming")
    plt.legend()
    plt.grid()
    plt.show()
    return w_acc