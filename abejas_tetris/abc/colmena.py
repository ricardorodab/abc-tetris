#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "José Ricardo Rodríguez Abreu"
__email__ = "ricardo_rodab@ciencias.unam.mx"

from .abeja import *
from .tipo_abeja import *
from abejas_tetris.my_random import get_random, get_randrange, get_randbits 

class Colmena():
    def __init__(self, size, fuente_inicial, limite, delta_obs):
        self._size = size
        self._fuente_ini = fuente_inicial
        self._abejas = {}
        self._exploradoras = {}
        self._observadoras = {}
        self._empleadas = {}
        self._fuente_abeja = {}
        self._limite = limite
        self._fuentes = {}
        self._suma_fuentes = 0
        self._delta_observacion = delta_obs
        self._busca_fuente = None
        self._observadoras_fun = None
        self._nectar_fun = None
        self._termino_iteracion = None
        self._explotar_fuente_fun = None

    def set_funcion_nectar(self, calcular_nectar_function):
        self._nectar_fun = calcular_nectar_function

    def set_funcion_buscar_fuente(self, busca_fuente_function):
        self._busca_fuente = busca_fuente_function

    def set_funcion_observacion(self, determina_observacion_function):
        self._observadoras_fun = determina_observacion_function

    def set_funcion_explotar_fuente(self, explorar_fuente):
        self._explotar_fuente_fun = explorar_fuente

    def set_funcion_termino_iteracion(self, termino_iteracion):
        self._termino_iteracion = termino_iteracion

    def actualiza_fuente_inicial(self, fuente_inicial):
        self._fuente_ini = fuente_inicial
    
    def inizializa_abejas(self):
        mitad = int(self._size / 2)
        id = 0
        for i in range(mitad):
            self._abejas[id] = Abeja(Tipo_Abeja.EXP, id, self._delta_observacion)
            self._abejas[id].set_fuente(self._fuente_ini.clona())
            self._fuente_abeja[self._abejas[id].get_fuente()] = id
            self._exploradoras[id] = self._abejas[id]
            self._asigna_funciones(id)
            id = id + 1
        for i in range(self._size - mitad):
            self._abejas[id] = Abeja(Tipo_Abeja.OBS, id, self._delta_observacion)
            self._observadoras[id] = self._abejas[id]
            self._asigna_funciones(id)
            id = id + 1

    def get_nectar_actual(self):
        if self._fuente_ini == None:
            return 0
        return self._nectar_fun(self._fuente_ini)
    
    def itera_colmena(self):
        self._suma_fuentes = 0
        self._itera_exploradoras()
        self._itera_empleadas()
        self._itera_observadoras()
        if self._termino_iteracion != None:
            for i in self._fuentes:
                self._termino_iteracion(i)
        if len(self._fuentes) > 0:
            self._fuente_ini = self.get_mejor_solucion().clona()

    def get_mejor_solucion(self):
        solucion = None
        valor_max = 0
        for i in self._fuentes:
            valor = self._nectar_fun(i)
            if valor > valor_max or solucion == None:
                solucion = i
                valor_max = valor
        return solucion

    def _actualiza_fuentes(self, actualiza):
        for i in actualiza:
            id = self._fuente_abeja[i]
            abja = self._abejas[id]
            del self._fuentes[abja.get_fuente()]
            del self._fuente_abeja[abja.get_fuente()]
            abja.set_fuente(actualiza[i])
            self._fuentes[abja.get_fuente()] = 0
            self._fuente_abeja[abja.get_fuente()] = abja.get_id()

    def _rueda_ruleta(self, nectar, factor):
        if self._suma_fuentes == 0 or factor < 0.0004:
            return bool(get_randbits(1))
        return (get_random() * factor)  <= (nectar/self._suma_fuentes)

    def _waggle_dances(self):
        asignacion = {}
        num_fuentes = len(self._fuentes)
        if num_fuentes <= 0:
            return {}
        llaves_fuentes = list(self._fuentes.keys())
        for i in self._observadoras:
            it = 0
            factor = 1
            while not i in asignacion:
                fuente = llaves_fuentes[it]
                nectar = self._fuentes[fuente]
                if self._rueda_ruleta(nectar, factor):
                    asignacion[i] = fuente
                elif (it + 1) == num_fuentes:
                    it = 0
                    factor = factor / 2
                else:
                    it = it + 1
        return asignacion
            
    def _asigna_funciones(self, id):
        abja = self._abejas[id]
        abja.asigna_funciones(self._busca_fuente, self._observadoras_fun, self._nectar_fun, self._explotar_fuente_fun)

    def _itera_exploradoras(self):
        eliminar = []
        for i in self._exploradoras:
            abja = self._exploradoras[i]
            abja.busca_fuente()
            abja.set_tipo(Tipo_Abeja.EMP)
            eliminar.append(i)
            self._empleadas[i] = abja
            self._fuentes[abja.get_fuente()] = 0
            self._fuente_abeja[abja.get_fuente()] = abja.get_id()
        for i in eliminar:
            del self._exploradoras[i]

    def _itera_empleadas(self):
        eliminar = []
        for i in self._empleadas:
            abja = self._empleadas[i] 
            if abja.get_limite() > self._limite:
                del self._fuentes[abja.get_fuente()]
                del self._fuente_abeja[abja.get_fuente()]
                abja.set_tipo(Tipo_Abeja.EXP)
                abja.set_fuente(self._fuente_ini.clona())
                eliminar.append(i)
                self._exploradoras[i] = abja
            else:
                nectar = abja.explota_fuente()
                self._suma_fuentes = self._suma_fuentes + nectar
                self._fuentes[abja.get_fuente()] = nectar
                abja.incrementa_iteracion()
        for i in eliminar:
            del self._empleadas[i]

    def _itera_observadoras(self):
        parejas_waggle = self._waggle_dances()
        fuentes_visitadas = list(parejas_waggle.values())
        eliminar = []
        for i in self._fuente_abeja:
            if not i in fuentes_visitadas:
                eliminar.append(i)
        for i in eliminar:
            abja = self._abejas[self._fuente_abeja[i]]
            abja.set_tipo(Tipo_Abeja.EXP)
            id = abja.get_id()
            abja.set_fuente(self._fuente_ini.clona())
            self._fuente_abeja[abja.get_fuente()] = id
            self._exploradoras[id] = abja
            del self._fuente_abeja[i]
            del self._fuentes[i]
        actualiza = {}
        for i in parejas_waggle:
            abja = self._observadoras[i]
            abja.set_fuente(parejas_waggle[i])
            fuente = abja.observa_solucion()
            nectar = self._nectar_fun(fuente)
            nectar_viejo = self._fuentes[parejas_waggle[i]]
            if nectar > nectar_viejo:
                actualiza[parejas_waggle[i]] = abja.get_fuente()
            abja.set_fuente(None)
        self._actualiza_fuentes(actualiza)

            