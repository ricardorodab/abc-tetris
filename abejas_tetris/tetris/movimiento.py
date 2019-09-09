#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "José Ricardo Rodríguez Abreu"
__email__ = "ricardo_rodab@ciencias.unam.mx"
from enum import Enum

class Movimiento(Enum):
    """Este enum representa los posibles movimientos de usuario
    en un juego de Tetris. """
    DER = 1
    IZQ = 2
    CAE = 3
    GIR = 4
    FIJ = 5
    