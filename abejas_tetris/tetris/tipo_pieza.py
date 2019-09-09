#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "José Ricardo Rodríguez Abreu"
__email__ = "ricardo_rodab@ciencias.unam.mx"
from .casilla import *
from .punto import *
from enum import Enum

class Tipo(Enum):
    I = 1
    RS = 2
    LG = 3
    T = 4
    RG = 5
    LS = 6
    Sq = 7

def instancia_i(pos):
    # La casilla media es 0Ó00
    p2 = Punto(pos.get_x() - 1, pos.get_y())
    p3 = Punto(pos.get_x() + 1, pos.get_y())
    p4 = Punto(pos.get_x() + 2, pos.get_y())
    c1 = Casilla(p2)
    c2 = Casilla(pos)
    c3 = Casilla(p3)
    c4 = Casilla(p4)
    return [c1,c2,c3,c4]

def instancia_rs(pos):
    # La casilla media es:
    #     Ó0
    #    00
    p1 = Punto(pos.get_x() - 1, pos.get_y() + 1)
    p2 = Punto(pos.get_x(), pos.get_y() + 1)
    p4 = Punto(pos.get_x() + 1, pos.get_y())
    c1 = Casilla(p1)
    c2 = Casilla(p2)
    c3 = Casilla(pos)
    c4 = Casilla(p4)
    return [c1,c2,c3,c4]

def instancia_lg(pos):
    # La casilla media es:
    #    0 
    #    Ó00
    p1 = Punto(pos.get_x(), pos.get_y() - 1)
    p3 = Punto(pos.get_x() + 1, pos.get_y())
    p4 = Punto(pos.get_x() + 2, pos.get_y())
    c1 = Casilla(p1)
    c2 = Casilla(pos)
    c3 = Casilla(p3)
    c4 = Casilla(p4)
    return [c1,c2,c3,c4]

def instancia_t(pos):
    # La casilla media es:
    #     0
    #    0Ó0
    p1 = Punto(pos.get_x() - 1, pos.get_y())
    p3 = Punto(pos.get_x(), pos.get_y() - 1)
    p4 = Punto(pos.get_x() + 1, pos.get_y())
    c1 = Casilla(p1)
    c2 = Casilla(pos)
    c3 = Casilla(p3)
    c4 = Casilla(p4)
    return [c1,c2,c3,c4]

def instancia_rg(pos):
    # La casilla media es:
    #      0
    #    00Ó
    p1 = Punto(pos.get_x() - 2, pos.get_y())
    p2 = Punto(pos.get_x() - 1, pos.get_y())
    p4 = Punto(pos.get_x(), pos.get_y() - 1)
    c1 = Casilla(p1)
    c2 = Casilla(p2)
    c3 = Casilla(pos)
    c4 = Casilla(p4)
    return [c1,c2,c3,c4]

def instancia_ls(pos):
    # La casilla media es:
    #    0Ó 
    #     00
    p1 = Punto(pos.get_x() - 1, pos.get_y())
    p3 = Punto(pos.get_x(), pos.get_y() + 1)
    p4 = Punto(pos.get_x() + 1, pos.get_y() + 1)
    c1 = Casilla(p1)
    c2 = Casilla(pos)
    c3 = Casilla(p3)
    c4 = Casilla(p4)
    return [c1,c2,c3,c4]

def instancia_sq(pos):
    # La casilla media es:
    #    Ó0 
    #    00
    p2 = Punto(pos.get_x() + 1, pos.get_y())
    p3 = Punto(pos.get_x(), pos.get_y() + 1)
    p4 = Punto(pos.get_x() + 1, pos.get_y() + 1)
    c1 = Casilla(pos)
    c2 = Casilla(p2)
    c3 = Casilla(p3)
    c4 = Casilla(p4)
    return [c1,c2,c3,c4]

def get_casillas(tipo, posicion):
    if tipo is Tipo.I:
        return instancia_i(posicion)
    elif tipo is Tipo.RS:
        return instancia_rs(posicion)
    elif tipo is Tipo.LG:
        return instancia_lg(posicion)
    elif tipo is Tipo.T:
        return instancia_t(posicion)
    elif tipo is Tipo.RG:
        return instancia_rg(posicion)
    elif tipo is Tipo.LS:
        return instancia_ls(posicion)
    else:
        return instancia_sq(posicion)

