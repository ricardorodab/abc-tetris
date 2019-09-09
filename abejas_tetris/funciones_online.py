#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "José Ricardo Rodríguez Abreu"
__email__ = "ricardo_rodab@ciencias.unam.mx"
import abejas_tetris
import math
from abejas_tetris.my_random import get_random, get_randrange, get_randbits

PESO_HORIZONTALIDAD = 1
PESO_ATRAPADOS = 1
PESO_CUBIERTOS = 1
PESO_FILA_REMOVIDA = 1
PESO_ALTURA = 1
PESO_VULNERABLE = 1

def set_pesos(data):
    PESO_HORIZONTALIDAD = data['peso_horizontalidad'] 
    PESO_ATRAPADOS = data['peso_atrapados']
    PESO_CUBIERTOS = data['peso_cubiertos']
    PESO_FILA_REMOVIDA = data['peso_fila_removida']
    PESO_ALTURA = data['peso_altura']
    PESO_VULNERABLE = data['peso_vulnerable']

# Ganancia de cada fuente
def funcion_nectar_online(fuente):
    #Entre menor, mejor.
    atrapados = cuenta_atrapados(fuente)
    # Entre menor, mejor.
    horizontal = horizontalidad(fuente)
    # Entre mayor, mejor.
    num_tetris_var = num_tetris(fuente)
    # Entre menor, mejor.
    cubiertos = cuenta_cubiertos(fuente)
    # La altura siempre debe ser baja
    altura = fuente.altura_maxima()
    # La funcion, entre mayor, mejor.
    
    horizontal = PESO_HORIZONTALIDAD * horizontal
    atrapados = PESO_ATRAPADOS * atrapados
    cubiertos = PESO_CUBIERTOS * cubiertos
    num_tetris_var = PESO_FILA_REMOVIDA * num_tetris_var
    altura =  PESO_ALTURA * altura 

    return (1 + num_tetris_var) / (horizontal + atrapados + cubiertos + altura)

# Explotar las abejas empleadas el tablero
def explota_tablero(fuente):
    funcion_buscar_fuente_online(fuente)
    return funcion_nectar_online(fuente)

# Como buscar una fuente
def funcion_buscar_fuente_online(fuente):
    if fuente.game_over():
        return
    lista_piezas = abejas_tetris.get_piezas()
    if fuente.requiere_pieza():
        pieza = lista_piezas[fuente.piezas_jugadas()]
        fuente.set_pieza(tipo=pieza)
    while not fuente.requiere_pieza():
        fuente.mueve_o_fija()

# Como observar y buscar fuentes vecindades
def funcion_observacion_online(fuente, delta):
    if fuente.game_over():
        return fuente
    fuente_clon = fuente.clona()
    fuente_clon.elimina_historial(delta)
    funcion_buscar_fuente_online(fuente_clon)
    return fuente_clon

# Función de ejecución posterior a cada fuente.
def funcion_limpiadora(fuente):
    fuente.limpia()

"""
    FUNCIONES AUXILIARES:
"""

def horizontalidad(fuente):
    altura_max = fuente.altura_maxima()
    altura_min = fuente.altura_minima()
    return abs(altura_max - altura_min)

def cuenta_atrapados(fuente):
    return fuente.cuenta_atrapados()

def cuenta_cubiertos(fuente):
    return fuente.cuenta_cubiertos()

def num_tetris(fuente):
    return fuente.num_tetris()