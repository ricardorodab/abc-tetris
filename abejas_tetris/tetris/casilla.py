#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "José Ricardo Rodríguez Abreu"
__email__ = "ricardo_rodab@ciencias.unam.mx"
class Casilla:
    """ Una casilla es un espacio atómico en un tablero"""
    def __init__(self, punto, tipo=None):
        """
        Parameters
        ----------
        punto : Punto
           Es el punto de la casilla
        tipo : Tipo
            Es el tipo que la que apareció
        """
        self._punto = punto
        self._fija = False
        self._tipo = tipo

    def get_tipo(self):
        """
        Regresa el tipo de la casilla.
        """
        return self._tipo

    def set_tipo(self, tipo):
        """
        Asigna el tipo de la casilla.

        Parameters
        ----------
        tipo : Tipo
            Es el nuevo tipo de la casilla.
        """
        self._tipo = tipo


    def get_punto(self):
        """
        Regresa el punto de la casilla.
        """
        return self._punto

    def clona(self):
        """
        Regresa una casilla clonada.
        """
        c = Casilla(self._punto.clona())
        c.set_tipo(self._tipo)
        if self.get_fija():
            c.set_fija()
        return c

    def set_punto(self, punto):
        """
        Asigna el punto de la casilla.

        Parameters
        ----------
        punto : Punto
            Es el nuevo punto de la casilla.
        """
        self._punto = punto

    def set_fija(self):
        """
        Coloca como final la posición de la casilla.
        """
        self._fija = True

    def get_fija(self):
        """
        Regresa el valor de la casilla en el tablero.
        """
        return self._fija
