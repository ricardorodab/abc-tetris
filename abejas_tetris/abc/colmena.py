#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "José Ricardo Rodríguez Abreu"
__email__ = "ricardo_rodab@ciencias.unam.mx"

from .abeja import *
from .tipo_abeja import *
from abejas_tetris.my_random import get_random, get_randrange, get_randbits 

class Colmena():
    """ El conjunto de información que todas las abejas necesitan. """
    def __init__(self, size, fuente_inicial, limite, delta_obs):
        """
        Parameters
        ----------
        size : int
            Es el tamaño de la colmena.
        fuente_inicial : T
            Es de donde partirán todas las abejas.
        limite : int
            Es el número máximo de veces que una abeja visita una fuente.
        delta_obs : float
            Es el número que las abejas observadoras se alejarán de su fuente.
        """
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
        """
        Asigna la función para evaluar el néctar.

        Parameters
        ----------
        calcular_nectar_function : function
            Es la función a asignar.
        """
        self._nectar_fun = calcular_nectar_function

    def set_funcion_buscar_fuente(self, busca_fuente_function):
        """
        Asigna la función para buscar una fuente.

        Parameters
        ----------
        calcular_nectar_function : function
            Es la función a asignar.
        """
        self._busca_fuente = busca_fuente_function

    def set_funcion_observacion(self, determina_observacion_function):
        """
        Asigna la función para que las observadoras busquen fuentes cercanas.

        Parameters
        ----------
        calcular_nectar_function : function
            Es la función a asignar.
        """
        self._observadoras_fun = determina_observacion_function

    def set_funcion_explotar_fuente(self, explorar_fuente):
        """
        Asigna la función para seguir explorando una fuente.

        Parameters
        ----------
        calcular_nectar_function : function
            Es la función a asignar.
        """
        self._explotar_fuente_fun = explorar_fuente

    def set_funcion_termino_iteracion(self, termino_iteracion):
        """
        Asigna la función para al finalizar una iteración, evaluar.

        Parameters
        ----------
        calcular_nectar_function : function
            Es la función a asignar.
        """
        self._termino_iteracion = termino_iteracion

    def actualiza_fuente_inicial(self, fuente_inicial):
        """
        Actualiza la fuente inicial que es de donde parten las exploradoras.

        Parameters
        ----------
        fuente_inicial : T
            Es la nueva fuente a partir.
        """
        self._fuente_ini = fuente_inicial
    
    def inizializa_abejas(self):
        """
        Crea una colmena con abejas que esperen ser llamadas.
        """
        mitad = int(self._size / 2)
        id = 0
        for i in range(mitad):
            self._abejas[id] = Abeja(Tipo_Abeja.EXP,id, self._delta_observacion)
            self._abejas[id].set_fuente(self._fuente_ini.clona())
            self._fuente_abeja[self._abejas[id].get_fuente()] = id
            self._exploradoras[id] = self._abejas[id]
            self._asigna_funciones(id)
            id = id + 1
        for i in range(self._size - mitad):
            self._abejas[id] = Abeja(Tipo_Abeja.OBS,id, self._delta_observacion)
            self._observadoras[id] = self._abejas[id]
            self._asigna_funciones(id)
            id = id + 1

    def get_nectar_actual(self):
        """
        Regresa el valor de la mejor solución.
        """
        if self._fuente_ini == None:
            return 0
        return self._nectar_fun(self._fuente_ini)
    
    def itera_colmena(self):
        """
        Itera sólo una ocasión a todas las abejas para que trabajen.
        """
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
        """
        Regresa la mejor solución hasta ahora.
        """
        solucion = None
        valor_max = 0
        for i in self._fuentes:
            valor = self._nectar_fun(i)
            if valor > valor_max or solucion == None:
                solucion = i
                valor_max = valor
        return solucion

    # Funciones auxiliares:

    # Actualiza las fuentes observadas que sean mejores que las originales.
    def _actualiza_fuentes(self, actualiza):
        for i in actualiza:
            id = self._fuente_abeja[i]
            abja = self._abejas[id]
            del self._fuentes[abja.get_fuente()]
            del self._fuente_abeja[abja.get_fuente()]
            abja.set_fuente(actualiza[i])
            self._fuentes[abja.get_fuente()] = 0
            self._fuente_abeja[abja.get_fuente()] = abja.get_id()

    # Una función que regrese True o False dependiendo una factor.
    # Esa función es la probabilidad de escoger una fuente.
    def _rueda_ruleta(self, nectar, factor):
        if self._suma_fuentes == 0 or factor < 0.0004:
            return bool(get_randbits(1))
        return (get_random() * factor)  <= (nectar/self._suma_fuentes)

    # Esta función genera parejas de observadoras con fuentes.
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
            
    # Asigna las funciones de la colmena a todas las abejas.
    def _asigna_funciones(self, id):
        abja = self._abejas[id]
        abja.asigna_funciones(self._busca_fuente, self._observadoras_fun, \
             self._nectar_fun, self._explotar_fuente_fun)

    # Esta función transforma a todas las abejas exploradoras a una con fuente.
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

    # Avanzamos en el tiempo las fuentes para que califiquemos su desempeño.
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

    # Mandamos a las observadoras a ver el waggle-dance y buscar vecindades.
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

            