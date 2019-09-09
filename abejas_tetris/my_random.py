#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "José Ricardo Rodríguez Abreu"
__email__ = "ricardo_rodab@ciencias.unam.mx"

import random

def set_random(semilla):
    random.seed(a=semilla, version=2)
    
def get_random():
    return random.random()

def get_randrange(number):
    return random.randrange(number)  

def get_randbits(number):
    return random.getrandbits(number)