#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "José Ricardo Rodríguez Abreu"
__email__ = "ricardo_rodab@ciencias.unam.mx"

from .tipo_abeja import *

class Abeja():
    """ Una representación de una abeja que trabaja en una colmena."""
    def __init__(self, tipo=None, id=0, delta=0):
        """
        Parameters
        ----------
        tipo : Tipo_Abeja
            Es uno de los tres tipos que puede ser.
        id : int
            Es el identificador único de cada abrja.
        delta : float
            Es el número que las abejas observadoras se alejarán.
        """
        self._tipo = tipo
        self._id = id
        self._fuente = None
        self._limite = 0
        self._delta = delta
        self._busca_fuente = None
        self._observadoras = None
        self._nectar = None
        self._explotar = None

    def asigna_funciones(self, fuente, observadoras, nectar, explotar):
        """
        Asigna las funciones que necesitan las abejas para trabajar.

        Parameters
        ----------
        fuente : function
            Es la función que busca una fuente.
        observadoras : function
            Es la función que usarán las observadoras para evaluar vecindades.
        nectar : function
            Es la función principal de evaluación de las fuentes.
        explotar : function
            Es la función que trabajará una fuente hasta que se agote.
        """
        self._busca_fuente = fuente
        self._observadoras = observadoras
        self._nectar = nectar
        self._explotar = explotar

    def get_tipo(self):
        """
        Regresa el tipo de la abeja.
        """
        return self._tipo

    def set_tipo(self, tipo):
        """
        Asigna un tipo a la abeja.

        Parameters
        ----------
        tipo : Tipo_Abeja
            Es el nuevo tipo de la abeja.
        """
        self._tipo = tipo
        self._limite = 0

    def get_id(self):
        """
        Regresa el id único de la abeja.
        """
        return self._id

    def set_fuente(self, fuente):
        """
        Asigna una nueva fuente a la abeja.
        
        Parameters
        ----------
        fuente : T
            La nueva fuente que la abeja trabajará.
        """
        self._fuente = fuente
        self._limite = 0

    def get_fuente(self):
        """
        Regresa la fuente actual de la abeja.
        """
        return self._fuente

    def observa_solucion(self):
        """
        Si es abeja observadora, corre su función con su fuente.
        """
        if not self._tipo == Tipo_Abeja.OBS:
            raise Exception("Abeja no debe observar")
        return self._observadoras(self._fuente, self._delta)    

    def explota_fuente(self):
        """
        Si es abeja empleada, corre su función con su fuente.
        """
        if not self._tipo == Tipo_Abeja.EMP:
            raise Exception("Abeja no debe explotar")
        return self._explotar(self._fuente) 
    
    def busca_fuente(self):
        """
        Si es abeja exploradora, corre su función con su fuente.
        """
        if not self._tipo == Tipo_Abeja.EXP:
            raise Exception("Abeja no debe explorar")
        self._busca_fuente(self._fuente)

    def get_nectar(self):
        """
        Evalúa con la función de néctar la fuente de la abeja.
        """
        if not self._tipo == Tipo_Abeja.EMP:
            raise Exception("Abeja no debe evaluar")
        return self._nectar(self._fuente)

    def get_limite(self):
        """
        Regresa el límite de la abeja sobre la fuente actual.
        """
        return self._limite

    def incrementa_iteracion(self):
        """
        Incrementa en uno el límite sobre las fuentes trabajadas.
        """
        self._limite = self._limite + 1