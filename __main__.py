#!/usr/bin/env python
# -*- coding: utf-8 -*-
from abejas_tetris.abejas_tetris import *
from abejas_tetris.parse_config import *
from abejas_tetris.my_random import get_random, get_randrange, get_randbits, set_random
import re,sys, os
import logging

mejor_historial = None

def copia_historial(historial, i):
    salida = 'soluciones/solucion' + str(i) + '.txt'
    global mejor_historial
    """ Si se experimenta, se desea guardar el mejor. """
    mejor_historial = []
    for i in historial:
        mejor_historial.append(i)
    if os.path.exists(salida):
        os.remove(salida)
    f = open (salida,'w')
    f.write(str(mejor_historial))
    f.close()

def lee_historia(ruta):
    historia_move = []
    file = open(ruta, "r")
    lineas = file.readlines()
    for linea in lineas:
        moves_lista = linea.split(',')
        for m in moves_lista:
            tmp = m.replace('[', '').replace(']', '').replace(' ', '')
            if tmp == '<Movimiento.DER:1>':
                historia_move.append(Movimiento.DER)
            elif tmp == '<Movimiento.IZQ:2>':
                historia_move.append(Movimiento.IZQ)
            elif tmp == '<Movimiento.CAE:3>':
                historia_move.append(Movimiento.CAE)
            elif tmp == '<Movimiento.GIR:4>':
                historia_move.append(Movimiento.GIR)
            elif tmp == '<Movimiento.FIJ:5>':
                historia_move.append(Movimiento.FIJ)
            else:
                raise Exception("No se puede leer el movimiento.")
    return historia_move

def set_logging(level):
    """ Crea un loggin para leer en terminal. """
    logging.basicConfig()
    level = None
    if level == 'INFO':
        level = logging.INFO
    elif level == 'DEBUG':
        level = logging.DEBUG
    elif level == 'WARN':
        level = logging.WARN
    else:
        level = logging.INFO
    logging.getLogger().setLevel(level)
        

def get_fichas(path="./etc/fichas.csv"):
    """ Regresa las fichas en forma de lista de cadenas. """
    fichas_lista = []
    file = open(path, "r")
    lineas = file.readlines()
    for linea in lineas:
        fichas_lista = linea.split(',')
    return fichas_lista

def get_config_hash():
    """ Regresa los parámetros principales. """
    return get_config("./etc/config.cfg")

def get_juego(data):
    """ Regresa una instancia de la inferfaz de heurística-juego. """
    online = data['online']
    size_colmena = data['size_colmena']
    limite_it = data['limite_it']
    delta = data['delta']
    alto = data['alto']
    ancho = data['ancho']
    abc = Abejas_Tetris(online=online, size_colmena=size_colmena, limite_it=limite_it, delta=delta, alto=alto, ancho=ancho)
    abc.set_lista_piezas(get_fichas())
    return abc

def imprime_datos(solucion):
    """ Imprime en pantalla algunos datos del tablero. """
    nectar_local = funcion_nectar_online(solucion)
    piezas_local = solucion.piezas_jugadas()
    logging.info('Nectar final: ' + str(nectar_local))
    logging.info('Piezas jugadas: ' + str(piezas_local))
    logging.info('Filas eliminadas: ' + str(solucion.num_tetris()))
    solucion.imprime_tablero()

def busca_semilla(data):
    """ Busca las mejores semillas a jugar. """
    itera_range = data['semilla_itera']
    semillero = data['semilla_ubicacion']
    logging.warning('Iniciando busqueda de mejor semilla')
    logging.warning('Este proceso puede tardar dependiendo de la variable SEMILLA_ITERA')
    semilla = 0
    nectar = 0
    piezas = 0
    it = 0
    file = open(semillero, "r")
    lineas = file.readlines()
    for linea in lineas:
        fichas_lista = linea.split(',')
        for r in range(itera_range):
            sem = fichas_lista[r]
            set_random(int(sem))
            abc = get_juego(data)
            if data['online']:
                iteraciones = data['iteraciones']
                limpia = data['limpieza']
                solucion = abc.juega_online(iteraciones=iteraciones, limpieza=limpia)
                nectar_local = funcion_nectar_online(solucion)
                piezas_local = solucion.piezas_jugadas()
                it = it + 1
                if (it % 5) == 0:
                    logging.info('Semillas probadas: ' + str(it))
                cond1 = nectar_local > nectar
                cond2 = nectar_local == nectar and piezas < piezas_local
                if cond1 or cond2:
                    logging.info('Semilla mejorada: ' + str(sem))
                    logging.info('Nectar final: ' + str(nectar_local))
                    logging.info('Piezas jugadas: ' + str(piezas_local))
                    eli = solucion.num_tetris()
                    logging.info('Filas eliminadas: ' + str(eli))
                    copia_historial(solucion.get_historial(), r)
                    nectar = nectar_local
                    semilla = int(sem)
                    piezas = piezas_local
    logging.info('La mejor semilla encontrada es: ' + str(semilla))
    return semilla

def set_random_local(data):
    """ Asigna una semilla al generador de números aleatorios. """
    semilla = data['semilla']
    if not data['random_var']:
        if semilla == -1:
            semilla = busca_semilla(data)
        set_random(semilla)
    else:
        set_random(semilla=None)

# Punto de entrada del proyecto:
if __name__ == "__main__":
    data = get_config_hash()

    set_logging(data['logging_level'])
    set_random_local(data)
    abc = get_juego(data)
    
    if data['interactivo']:
        abc.interactivo()
    elif data['reproduccion_previa']:
        historial_muestra = lee_historia(data['solucion_previa'])
        filename, file_extension = os.path.splitext(data['solucion_previa'])
        filename = filename + '.csv'
        if os.path.exists(filename):
            abc.set_lista_piezas(get_fichas(filename))
        abc.pinta_historia(historial_muestra)
    elif mejor_historial != None and data['gui']:
        abc.pinta_historia(mejor_historial)
    elif data['online']:
        it = data['iteraciones']
        limpia = data['limpieza']
        solucion = abc.juega_online(iteraciones=it, limpieza=limpia)
        imprime_datos(solucion)
        if data['gui']:  
            abc.pinta_solucion(solucion)