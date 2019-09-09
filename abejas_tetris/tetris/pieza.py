#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "José Ricardo Rodríguez Abreu"
__email__ = "ricardo_rodab@ciencias.unam.mx"
import abejas_tetris.tetris 
from .tipo_pieza import *

class Pieza:
    def __init__(self, tipo, posicion):
        self._tipo = tipo
        self._orientacion = 0
        self._posicion = posicion
        self._casillas = self.__get_casillas()
        for i in self._casillas:
            i.set_tipo(tipo)
        self._fijo = False

    def clona(self):
        pos = Punto(self._posicion.get_x(), self._posicion.get_y())
        clone = Pieza(self._tipo, pos)
        clone.set_puntos(self.get_casillas_self())
        clone.set_orientacion(self._orientacion)
        return clone

    def get_orientacion(self):
        return self._orientacion

    def set_orientacion(self, orientacion):
        self._orientacion = orientacion

    def set_puntos(self, casillas):
        self._casillas[0] = casillas[0].clona()
        self._casillas[1] = casillas[1].clona()
        self._casillas[2] = casillas[2].clona()
        self._casillas[3] = casillas[3].clona()

    def get_casillas_self(self):
        return self._casillas

    def get_puntos(self):
        p1 = self._casillas[0].get_punto().clona()
        p2 = self._casillas[1].get_punto().clona()
        p3 = self._casillas[2].get_punto().clona()
        p4 = self._casillas[3].get_punto().clona()
        return [p1, p2, p3, p4]

    def rota(self):
        self._orientacion = (self._orientacion + 90) % 360
        puntos = rota(self._tipo, self._casillas)
        i = 0
        while i < 4:
            self._casillas[i].set_punto(puntos[i])
            i = i + 1

    def mueve_derecha(self):
        for i in self._casillas:
            punto = i.get_punto()
            punto.set_x(punto.get_x() + 1)

    def mueve_izquierda(self):
        for i in self._casillas:
            punto = i.get_punto()
            punto.set_x(punto.get_x() - 1)

    def baja(self):
        for i in self._casillas:
            punto = i.get_punto()
            punto.set_y(punto.get_y() + 1)

    def sube(self):
        for i in self._casillas:
            punto = i.get_punto()
            punto.set_y(punto.get_y() - 1)

    def fija(self):
        return self._fijo

    def casillas(self):
        return self._casillas

    def get_tipo(self):
        return self._tipo

    def __get_casillas(self):
        return get_casillas(self._tipo, self._posicion)
