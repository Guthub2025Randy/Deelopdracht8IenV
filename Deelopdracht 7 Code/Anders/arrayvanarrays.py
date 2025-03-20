# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 13:59:12 2025

@author: randy
"""
from bibliotheek import *

def bulkheadchecker(positie,teller):
    if positie[1] != 0:
        teller += 1
        return teller, positie
    else:
        return teller, None

def bulkheadcheker2(*posities):
    lengte = 0
    bulkheads = []
    bulkheadsvan2 = []
    for positie in posities:
        teller, bulkhead = bulkheadchecker(positie, lengte)
        if bulkhead is not None:
            bulkheads.append(bulkhead)
        else:
            bulkheadsvan2.append(positie)
    
    return lengte, np.array(bulkheads), np.array(bulkheadsvan2)

def arrayvanarrays(*krachtenenposities):
    
    
    
    return krachtenarray, momentenarray