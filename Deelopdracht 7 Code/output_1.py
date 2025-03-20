# -*- coding: utf-8 -*-
"""
Created on Fri Mar  7 09:28:28 2025

@author: CWMaz
"""
from bibliotheek import *

def output_1(version,entrance_angle_location,R_14knp,gm,dikte_huid_en_dek,loa,B,H,T,trim,heel,dichtheid_staal,dichtheid_water,Deplacement,L_C_G,T_C_G,V_C_G,opdrijvendekracht,L_C_B,T_C_B,V_C_B,DVF,DLM,DTM,aantal_transition_pieces,massa_transition_pieces,lcg_tp,tcg_tp,vcg_tp):
    bestandspad= "Antwoordenblad_MT1463_1466_V03 .xlsx"
    wb= load_workbook(bestandspad)
    ws=wb.active 
    ws["D8"]  = version  #versie 
    ws["D11"] = entrance_angle_location#entrance angle location 
    ws["D12"] = R_14knp #totale weerstand bij 14 knoop
    ws["D16"] = gm #GM
    ws["D19"] = dikte_huid_en_dek #dikte huid en dek
    ws["D22"] = loa #lengte
    ws["D23"] = B #breedte
    ws["D24"] = H #holte
    ws["D25"] = T #diepgang
    ws["D26"] = trim #trim
    ws["D27"] = heel #helling
    ws["D31"] = dichtheid_staal # dichtheid staal
    ws["D32"] = dichtheid_water #dichtheid water
    ws["D36"] = Deplacement # deplacement
    ws["D37"] = L_C_G #LCG(x)
    ws["D38"] = T_C_G #TCG(y)
    ws["D39"] = V_C_G #VCG (z)
    ws["D43"] = opdrijvendekracht # opdrijvende kracht
    ws["D44"] = L_C_B #LCB
    ws["D45"] = T_C_B #TCB
    ws["D46"] = V_C_B #VCB
    ws["D49"] = DVF#Afwijking van verticaal krachtevenwicht
    ws["D50"] = DLM#Afwijking van longitudinaal momentevenwicht
    ws["D51"] = DTM#Afwijking van transversaal momentevenwicht
    ws["D55"] = aantal_transition_pieces
    ws["D56"] = massa_transition_pieces
    ws["D57"] = lcg_tp
    ws["D58"] = tcg_tp
    ws["D59"] = vcg_tp
    wb.save(bestandspad)
    return None