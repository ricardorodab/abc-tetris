#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "José Ricardo Rodríguez Abreu"
__email__ = "ricardo_rodab@ciencias.unam.mx"
from abejas_tetris.tetris.punto import *
from abejas_tetris.tetris.pieza import *
from abejas_tetris.tetris.movimiento import *
from abejas_tetris.tetris.tipo_pieza import *

class Tablero:
    def __init__(self, x, y):
        """
        Parameters
        ----------
        x : int
                Es el ancho del tablero.
        y : int
               Es el alto del tablero.
        """
        self._x = x
        self._y = y
        self._pieza = None
        self._pieza_anterior = None
        self._limpia_automatico = True
        self._tablero = []
        self._num_tetris = 0
        for i in range(self._x):
            fila = []
            for j in range(self._y):
                fila.append(None)
            self._tablero.append(fila)

    def get_casilla(self, x, y):
        """
        Regresa lo que haya en la posición dada.
        
        Parameters
        ----------
        x : int
            Es el ancho del tablero.
        y : int
            Es el alto del tablero.
        """
        return self._tablero[x][y]

    def set_limpieza_automatica(self, limpieza=True):
        """
        Asigna la variable para que el tablero se limpie solo.
        
        Parameters
        ----------
        limpieza=True : bool
            Es la bandera para que se limpie o no solo.
        """
        self._limpia_automatico = limpieza

    def get_limpieza(self):
        """
        Regresa la bandera para saber si eliminar o no 
        los tetrominoes de forma automática. 
        """
        return self._limpia_automatico

    def clona(self):
        """
        Regresa un objeto clon.
        """
        clon = Tablero(self._x, self._y)
        clon.copia_tablero(self._tablero)
        if self._pieza != None:
            clon.asigna_pieza_clonada(self._pieza.clona())
        if self._pieza_anterior != None:
            clon.asigna_pieza_anterior(self._pieza_anterior.clona())
        clon.set_num_tetris(self._num_tetris)
        clon.set_limpieza_automatica(self._limpia_automatico)
        return clon

    def copia_tablero(self, tablero):
        """
        Dado un tablero, copia lo que haya en él sobre el objeto.    
        
        Parameters
        ----------
        tablero : list(list(Casilla))
            Es el tablero a copiar.
        """
        for i in range(self._x):
            for j in range(self._y):
                if tablero[i][j] != None: 
                    self._tablero[i][j] = tablero[i][j].clona()
                else:
                    self._tablero[i][j] = None

    def asigna_pieza_anterior(self, pieza):
        """
        Dado una pieza, asigna la pieza anterior.
        
        Parameters
        ----------
        pieza : Pieza
            Es la pieza anterior jugada.
        """
        self._pieza_anterior = pieza

    def asigna_pieza_clonada(self, pieza):
        """
        Asigna pieza actual.
        
        Parameters
        ----------
        pieza : Pieza
            Asigna una pieza previamente clonada.
        """
        self._pieza = pieza
        self.__actualiza_pieza([])

    def punto_inicial(self):
        """
        Regresa el punto inicial de la pieza.
        """
        return Punto(int(self._x / 2), 2)

    def set_pieza(self, tipo):
        """
        Asigna una nueva pieza.
        
        Parameters
        ----------
        tipo : Tipo
            Es el tipo de la nueva pieza.
        """
        p = Pieza(tipo, self.punto_inicial())
        for i in p.casillas():
            punto = i.get_punto()
            x = punto.get_x()
            y = punto.get_y()
            if self._tablero[x][y] != None:
                return False
        self._pieza = p
        self.__actualiza_pieza([])
        return True

    def requiere_pieza(self):
        """
        Regresa verdadero si el tablero no tiene pieza actual.
        """
        return self._pieza == None

    def altura_maxima(self):
        """
        Regresa la altura de la pieza más alta.
        """
        altura = 0
        x = 0
        while x < self._x:
            y = 0   
            while y < self._y:
                if self._tablero[x][y] != None:
                    altura_local = self._y - y
                    if altura <= altura_local:
                        altura = altura_local
                y = y + 1
            x = x + 1
        return (altura)

    def altura_minima(self):
        """
        Regresa la altura de la pieza más al fondo.
        """
        y = self._y - 1
        while y >= 0:
            x = 0
            while x < self._x:
                if self._tablero[x][y] == None:
                    return self._y - (y + 1)
                x = x +1
            y = y - 1
        return self._y

    def movimiento_valido(self, move):
        """
        Regresa True si el movimiento que recibe es jugable.
        
        Parameters
        ----------
        move : Movimiento
            Es un movimiento a revisar si es válido.
        """
        if self._pieza == None:
            return False
        if move == Movimiento.CAE:
            return self.__check_cae()
        elif move == Movimiento.DER:
            return self.__check_der()
        elif move == Movimiento.IZQ:
            return self.__check_izq()
        elif move == Movimiento.GIR:
            return self.__check_gir()
        else:
            return False

    def juega_movimiento(self, move):
        """
        Mueve el estado del tablero un movimiento más adelante.
        
        Parameters
        ----------
        move : Movimiento
            Es el movimiento jugado.
        """
        if self._pieza == None:
            return False
        if self.movimiento_valido(move):
            puntos_previos = self._pieza.get_puntos()
            if move == Movimiento.CAE:
                self._pieza.baja()
            elif move == Movimiento.DER:
                self._pieza.mueve_derecha()
            elif move == Movimiento.IZQ:
                self._pieza.mueve_izquierda()
            else:
                self._pieza.rota()
            self.__actualiza_pieza(puntos_previos)
            return True
        else:
            return False

    def restaura_pieza(self):
        """ Si la pieza es vacía vuelve a colocar una anterior"""
        if self._pieza == None and self._pieza_anterior != None:
            self._pieza = self._pieza_anterior
            for i in self._pieza.casillas():
                i.set_fija(False)
            self.__actualiza_pieza([])

    def juega_movimiento_inverso(self, move):
        """
        Mueve el estado del tablero un movimiento hacia atrás.
        
        Parameters
        ----------
        move : Movimiento
            Es el movimiento que se tiene que retirar.
        """
        self.restaura_pieza()
        if self._pieza == None:
            return False
        puntos_previos = self._pieza.get_puntos()
        if move == Movimiento.CAE and self.__check_cae(True):
            self._pieza.sube()
        elif move == Movimiento.DER and self.__check_izq():
            self._pieza.mueve_izquierda()
        elif move == Movimiento.IZQ and self.__check_der():
            self._pieza.mueve_derecha()
        elif move == Movimiento.FIJ:
            raise Exception("No se puede deshacer fijar pieza")
        elif move == Movimiento.GIR:
            tipo = self._pieza.get_tipo()
            tres_giro = tipo == Tipo.LG or tipo == Tipo.T or tipo == Tipo.RG
            if tres_giro:
                self._pieza.rota()
                self._pieza.rota()
                if self.__check_gir():
                    self._pieza.rota()
                else:
                    self._pieza.rota()
                    self._pieza.rota()
                    return False
            elif self.__check_gir():
                self._pieza.rota()
            else:
                return False
        else:
            return False
        self.__actualiza_pieza(puntos_previos)
        return True

    def limpia(self):
        """
        Limpia las filas llenas.
        """
        if not self._limpia_automatico:
            self._cuenta_filas_removidas()
            self.__revisa_filas()

    def puede_limpiar(self):
        """ 
        Regresa las filas que pueden ser eliminadas.
        """
        cuenta_filas = 0
        limite_x = self._x
        limite_y = self._y
        columna = limite_y - 1
        while columna >= 0:
            hay_none = False
            fila = 0
            while fila < limite_x:
                if self._tablero[fila][columna] == None:
                    hay_none = True
                fila = fila + 1
            if not hay_none:
                cuenta_filas = cuenta_filas + 1      
            columna = columna - 1
        return cuenta_filas
            
    def puede_fijar(self):
        """
        Regresa True si la pieza actual puede fijarse en esta posición.
        """
        if self._pieza == None:
            return False
        for i in self._pieza.casillas():
            punto = i.get_punto()
            x = punto.get_x()
            y = punto.get_y()
            if self._y == y + 1:
                return True
            if self._tablero[x][y + 1] != None:
                if self._tablero[x][y + 1].get_fija():
                    return True
        return False
    
    def fijar(self):
        """
        Fija la pieza actual en su posición actual.
        """
        if self.puede_fijar():
            if self._pieza == None:
                return False
            self._pieza_anterior = self._pieza
            for i in self._pieza.casillas():
                i.set_fija()
            self._pieza = None
            if self._limpia_automatico:
                self._cuenta_filas_removidas()
                self.__revisa_filas()
            return True
        else:
            return False

    def print(self):
        """
        Imprime en la consola una representación más 
        amigable del tablero.
        """
        blanco ="#"
        for i in range(self._y):
            cad = ''
            spa = '_'
            for j in range(self._x):
                cad = cad + '|'
                spa = spa + '__'
                if self._tablero[j][i] != None:
                    cad = cad + blanco
                else:
                    cad = cad + " "
            print(cad)
            print(spa)
    
    def cuenta_espacios(self, fila):
        """
        Nos dice cuantas casillas con espacios hay en cierta fila.
        
        Parameters
        ----------
        fila : int
            Es la fila a revisar.
        """
        fila_real = self._y - (fila + 1)
        espacios = 0
        x = 0
        while x < self._x:
            if self._tablero[x][fila_real] == None:
                espacios = espacios + 1
            x = x + 1
        return espacios

    def cuenta_atrapados(self):
        """
        Nos dice cuantas casillas rodeadas de fichas hay.
        """
        x = 0
        atrapado = 0
        while x < self._x:
            y = 0
            while y < self._y:
                rodeado = True
                if self._tablero[x][y] == None:
                    if x - 1 >= 0:
                        rodeado = rodeado and self._tablero[x-1][y] != None
                    if x + 1 < self._x:
                        rodeado = rodeado and self._tablero[x+1][y] != None
                    if y - 1 >= 0:
                        rodeado = rodeado and self._tablero[x][y-1] != None
                    if y + 1 < self._y:
                        rodeado = rodeado and self._tablero[x][y+1] != None
                    if rodeado:
                        atrapado = atrapado + 1
                y = y + 1
            x = x +1
        return atrapado

    
    def cuenta_cubiertos(self):
        """
        No dice cuantas casillas vacías tiene alguna no vacia arriba.
        """
        cubiertos = 0
        for i in range(self._x):
            for j in range(self._y):
                if self._tablero[i][j] == None:
                    cubiertos = cubiertos + self._helper_cubiertos(i, j)
        return cubiertos

    def num_tetris(self):
        """
        Nos dice cuántas filas de han ido hasta ahora.
        """
        return self._num_tetris

    def set_num_tetris(self, num):
        """
        Asigna un número de filas retiradas.
        
        Parameters
        ----------
        num : int
            Es el nuevo número de filas retiradas del tablero.
        """
        self._num_tetris = num

    # Funciones auxiliares:

    # Regresa 1 si la casilla esta cubierta por otra.
    def _helper_cubiertos(self, x, y):
        if y < 0:
            return 0
        if self._tablero[x][y] != None:
            return 1
        return self._helper_cubiertos(x, y - 1)

    # Cuenta si hay filas que quitar.
    def _cuenta_filas_removidas(self):
        limite_x = self._x
        limite_y = self._y
        columna = limite_y - 1
        while columna >= 0:
            hay_none = False
            fila = 0
            while fila < limite_x:
                if self._tablero[fila][columna] == None:
                    hay_none = True
                fila = fila + 1
            if not hay_none:
                self._num_tetris = self._num_tetris + 1      
            columna = columna - 1

    # Revisa si puede caer la pieza actual.
    def __check_cae(self, inverso=False):
        for i in self._pieza.casillas():
            punto = i.get_punto()
            x = punto.get_x()
            y = punto.get_y()
            if inverso:
                if y == 0:
                    return False
            else:
                if y + 1 >= self._y:
                    return False
            if inverso:
                if self._tablero[x][y - 1] != None:
                    if self._tablero[x][y - 1].get_fija():
                        return False
            else:
                if self._tablero[x][y + 1] != None:
                    if self._tablero[x][y + 1].get_fija():
                        return False
        return True

    # Revisa si puede moverse a la derecha la pieza actual.
    def __check_der(self):
        for i in self._pieza.casillas():
            punto = i.get_punto()
            x = punto.get_x()
            y = punto.get_y()
            if self._x <= x + 1:
                return False
            if self._tablero[x + 1][y] != None:
                if self._tablero[x + 1][y].get_fija():
                    return False
        return True

    # Revisa si puede moverse a la izquierda la pieza actual.
    def __check_izq(self):
        for i in self._pieza.casillas():
            punto = i.get_punto()
            x = punto.get_x()
            y = punto.get_y()
            if x - 1 < 0:
                return False
            if self._tablero[x - 1][y] != None:
                if self._tablero[x - 1][y].get_fija():
                    return False
        return True

    # Revisa si puede rotar la pieza actual.
    def __check_gir(self):
        puntos = rota(self._pieza.get_tipo(), self._pieza.casillas())
        for i in puntos:
            if i.get_x() >= self._x or i.get_x() < 0:
                return False
            elif i.get_y() >= self._y or i.get_y() < 0:
                return False
            else:
                valor = self._tablero[i.get_x()][i.get_y()]
                if valor != None:
                    if valor.get_fija():
                        return False
        return True

    # Actualiza los puntos de la pieza actual.
    def __actualiza_pieza(self, puntos_viejos):
        for i in puntos_viejos:
            x = i.get_x()
            y = i.get_y()
            self._tablero[x][y] = None
        for i in self._pieza.casillas():
            punto = i.get_punto()
            x = punto.get_x()
            y = punto.get_y()
            self._tablero[x][y] = i

    # Revisa las filas si hay que eliminar.
    def __revisa_filas(self):
        limite_x = self._x
        limite_y = self._y
        fila = limite_y - 1
        while fila >= 0:
            hay_none = False
            columna = 0
            while columna < limite_x:
                if self._tablero[columna][fila] == None:
                    hay_none = True
                columna = columna + 1
            if not hay_none:
                self.__limpia(fila)
                fila = fila + 1      
            fila = fila - 1

    # Elimina todos las casillas de una fila.
    def __limpia(self, fil):
        limite_x = self._x

        if self._pieza_anterior != None:
            eliminar_anterior = False
            for i in self._pieza_anterior.casillas():
                punto = i.get_punto()
                y = punto.get_y()
                eliminar_anterior = eliminar_anterior \
                    or y == fil \
                    or y + 1 == 0 
                punto.set_y(y + 1)
            if eliminar_anterior:
                self._pieza_anterior = None

        for i in range(limite_x):
            self._tablero[i][fil] = None
        while fil > 0:
            for i in range(limite_x):
                self._tablero[i][fil] = self._tablero[i][fil - 1]
            fil = fil - 1
        for i in range(limite_x):
            self._tablero[i][0] = None

