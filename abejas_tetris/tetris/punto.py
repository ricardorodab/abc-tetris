#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "José Ricardo Rodríguez Abreu"
__email__ = "ricardo_rodab@ciencias.unam.mx"
class Punto:
    """Un simple punto para coordenadas."""
    def __init__(self, x, y):
        """
        Parameters
        ----------
        x : int
            La coordenada x del punto.
        y : int
            La coordenada y del punto.
         """
        self._x = x
        self._y = y

    def get_x(self):
        """
        Regresa la variable X del punto.
        """
        return self._x

    def get_y(self):
        """
        Regresa la variable Y del punto.
        """
        return self._y

    def set_x(self, valor):
        """
        Asigna la variable X del punto.
        
        Parameters
        ----------
        valor : int
            Es el nuevo valor de la coordenada.
        """
        self._x = valor

    def set_y(self, valor):
        """
        Asigna la variable Y del punto.
        
        Parameters
        ----------
        valor : int
            Es el nuevo valor de la coordenada.
        """
        self._y = valor

    def same(self, punto):
        """
        Revisa que dos puntos sean el mismo.
        
        Parameters
        ----------
        punto : Punto
            Es el otro punto.
        """
        return self._x == punto.get_x() and self._y == punto.get_y()

    def clona(self):
        """
        Crea un mismo punto.
        """
        return Punto(self._x, self._y)
