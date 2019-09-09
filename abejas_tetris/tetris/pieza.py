#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "José Ricardo Rodríguez Abreu"
__email__ = "ricardo_rodab@ciencias.unam.mx"
import abejas_tetris.tetris 
from .tipo_pieza import *

class Pieza:
    """ Representa una pieza dentro del tablero. """
    def __init__(self, tipo, posicion):
        """
        Parameters
        ----------
        tipo : Tipo
                El tipo de los 7 posibles de pieza.
        posicion : Punto
                Es un punto de tipo (X,Y).
        """
        self._tipo = tipo
        self._orientacion = 0
        self._posicion = posicion
        self._casillas = self.__get_casillas()
        for i in self._casillas:
            i.set_tipo(tipo)
        self._fijo = False

    def clona(self):
        """
        Regresa un clon del objeto
        """
        pos = Punto(self._posicion.get_x(), self._posicion.get_y())
        clone = Pieza(self._tipo, pos)
        clone.set_puntos(self.get_casillas_self())
        clone.set_orientacion(self._orientacion)
        return clone

    def get_orientacion(self):
        """
        Regresa la orientación de la pieza de forma X = (n*90)mod360
        """
        return self._orientacion

    def set_orientacion(self, orientacion):
        """
        Asigna una orientación a la pieza
        
        Parameters
        ----------
        orientacion : int
                Es el número modulo 360.
        """
        self._orientacion = orientacion

    def set_puntos(self, casillas):
        """
        Asigna los puntos al objeto clonando las casillas.
        
        Parameters
        ----------
        casillas : list(Casilla)
                Es una lista de casillas.
        """
        self._casillas[0] = casillas[0].clona()
        self._casillas[1] = casillas[1].clona()
        self._casillas[2] = casillas[2].clona()
        self._casillas[3] = casillas[3].clona()

    def get_casillas_self(self):
        """
        Regresa las casillas que tiene el objeto.
        """
        return self._casillas

    def get_puntos(self):
        """
        Regresa puntos que representan la posición de la pieza.
        """
        p1 = self._casillas[0].get_punto().clona()
        p2 = self._casillas[1].get_punto().clona()
        p3 = self._casillas[2].get_punto().clona()
        p4 = self._casillas[3].get_punto().clona()
        return [p1, p2, p3, p4]

    def rota(self):
        """
        Realiza la rotación de la pieza incluyendo las casillas. 
        """
        self._orientacion = (self._orientacion + 90) % 360
        puntos = rota(self._tipo, self._casillas)
        i = 0
        while i < 4:
            self._casillas[i].set_punto(puntos[i])
            i = i + 1

    def mueve_derecha(self):
        """
        Mueve las casillas de la pieza hacia la derecha.
        """
        for i in self._casillas:
            punto = i.get_punto()
            punto.set_x(punto.get_x() + 1)

    def mueve_izquierda(self):
        """
        Mueve las casillas de la pieza hacia la izquierda.
        """
        for i in self._casillas:
            punto = i.get_punto()
            punto.set_x(punto.get_x() - 1)

    def baja(self):
        """
        Mueve las casillas de la pieza hacia abajo.
        Parameters
        ----------
        """
        for i in self._casillas:
            punto = i.get_punto()
            punto.set_y(punto.get_y() + 1)

    # Este método sólo se usa por las abejas observadoras
    # para regresar a un estado previo.
    def sube(self):
        """
        Mueve las casillas de la pieza hacia arriba.
        """
        for i in self._casillas:
            punto = i.get_punto()
            punto.set_y(punto.get_y() - 1)

    def fija(self):
        """
        Cambia el estado de todas las casillas.
        """
        return self._fijo

    def casillas(self):
        """
        Regresa las casillas de la pieza.
        """
        return self._casillas

    def get_tipo(self):
        """
        Regresa el tipo de la pieza.
        """
        return self._tipo

    # Funciones auxiliares:

    def __get_casillas(self):
        return get_casillas(self._tipo, self._posicion)
