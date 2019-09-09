#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "José Ricardo Rodríguez Abreu"
__email__ = "ricardo_rodab@ciencias.unam.mx"

import configparser
from abejas_tetris.funciones_online import set_pesos

def parse_tipos(config):
    size_colmena = int(config['size'])
    limite_it = int(config['limite'])
    if config['iteraciones'] == 'None':
        iteraciones = None
    else:    
        iteraciones = int(config['iteraciones'])
    delta = float(config['delta'])
    modo = str(config['modo'])
    alto = int(config['alto'])
    ancho = int(config['ancho'])
    semilla = int(config['semilla'])
    semilla_itera = int(config['semilla_itera'])
    semilla_ubicacion = str(config['ubicacion'])
    bool_value = {'True' : True, 'False' : False}
    random_var = bool_value[config['random']]
    gui = bool_value[config['visualizar_resultado']]
    online = (modo == 'online')
    logging_level = config['logging_level']
    interactivo = bool_value[config['interactivo']]
    peso_horizontalidad = int(config['peso_horizontalidad'])
    peso_atrapados = int(config['peso_atrapados'])
    peso_cubiertos = int(config['peso_cubiertos'])
    peso_fila_removida = int(config['peso_fila_removida'])
    peso_altura = int(config['peso_altura'])
    peso_vulnerable = int(config['peso_vulnerable'])
    
    data = {
        'online' : online,
        'size_colmena' : size_colmena,
        'limite_it' : limite_it,
        'delta' : delta,
        'alto' : alto,
        'ancho' : ancho,
        'iteraciones' : iteraciones,
        'modo' : modo,
        'semilla' : semilla,
        'semilla_itera' : semilla_itera,
        'semilla_ubicacion' : semilla_ubicacion,
        'random_var' : random_var,
        'gui' : gui,
        'online' : online,
        'logging_level' : logging_level,
        'interactivo' : interactivo,
        'peso_horizontalidad' : peso_horizontalidad,
        'peso_atrapados' : peso_atrapados,
        'peso_cubiertos' : peso_cubiertos,
        'peso_fila_removida' : peso_fila_removida,
        'peso_altura' : peso_altura,
        'peso_vulnerable' : peso_vulnerable
    }

    return data

def get_config(path):
    config = configparser.ConfigParser()
    config.read(path)
    data = {}
    for seccion in config.sections():
        for key in config[seccion]:
            data[key] = config[seccion][key]
    resultado = parse_tipos(data)
    set_pesos(resultado)
    return resultado