def rota_i(casillas):
    # La casilla media es 0Ó00
    p1 = casillas[0].get_punto()
    p2 = casillas[1].get_punto()

    if p1.get_x() == p2.get_x():
        cas = instancia_i(p2)
        np1 = cas[0].get_punto()
        np2 = cas[1].get_punto()
        np3 = cas[2].get_punto()
        np4 = cas[3].get_punto()
        return [np1, np2, np3, np4]

    np1 = Punto(p2.get_x(), p2.get_y() - 1)
    np2 = Punto(p2.get_x(), p2.get_y())
    np3 = Punto(p2.get_x(), p2.get_y() + 1)
    np4 = Punto(p2.get_x(), p2.get_y() + 2)
    return [np1, np2, np3, np4]

def rota_rs(casillas):
    # La casilla media es:
    #     Ó0
    #    00
    p3 = casillas[2].get_punto()
    p4 = casillas[3].get_punto()

    if p3.get_x() == p4.get_x():
        cas = instancia_rs(p3)
        np1 = cas[0].get_punto()
        np2 = cas[1].get_punto()
        np3 = cas[2].get_punto()
        np4 = cas[3].get_punto()
        return [np1, np2, np3, np4]

    np1 = Punto(p3.get_x() - 1, p3.get_y() - 1)
    np2 = Punto(p3.get_x() - 1, p3.get_y())
    np3 = Punto(p3.get_x(), p3.get_y())
    np4 = Punto(p3.get_x(), p3.get_y() + 1)
    return [np1, np2, np3, np4]
    
    
def rota_lg(casillas):
    # La casilla media es:
    #    0 
    #    Ó00
    p1 = casillas[0].get_punto()
    p2 = casillas[1].get_punto()
    p3 = casillas[2].get_punto()

    if p1.get_y() == p2.get_y():
        if p1.get_y() > p3.get_y():
            cas = instancia_lg(p2)
            np1 = cas[0].get_punto()
            np2 = cas[1].get_punto()
            np3 = cas[2].get_punto()
            np4 = cas[3].get_punto()
            return [np1, np2, np3, np4]
        np1 = Punto(p2.get_x(), p2.get_y() + 1)
        np2 = Punto(p2.get_x(), p2.get_y())
        np3 = Punto(p2.get_x() - 1, p2.get_y())
        np4 = Punto(p2.get_x() - 2, p2.get_y())
        return [np1, np2, np3, np4]
    elif p1.get_y() > p2.get_y():
        np1 = Punto(p2.get_x() - 1, p2.get_y())
        np2 = Punto(p2.get_x(), p2.get_y())
        np3 = Punto(p2.get_x(), p2.get_y() - 1)
        np4 = Punto(p2.get_x(), p2.get_y() - 2)
        return [np1, np2, np3, np4]
    else:
        np1 = Punto(p2.get_x() + 1, p2.get_y())
        np2 = Punto(p2.get_x(), p2.get_y())
        np3 = Punto(p2.get_x(), p2.get_y() + 1)
        np4 = Punto(p2.get_x(), p2.get_y() + 2)
        return [np1, np2, np3, np4]

def rota_t(casillas):
    # La casilla media es:
    #     0
    #    0Ó0
    p1 = casillas[0].get_punto()
    p2 = casillas[1].get_punto()
    p3 = casillas[2].get_punto()
    p4 = casillas[3].get_punto()
    
    if p1.get_x() == p4.get_x():
        if p2.get_x() > p3.get_x():
            cas = instancia_t(p2)
            np1 = cas[0].get_punto()
            np2 = cas[1].get_punto()
            np3 = cas[2].get_punto()
            np4 = cas[3].get_punto()
            return [np1, np2, np3, np4]
        np1 = Punto(p2.get_x() + 1, p2.get_y())
        np2 = Punto(p2.get_x(), p2.get_y())
        np3 = Punto(p2.get_x(), p2.get_y() + 1)
        np4 = Punto(p2.get_x() - 1, p2.get_y())
        return [np1, np2, np3, np4]
    elif p3.get_y() > p2.get_y():
        np1 = Punto(p2.get_x(), p2.get_y() + 1)
        np2 = Punto(p2.get_x(), p2.get_y())
        np3 = Punto(p2.get_x() - 1, p2.get_y())
        np4 = Punto(p2.get_x(), p2.get_y() - 1)
        return [np1, np2, np3, np4]
    else:
        np1 = Punto(p2.get_x(), p2.get_y() - 1)
        np2 = Punto(p2.get_x(), p2.get_y())
        np3 = Punto(p2.get_x() + 1, p2.get_y())
        np4 = Punto(p2.get_x(), p2.get_y() + 1)
        return [np1, np2, np3, np4]
    
