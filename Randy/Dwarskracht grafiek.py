# -*- coding: utf-8 -*-
"""
Created on Mon Mar 31 14:07:00 2025

@author: randy
"""
from scipy.integrate import cumulative_trapezoid as cumtrapz
import matplotlib.pyplot as plt
import numpy as np

def dwarskracht(q_x,Lengte_schip):
    dwarskracht = cumtrapz(q_x, Lengte_schip, initial=0)
    dwarskracht[0]=0
    dwarskracht[-1]=0
    plt.plot(Lengte_schip, dwarskracht, label="Dwarskracht F(x)", color="orange")
    plt.fill_between(Lengte_schip, dwarskracht, alpha=0.3, color="orange")
    plt.set_xlabel("Lengte van het schip L [m]")
    plt.set_ylabel("Dwarskracht F(x) [N]")
    plt.set_title("Dwarskracht grafiek")
    plt.legend()
    plt.grid()
    plt.show
    return dwarskracht