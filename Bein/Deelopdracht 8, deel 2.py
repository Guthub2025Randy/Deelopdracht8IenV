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

# hoekverdraaing (phi) = phi_accent + C
# Doorbuiging (w) = w_acc +C
# Dus C berekenen:

C = - (doorbuiging_acc[n-1] / Lengte_schip)

#phi
def hoekverdraaiing(phi_acc, Lengte_schip):
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




    

