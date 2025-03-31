# -*- coding: utf-8 -*-
"""
Created on Mon Mar 31 14:21:24 2025

@author: randy
"""

from scipy.integrate import cumulative_trapezoid as cumtrapz
import matplotlib.pyplot as plt
import numpy as np

def traagheidsmoment_over_lengte(traagheidsmoment, Lengte_schip):
    plt.plot(Lengte_schip, traagheidsmoment, label="Traagheidsmoment", color='purple')
    plt.fill_between(Lengte_schip, traagheidsmoment, alpha=0.3, color='purple')
    plt.set_xlabel("Lengte van het schip L [m]")
    plt.set_ylabel("Traagheidsmoment I [m4]")
    plt.set_title("Traagheidsmoment grafiek")
    plt.legend()
    plt.grid()
    plt.show()
    return traagheidsmoment