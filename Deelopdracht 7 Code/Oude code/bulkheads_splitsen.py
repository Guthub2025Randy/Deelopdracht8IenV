# -*- coding: utf-8 -*-
"""
Created on Tue Mar  4 13:34:21 2025

@author: randy
"""

from bibliotheek import *
from input_code import *

def bulkhead2(bulkhead_dataframe):
    bulkhead2 = {}
    bulkheadandere = {}
    for i in range(len(bulkhead_dataframe)):
        bulkhead_teller = f"bulkhead_{i+1}"
        bulkhead_data = bulkhead_dataframe.iloc[i, :].to_numpy()
        tcg_waarde = bulkhead_dataframe.iloc[i, 2]
        if tcg_waarde == 0:
            bulkhead2[bulkhead_teller] = bulkhead_data
        else:
            bulkheadandere[bulkhead_teller] = bulkhead_data
    return bulkhead2, bulkheadandere