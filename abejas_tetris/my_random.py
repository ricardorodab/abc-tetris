#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "José Ricardo Rodríguez Abreu"
__email__ = "ricardo_rodab@ciencias.unam.mx"

import random

def set_random(semilla):
    """ Asigna una semilla al generador de números aleatorios. """
    global my_random
    random.seed(a=semilla, version=2)
    my_random = random.Random(semilla)
    
def get_random():
    """ Regresa de forma pseudoaleatoria un número entre 0 y 1. """
    return my_random.random()

def get_randrange(number):
    """ Regresa un número dentro de un rango. """
    return my_random.randrange(number)  

def get_randbits(number):
    """ Usamos esta función para obtener booleanos. """
    return my_random.getrandbits(number)