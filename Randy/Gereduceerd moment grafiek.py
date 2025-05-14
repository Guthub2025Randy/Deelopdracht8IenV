    # -*- coding: utf-8 -*-
"""
Created on Mon Mar 31 14:40:50 2025

@author: randy
"""
from scipy.integrate import cumulative_trapezoid as cumtrapz
import matplotlib.pyplot as plt
import numpy as np

def gereduceerde_moment(buigend_M, traagheids_M, Elastiteitsmodulus, Lengte_schip):
    Gereduceerd_moment = buigend_M/(traagheids_M*Elastiteitsmodulus)
    plt.plot(Lengte_schip, Gereduceerd_moment, label="Gereduceerde Moment", color='red')
    plt.fill_between(Lengte_schip, Gereduceerd_moment, alpha=0.3, color='red')
    plt.set_xlabel("Lengte van het schip L [m]")
    plt.set_ylabel("Gereduceerd moment M'(x) [Nm]")
    plt.set_title("Gereduceerd moment grafiek")
    plt.legend()
    plt.grid()
    plt.show()
    return Gereduceerd_moment