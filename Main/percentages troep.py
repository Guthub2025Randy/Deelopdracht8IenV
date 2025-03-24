# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 12:43:55 2025

@author: randy
"""

momentdic = d1['vol_1'] * d1['tcg_1'] * WEIGHT_WATER
vulperc1dic = d1['vulling_%_1'][:7]
vulperc1ip = ip.interp1d(momentdic,vulperc1dic, kind = "cubic")
vulperc1 = vulperc1ip(momentensom1_[0])
vulperc2ip = ip.interp1d(d2['vol_2'], d2['vulling_%_2'][:7], kind = "cubic")
vulperc2 = vulperc2ip(volume_t2)
vulperc3ip = ip.interp1d(d3['vol_3'], d3['vulling_%_3'][:7], kind = "cubic")
vulperc3 = vulperc3ip(volume_t3)