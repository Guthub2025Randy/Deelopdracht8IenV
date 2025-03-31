# -*- coding: utf-8 -*-
"""
Created on Mon Mar 31 14:07:00 2025

@author: randy
"""
from scipy.integrate import cumulative_trapezoid as cumtrapz
import matplotlib.pyplot as plt
import numpy as np

def Buigend_Moment(F_x,Lengte_schip):
    buigend_moment = cumtrapz(F_x, Lengte_schip, initial=0)
    buigend_moment[0]=0
    buigend_moment[-1]=0
    plt.plot(Lengte_schip, buigend_moment, label="Dwarskracht F(x)", color="yellow")
    plt.fill_between(Lengte_schip, buigend_moment, alpha=0.3, color="yellow")
    plt.set_xlabel("Lengte van het schip L [m]")
    plt.set_ylabel("Buigend moment M(x) [Nm]")
    plt.set_title("Buigend moment grafiek")
    plt.legend()
    plt.grid()
    plt.show
    return buigend_moment