def rota_rg(casillas):
    # La casilla media es:
    #      0
    #    00Ó
    p1 = casillas[0].get_punto()
    p3 = casillas[2].get_punto()
    p4 = casillas[3].get_punto()

    if p3.get_y() == p4.get_y():
        if p1.get_y() > p3.get_y():
            cas = instancia_rg(p3)
            np1 = cas[0].get_punto()
            np2 = cas[1].get_punto()
            np3 = cas[2].get_punto()
            np4 = cas[3].get_punto()
            return [np1, np2, np3, np4]
        np1 = Punto(p3.get_x() + 2, p3.get_y())
        np2 = Punto(p3.get_x() + 1, p3.get_y())
        np3 = Punto(p3.get_x(), p3.get_y())
        np4 = Punto(p3.get_x(), p3.get_y() + 1)
        return [np1, np2, np3, np4]
    elif p3.get_y() > p4.get_y():
        np1 = Punto(p3.get_x(), p3.get_y() - 2)
        np2 = Punto(p3.get_x(), p3.get_y() - 1)
        np3 = Punto(p3.get_x(), p3.get_y())
        np4 = Punto(p3.get_x() + 1, p3.get_y())
        return [np1, np2, np3, np4]
    else:
        np1 = Punto(p3.get_x(), p3.get_y() + 2)
        np2 = Punto(p3.get_x(), p3.get_y() + 1)
        np3 = Punto(p3.get_x(), p3.get_y())
        np4 = Punto(p3.get_x() - 1, p3.get_y())
        return [np1, np2, np3, np4]
    
def rota_ls(casillas):
    # La casilla media es:
    #    0Ó 
    #     00
    p1 = casillas[0].get_punto()
    p2 = casillas[1].get_punto()

    if p2.get_x() == p1.get_x():
        cas = instancia_ls(p2)
        np1 = cas[0].get_punto()
        np2 = cas[1].get_punto()
        np3 = cas[2].get_punto()
        np4 = cas[3].get_punto()
        return [np1, np2, np3, np4]

    np1 = Punto(p2.get_x(), p2.get_y() - 1)
    np2 = Punto(p2.get_x(), p2.get_y())
    np3 = Punto(p2.get_x() - 1, p2.get_y())
    np4 = Punto(p2.get_x() - 1, p2.get_y() + 1)
    return [np1, np2, np3, np4]

def rota_sq(casillas):
    # La casilla media es:
    #    Ó0 
    #    00
    p1 = casillas[0].get_punto()
    p2 = casillas[1].get_punto()
    p3 = casillas[2].get_punto()
    p4 = casillas[3].get_punto()

    np1 = Punto(p1.get_x(), p1.get_y())
    np2 = Punto(p2.get_x(), p2.get_y())
    np3 = Punto(p3.get_x(), p3.get_y())
    np4 = Punto(p4.get_x(), p4.get_y())
    return [np1, np2, np3, np4]
    
def rota(tipo, casillas):
    if tipo is Tipo.I:
        return rota_i(casillas)
    elif tipo is Tipo.RS:
        return rota_rs(casillas)
    elif tipo is Tipo.LG:
        return rota_lg(casillas)
    elif tipo is Tipo.T:
        return rota_t(casillas)
    elif tipo is Tipo.RG:
        return rota_rg(casillas)
    elif tipo is Tipo.LS:
        return rota_ls(casillas)
    else:
        return rota_sq(casillas)
    
