#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "José Ricardo Rodríguez Abreu"
__email__ = "ricardo_rodab@ciencias.unam.mx"

from .tipo_abeja import *

class Abeja():
    def __init__(self, tipo=None, id=0, delta=0):
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
        self._busca_fuente = fuente
        self._observadoras = observadoras
        self._nectar = nectar
        self._explotar = explotar

    def get_tipo(self):
        return self._tipo

    def set_tipo(self, tipo):
        self._tipo = tipo
        self._limite = 0

    def get_id(self):
        return self._id

    def set_fuente(self, fuente):
        self._fuente = fuente

    def get_fuente(self):
        return self._fuente

    def observa_solucion(self):
        if not self._tipo == Tipo_Abeja.OBS:
            raise Exception("Abeja no debe observar")
        return self._observadoras(self._fuente, self._delta)    

    def explota_fuente(self):
        if not self._tipo == Tipo_Abeja.EMP:
            raise Exception("Abeja no debe explotar")
        return self._explotar(self._fuente) 
    
    def busca_fuente(self):
        if not self._tipo == Tipo_Abeja.EXP:
            raise Exception("Abeja no debe explorar")
        self._busca_fuente(self._fuente)

    def get_nectar(self):
        if not self._tipo == Tipo_Abeja.EMP:
            raise Exception("Abeja no debe evaluar")
        return self._nectar(self._fuente)

    def get_limite(self):
        return self._limite

    def incrementa_iteracion(self):
        self._limite = self._limite + 1