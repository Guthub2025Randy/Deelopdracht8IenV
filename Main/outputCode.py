# -*- coding: utf-8 -*-
"""
Created on Wed May  7 11:08:35 2025

@author: CWMaz
"""
from bibliotheek import *

def outputKraan(swlmax, gewichttransitionpiece, lengte_kraan_fundatie, draaihoogte_kraan, jib_length, zwenkhoek, giekhoek, lcg_tp, tcg_tp, vcg_tp, lcg_kraanhuis, tcg_kraanhuis, vcg_kraanhuis, lcg_kraanboom, tcg_kraanboom, vcg_kraanboom, lcg_heisgerei, tcg_heisgerei, vcg_heisgerei, versienummer):
    """
    Deze functie regelt de output voor alles wat met de kraan te maken heeft en zet het op de juiste plek in het antwoordenblad
    """
    bestandspad = "Antwoordenblad_MT1463_1466_V0{0}.xlsx".format(versienummer)

    wb = load_workbook(bestandspad)

    ws = wb.active 
    
    ws["D65"] = swlmax # swlmax van de kraan
    ws["D67"] = gewichttransitionpiece #gewicht per transition piece
    ws["D69"] = lengte_kraan_fundatie #lengte_kraanfundatie 
    ws["D70"] = draaihoogte_kraan #draaihoogte_kraan
    ws["D71"] = jib_length# kraanboom lengte
    ws["D72"] = zwenkhoek #zwenkhoek
    ws["D73"] = giekhoek #giekhoek
    ws["D75"] = lcg_heisgerei #lcg van de kraanlast
    ws["D76"] = tcg_heisgerei #tcg van de kraanlast
    ws["D77"] = vcg_heisgerei #vcg van de kraanlast
    ws["D79"] = lcg_kraanhuis #lcg_kraanhuis
    ws["D80"] = tcg_kraanhuis #tcg_kraanhuis
    ws["D81"] = vcg_kraanhuis #vcg_kraanhuis
    ws["D83"] = lcg_kraanboom #lcg_kraanboom
    ws["D84"] = tcg_kraanboom #tcg_kraanboom
    ws["D85"] = vcg_kraanboom #vcg_kraanboom
    ws["D87"] = lcg_heisgerei #lcg_heisgerei
    ws["D88"] = tcg_heisgerei #vcg_heisgerei
    ws["D89"] = vcg_heisgerei #tcg_heisgerei
    
    wb.save(bestandspad)
    return None

def output1(version, entrance_angle_location, r_14knp, gm, dikte_huid_en_dek, loa, b, h, t, trim, heel, dichtheid_staal, dichtheid_water, deplacement, l_c_g, t_c_g, v_c_g, opdrijvendekracht, l_c_b, t_c_b, v_c_b, aantal_transition_pieces, massa_transition_pieces, lcg_tp, tcg_tp, vcg_tp, versienummer):
    """
    deze functie regelt een deel van de output en zorgt er voor dat het op de juiste plek in het excel document komt te staan.
    """
    bestandspad= "Antwoordenblad_MT1463_1466_V0{0}.xlsx".format(versienummer)
    wb = load_workbook(bestandspad)
    ws = wb.active 
    ws["D8"]  = version  #versie 
    ws["D11"] = entrance_angle_location#entrance angle location 
    ws["D12"] = r_14knp #totale weerstand bij 14 knopen
    ws["D16"] = gm #GM
    ws["D19"] = dikte_huid_en_dek #dikte huid en dek
    ws["D22"] = loa #lengte
    ws["D23"] = b #breedte
    ws["D24"] = h #holte
    ws["D25"] = t #diepgang
    ws["D26"] = trim #trim
    ws["D27"] = heel #helling
    ws["D31"] = dichtheid_staal # dichtheid staal
    ws["D32"] = dichtheid_water #dichtheid water
    ws["D36"] = deplacement # deplacement
    ws["D37"] = l_c_g #LCG(x)
    ws["D38"] = t_c_g #TCG(y)
    ws["D39"] = v_c_g #VCG (z)
    ws["D43"] = opdrijvendekracht # opdrijvende kracht
    ws["D44"] = l_c_b #LCB
    ws["D45"] = t_c_b #TCB
    ws["D46"] = v_c_b #VCB
    ws["D49"] = deplacement + opdrijvendekracht #Afwijking van verticaal krachtevenwicht
    ws["D50"] = deplacement*(l_c_g - l_c_b) #Afwijking van longitudinaal momentevenwicht
    ws["D51"] = deplacement*(t_c_g - t_c_b)#Afwijking van transversaal momentevenwicht
    ws["D55"] = aantal_transition_pieces
    ws["D56"] = massa_transition_pieces
    ws["D57"] = lcg_tp
    ws["D58"] = tcg_tp
    ws["D59"] = vcg_tp
    wb.save(bestandspad)
    return None

def outputGlobaleSterkte(maximaal_moment, lmmilvda, maximale_afschuiving, lmailvda, maximale_doorbuiging, lmdilvda, versienummer):
    """
    deze functie regelt de output van de globale sterkte waarden en zet ze op de juiste plek in de excel sheet
    """
    bestandspad = "Antwoordenblad_MT1463_1466_V0{0}.xlsx".format(versienummer)
    wb = load_workbook(bestandspad)
    ws = wb.active
    ws["D92"] = maximaal_moment 
    ws["D93"] = lmmilvda #Locatie Maximaal moment in lengte vanaf de achterloodlijn
    ws["D94"] = maximale_afschuiving
    ws["D95"] = lmailvda #Locatie Maximale afschuiving in lengte vanaf de achterloodlijn
    ws["D96"] = maximale_doorbuiging
    ws["D97"] = lmdilvda #Locatie Maximale doorbuiging in lengte vanaf de achterloodlijn
    wb.save(bestandspad)
    return None

