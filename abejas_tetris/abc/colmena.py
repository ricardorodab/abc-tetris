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
        self._fuente_ini = fuente_inicial.clona()
        # abejas : int -> Abeja 
        self._abejas = {}
        # exploradoras : int -> Abeja
        self._exploradoras = {}
        # observadoras: int -> Abeja
        self._observadoras = {}
        # empleadas: int -> Abeja
        self._empleadas = {}
        # T -> int
        self._fuente_abeja = {}
        self._limite = limite
        # T -> int
        self._fuentes = {}
        self._suma_fuentes = 0
        self._delta_observacion = delta_obs
        self._busca_fuente = None
        self._observadoras_fun = None
        self._nectar_fun = None
        self._termino_iteracion = None
        self._explotar_fuente_fun = None
        self._funcion_comparativa = None

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
    
    def set_funcion_comparativa(self, funcion_comparativa):
        """
        Asigna la función para comparar soluciones entre ellas.

        Parameters
        ----------
        funcion_comparativa : function
            Es la función a asignar.
        """
        self._funcion_comparativa = funcion_comparativa

    def actualiza_fuente_inicial(self, fuente_inicial):
        """
        Actualiza la fuente inicial que es de donde parten las exploradoras.

        Parameters
        ----------
        fuente_inicial : T
            Es la nueva fuente a partir.
        """
        self._fuente_ini = fuente_inicial.clona()
    
    def inizializa_abejas(self):
        """
        Crea una colmena con abejas que esperen ser llamadas.
        """
        mitad = int(self._size / 2)
        id = 0
        for _ in range(mitad):
            abja = Abeja(Tipo_Abeja.EXP,id, self._delta_observacion)
            self._abejas[id] = abja
            self._fuente_abeja[abja.get_fuente()] = id
            self._exploradoras[abja.get_id()] = abja
            self._asigna_funciones(id)
            id = id + 1
        for _ in range(self._size - mitad):
            abja = Abeja(Tipo_Abeja.OBS,id, self._delta_observacion)
            self._abejas[id] = abja
            self._observadoras[id] = abja
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
        for i in self._fuentes:
            self._termino_iteracion(i)
        self._itera_empleadas()
        #for i in self._fuentes:
        #    self._termino_iteracion(i)
        self._itera_observadoras()
        self.actualiza_fuente_inicial(self.get_mejor_solucion())
        self._llamada_post_iteracion()


    def get_solucion_final(self):
        """
        Regresa el ultimo resultado con la mayor calificación.
        """
        if self._fuente_ini == None:
            self._fuente_ini = self.get_mejor_solucion()
        return self._fuente_ini

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

        if self._funcion_comparativa != None and False:
            for i in self._fuentes:
                if self._funcion_comparativa(solucion) < self._funcion_comparativa(i): 
                    solucion = i
        return solucion.clona()

    # Funciones auxiliares:
            
    # Asigna las funciones de la colmena a todas las abejas.
    def _asigna_funciones(self, id):
        abja = self._abejas[id]
        abja.asigna_funciones(self._busca_fuente, self._observadoras_fun, \
             self._nectar_fun, self._explotar_fuente_fun)

    # Esta función transforma a todas las abejas exploradoras a una con fuente.
    def _itera_exploradoras(self):
        eliminar = []
        for id in self._exploradoras:
            abja = self._abejas[id]
            if abja.get_fuente() != None:
                del self._fuentes[abja.get_fuente()]
                del self._fuente_abeja[abja.get_fuente()]
            abja.set_fuente(self._fuente_ini.clona())
            self._fuente_abeja[abja.get_fuente()] = id
            abja.busca_fuente()
            abja.set_tipo(Tipo_Abeja.EMP)
            eliminar.append(id)
            self._empleadas[id] = abja
            self._fuentes[abja.get_fuente()] = \
                self._nectar_fun(abja.get_fuente())
        for id in eliminar:
            del self._exploradoras[id]

    # Avanzamos en el tiempo las fuentes para que califiquemos su desempeño.
    def _itera_empleadas(self):
        eliminar = []
        for id in self._empleadas:
            abja = self._empleadas[id] 
            if abja.get_limite() > self._limite:
                del self._fuente_abeja[abja.get_fuente()]
                del self._fuentes[abja.get_fuente()]
                eliminar.append(id)
                abja.set_fuente(None)
                abja.set_tipo(Tipo_Abeja.EXP)
                self._exploradoras[abja.get_id()] = abja
            else:
                nectar = abja.explota_fuente()
                self._suma_fuentes = self._suma_fuentes + nectar
                self._fuentes[abja.get_fuente()] = nectar
                abja.incrementa_iteracion()
        for id in eliminar:
            del self._empleadas[id]

    # Mandamos a las observadoras a ver el waggle-dance y buscar vecindades.
    def _itera_observadoras(self):
        # waggle es la función que le asigna a las abejas su fuente
        self._waggle_dances()

        # checamos cuales fuentes no fueron asignadas.
        # Asignadas tiene de llave la fuente y de valor el id de la abeja.
        eliminar = list(self._fuentes)

        for id in self._observadoras:
            abja = self._observadoras[id]
            if abja.get_fuente() in eliminar:
                eliminar.remove(abja.get_fuente())

        # eliminamos las fuentes no asignadas.
        for fuente in eliminar:
            id = self._fuente_abeja[fuente]
            abja = self._abejas[id]
            del self._fuente_abeja[fuente]
            del self._fuentes[fuente]
            del self._empleadas[abja.get_id()]
            abja.set_fuente(None)
            abja.set_tipo(Tipo_Abeja.EXP)
            self._exploradoras[abja.get_id()] = abja

        # observamos las fuentes asignadas para ver si 
        # la exploración local mejora el resultado.
        for id in self._observadoras:
            abja = self._observadoras[id]
            fuente_delta = abja.observa_solucion()
            nectar_delta = self._nectar_fun(fuente_delta)
            nectar_original = self._fuentes[abja.get_fuente()]
            if nectar_delta > nectar_original:
                self._actualiza_fuentes(fuente_delta, abja.get_fuente())
            
        # Reiniciamos la fuente de las observadoras para la siguiente itercación
        for id in self._observadoras:
            abja = self._observadoras[id]
            abja.set_fuente(None)

    # Una función que regrese True o False dependiendo un factor.
    # Esa función es la probabilidad de escoger una fuente.
    def _rueda_ruleta(self, nectar, factor):
        if self._suma_fuentes == 0 or factor < 0.00000004:
            return bool(get_randbits(1))
        return (get_random() * factor)  <= (nectar/self._suma_fuentes)

    # Esta función genera parejas de observadoras con fuentes.
    def _waggle_dances(self):
        llaves_fuentes = list(self._fuentes)
        if len(llaves_fuentes) <= 0:
            return
        for id in self._observadoras:
            abja = self._observadoras[id]
            it = 0
            factor = 1
            while abja.get_fuente() == None:
                fuente = llaves_fuentes[it]
                nectar = self._fuentes[fuente]
                if self._rueda_ruleta(nectar, factor):
                    abja.set_fuente(fuente)
                elif (it + 1) == len(llaves_fuentes):
                    it = 0
                    factor = factor / 2
                else:
                    it = it + 1

    # Actualiza las fuentes observadas que sean mejores que las originales.
    def _actualiza_fuentes(self, fuente_delta, fuente_original):
        if self._termino_iteracion != None:
            self._termino_iteracion(fuente_delta)
        id = self._fuente_abeja[fuente_original]
        abja = self._abejas[id]

        del self._fuentes[fuente_original]
        del self._fuente_abeja[fuente_original]

        self._fuentes[fuente_delta] = self._nectar_fun(fuente_delta)
        self._fuente_abeja[fuente_delta] = abja.get_id()
        
        abja.set_fuente(fuente_delta)

        # Pero si la asignamos a todas después de limpiarla entonces
        # ya no se puede observar, o si? 
        for i in self._observadoras:
            abja_obs = self._observadoras[i]
            if not (abja_obs.get_fuente() in self._fuentes):
                abja_obs.set_fuente(fuente_delta)

    # Actualiza las fuentes si se requiere de alguna operación posterior.
    def _llamada_post_iteracion(self):
        if self._termino_iteracion != None:
            if self._fuente_ini != None:
                self._termino_iteracion(self._fuente_ini)
            for i in self._fuentes:
                self._termino_iteracion(i)
