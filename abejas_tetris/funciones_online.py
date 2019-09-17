#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "José Ricardo Rodríguez Abreu"
__email__ = "ricardo_rodab@ciencias.unam.mx"
import abejas_tetris
import math
from abejas_tetris.tetris.movimiento import *
from abejas_tetris.my_random import get_random, get_randrange, get_randbits
import logging
PESO_HORIZONTALIDAD = 1
PESO_ATRAPADOS = 1
PESO_CUBIERTOS = 1
PESO_FILA_REMOVIDA = 1
PESO_ALTURA = 1
PESO_VULNERABLE = 1
FUNCION = None

def set_pesos(data):
    global PESO_HORIZONTALIDAD
    global PESO_ATRAPADOS
    global PESO_CUBIERTOS
    global PESO_FILA_REMOVIDA
    global PESO_ALTURA
    global PESO_VULNERABLE
    global FUNCION
    PESO_HORIZONTALIDAD = data['peso_horizontalidad'] 
    PESO_ATRAPADOS = data['peso_atrapados']
    PESO_CUBIERTOS = data['peso_cubiertos']
    PESO_FILA_REMOVIDA = data['peso_fila_removida']
    PESO_ALTURA = data['peso_altura']
    PESO_VULNERABLE = data['peso_vulnerable']
    logging.getLogger().setLevel('INFO')
    FUNCION = data['funcion']
    if FUNCION == 'pesos':
        logging.info('Se usará Pesos entre pesos negativo.')
    elif FUNCION == 'skyline':
        logging.info('Se usará raining skyline.')
    else:
        logging.info('Se usará una combinación de ambas funciones.')
    
def funcion_nectar_online(fuente):
    if fuente.game_over() and fuente.num_tetris() > 100:
        return math.inf
    elif FUNCION == 'pesos':
        return filas_pesos_negativos(fuente)
    elif FUNCION == 'skyline':
        return skyline(fuente)
    else:
        return hibrido(fuente)

def hibrido(fuente):
    skyline_val = skyline(fuente)
    
    cubiertos_val = (cuenta_cubiertos(fuente) + 1)
    cubiertos_val = PESO_CUBIERTOS * cubiertos_val
    
    num_tetris_val = num_tetris(fuente)

    return (skyline_val * (num_tetris_val + 1)) / (cubiertos_val + 1)

def skyline(fuente):
    # Ponderado:
    total = get_total_convexo_ponderado(fuente.get_ancho(), fuente.get_altura())
    disponibles = cuenta_descubiertos(fuente) 
    return (disponibles / total) * (1 + num_tetris(fuente))

    # No ponderado:
    #total = get_total_convexo_no_ponderado(fuente.get_ancho(), fuente.get_altura())
    #disponibles = cuenta_descubiertos_no_ponderado(fuente) 
    #return (disponibles / total) 


# Ganancia de cada fuente
def filas_pesos_negativos(fuente):
    global PESO_HORIZONTALIDAD
    global PESO_ATRAPADOS
    global PESO_CUBIERTOS
    global PESO_FILA_REMOVIDA
    global PESO_ALTURA
    global PESO_VULNERABLE
    global FUNCION
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

    if (horizontal + atrapados + cubiertos + altura) == 0:
        return 0

    return (1 + num_tetris_var) / (horizontal + atrapados + cubiertos + altura)

# Explotar las abejas empleadas el tablero
def explota_tablero(fuente):
    funcion_buscar_fuente_online(fuente)
    return funcion_nectar_online(fuente)

# Como buscar una fuente
def funcion_buscar_fuente_online(fuente, coloca_pieza=True):
    lista_piezas = abejas_tetris.get_piezas()
    if fuente.game_over() or fuente.piezas_jugadas() == len(lista_piezas):
        fuente.set_game_over(True)
        return
    if fuente.requiere_pieza() and coloca_pieza:
        pieza = lista_piezas[fuente.piezas_jugadas()]
        fuente.set_pieza(tipo=pieza)
    condicion_termino = fuente.requiere_pieza()
    while not condicion_termino:
        fuente.mueve_o_fija()
        condicion_termino = fuente.requiere_pieza()

# Como observar y buscar fuentes vecindades
def funcion_observacion_online(fuente, delta):
    fuente_clon = fuente.clona()
    if fuente.game_over():
        return fuente_clon
    fuente_clon.elimina_historial(delta)
    funcion_buscar_fuente_online(fuente_clon, True)
    return fuente_clon

# Función de ejecución posterior a cada fuente.
def funcion_limpiadora(fuente):
    fuente.limpia()

def num_tetris(fuente):
    return fuente.puede_limpiar() + fuente.num_tetris()

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

# Funciones auxiliares del raining skyline no ponderado

def cuenta_descubiertos_no_ponderado(fuente):
    total = 0
    x = fuente.get_ancho()
    y = fuente.get_altura()
    for i in range(x):
        total = total + get_altura_nop(i, y, fuente)
    return total

def get_altura_nop(x, y, fuente):
    for i in range(y):
        if fuente.get_casilla(x, i) != None:
            return get_altura_no_ponderada(x, i - 1, fuente) 
    return get_altura_no_ponderada(x, y - 1, fuente)

def get_altura_no_ponderada(x, y, fuente):
    if y < 0:
        return 0
    if y == 0:
        return 1
    return 1 + get_altura_no_ponderada(x, y - 1, fuente) 

def get_total_convexo_no_ponderado(x, y):
    return x * y

# Funciones auxiliares del raining skyline ponderado

def cuenta_descubiertos(fuente):
    total = 0
    x = fuente.get_ancho()
    y = fuente.get_altura()
    for i in range(x):
        total = total + get_altura(i, y, fuente)
    return total

def get_altura(x, y, fuente):
    for i in range(y):
        if fuente.get_casilla(x, i) != None:
            return get_altura_ponderada(i - 1, fuente) 
    return get_altura_ponderada(y - 1, fuente)

def get_altura_ponderada(y, fuente):
    if y < 0:
        return 0
    if y == 0:
        return fuente.get_altura()
    return (fuente.get_altura() - y) + get_altura_ponderada(y - 1, fuente) 
     
def get_total_convexo_ponderado(x, y):
    if y == 0:
        return x
    return ((y + 1) * x) + get_total_convexo_ponderado(x, y - 1) 