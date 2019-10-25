#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "José Ricardo Rodríguez Abreu"
__email__ = "ricardo_rodab@ciencias.unam.mx"

from abejas_tetris.tetris.tablero import *
from abejas_tetris.tetris.indexer import *


from abejas_tetris.my_random import get_random, get_randrange, get_randbits

class Tetris:
    """ Representa un juego de tetris con todos sus componentes."""
    def __init__(self, x, y, tablero=None):
        """
        Parameters
        ----------
        x : int
                Es el ancho del tablero.
        y : int
               Es el alto del tablero.
        tablero : Tablero 
                Es un tablero por si el objeto es clonado.
        """
        if tablero == None: 
            self._tablero = Tablero(x,y)
        else:
            self._tablero = tablero
        self._x = x
        self._y = y
        self._historial = []
        self._piezas_jugadas = 0
        self._game_over = False
        self.id = get_index()

    def desactiva_limpieza_automatica(self):
        """
        Quita la remoción automática de filas llenas.
        """
        self._tablero.set_limpieza_automatica(False)

    def activa_limpieza_automatica(self):
        """
        Activa la remoción automática de filas llenas.
        """
        self._tablero.set_limpieza_automatica()

    def get_altura(self):
        """
        Regresa la altura total del tablero.
        """
        return self._y

    def get_ancho(self):
        """
        Regresa el ancho total del tablero.
        """
        return self._x

    def set_game_over(self, flag):
        self._game_over = flag
    
    def game_over(self):
        """
        Bandera que nos dice si ya perdimos.
        """
        return self._game_over

    def set_piezas_jugadas(self, number):
        """
        Asigna un número de piezas jugadas.
        
        Parameters
        ----------
        number : int
            Es el número total de piezas jugadas.
        """
        self._piezas_jugadas = number

    def altura_maxima(self):
        """
        Regresa la altura máxima actual del tablero.
        """
        return self._tablero.altura_maxima()

    def altura_minima(self):
        """
        Regresa la altura mínima actual del tablero.
        """
        return self._tablero.altura_minima()

    def ultimo_movimiento(self):
        """
        Regresa el último movimiento hecho en el juego.
        """
        return self._historial[len(self._historial) - 1]

    def clona(self):
        """
        Regresa una instancia idéntica del juego de Tetris.
        """
        clon = Tetris(self._x, self._y, self._tablero.clona())
        historial_clone = []
        for i in range(len(self._historial)):
            historial_clone.append(self._historial[i])
        clon.set_historial(historial_clone)
        clon.set_piezas_jugadas(self._piezas_jugadas)
        clon.set_game_over(self._game_over)
        if not self._tablero.get_limpieza():
            clon.desactiva_limpieza_automatica()
        return clon

    def set_pieza(self, tipo=None):
        """
        Asigna una pieza nueva.
        
        Parameters
        ----------
        tipo : Tipo
            Es el tipo de la pieza a jugar.
        """
        if self._tablero.requiere_pieza() and not self._game_over:
            if tipo == None:
                piezas = [Tipo.I, Tipo.LG, Tipo.LS, \
                    Tipo.T, Tipo.RS, Tipo.RG, Tipo.Sq]
                tipo = piezas[get_randrange(len(piezas))]
            self._piezas_jugadas = self._piezas_jugadas + 1
            self._game_over = not self._tablero.set_pieza(tipo)
            return self._game_over
        return False

    def puede_fijar(self):
        """
        Nos dice si el tablero puede fijar la pieza actual.
        """
        return self._tablero.puede_fijar()

    '''
    Para la vista
    '''
    def mueve(self, move):
        """
        Mueve una pieza en el tablero.
        
        Parameters
        ----------
        move : Movimiento
            Es el movimiento del tablero.
        """
        if move == None:
            raise Exception()
        elif move == Movimiento.FIJ:
            return False 
        elif self._tablero.juega_movimiento(move):
            self._historial.append(move)
            return True
        else:
            return False

    '''
    Para la vista
    '''
    def fija(self):
        """
        Fija la pieza actual en el tablero.
        """
        if self._tablero.puede_fijar():
            if self._tablero.fijar():
                self._historial.append(Movimiento.FIJ)
                return True
            else:
                return False
        else:
            return False

    def mueve_o_fija(self, move=None):
        """
        Realiza una acción en el tablero para avanzar el juego.
        
        Parameters
        ----------
        move : Movimiento
            Si es que pasan un movimiento, se realiza el movimiento.
        """
        moves = [Movimiento.CAE, Movimiento.DER, Movimiento.IZQ, Movimiento.GIR]
        moves_posibles = []
        for i in moves:
            if self._tablero.movimiento_valido(i):
                moves_posibles.append(i)
        fijar = self._tablero.puede_fijar()
        if fijar and move == Movimiento.FIJ:
            if self._tablero.fijar():
                self._historial.append(Movimiento.FIJ)
                return True
            return False
        if len(moves_posibles) == 0 and fijar:
            if self._tablero.fijar():
                self._historial.append(Movimiento.FIJ)
                return True
            return False
        elif len(moves_posibles) == 0:
            self._game_over = True
            return False
        elif fijar:
            if move == None:
                move = moves_posibles[get_randrange(len(moves_posibles))]
            # El 0.3 funciona bastante bien
            if get_random() < 0.3:
                if self._tablero.fijar():
                    self._historial.append(Movimiento.FIJ)
                    return True
                return False
            else:
                if self._tablero.juega_movimiento(move):
                    self._historial.append(move)
                    return True
                return False
        else:
            if move == None:
                move = moves_posibles[get_randrange(len(moves_posibles))]
            if self._tablero.juega_movimiento(move):
                self._historial.append(move)
                return True
            return False

    def siguiente_random(self, tipo=None, move=None):
        """
        Juega un movimiento para avanzar en el tiempo de juego.
        
        Parameters
        ----------
        tipo : Tipo
            Es el tipo de pieza siguiente a jugar si se necesita.
        move : Movimiento
            Es el movimiento a jugar.
        """
        if self._tablero.requiere_pieza():
            if tipo == None:
                piezas = [Tipo.I, Tipo.LG, Tipo.LS, \
                    Tipo.T, Tipo.RS, Tipo.RG, Tipo.Sq]
                tipo = piezas[get_randrange(len(piezas))]
            self._piezas_jugadas = self._piezas_jugadas + 1
            return self._tablero.set_pieza(tipo)
        moves = [Movimiento.CAE, Movimiento.DER, Movimiento.IZQ, Movimiento.GIR]
        moves_posibles = []
        for i in moves:
            if self._tablero.movimiento_valido(i):
                moves_posibles.append(i)
        fijar = self._tablero.puede_fijar()
        if len(moves_posibles) == 0 and fijar:
            self._tablero.fijar()
            self._historial.append(Movimiento.FIJ)
            return True
        elif len(moves_posibles) == 0:
            self._game_over = True
            return False
        elif fijar:
            if move == None:
                move = moves_posibles[get_randrange(len(moves_posibles))]
            if get_random() < 0.3:
                self._tablero.fijar()
                self._historial.append(Movimiento.FIJ)
                return True
            else:
                self._historial.append(move)
                self._tablero.juega_movimiento(move)
                return True
        else:
            if move == None:
                move = moves_posibles[get_randrange(len(moves_posibles))]
            self._historial.append(move)
            self._tablero.juega_movimiento(move)
            return True

    def limpia(self):
        """
        Limpia el tablero de ser necesario, fila por fila.
        """
        self._tablero.limpia()

    def puede_limpiar(self):
        """
        Regresa la cantidad de filas que se pueden eliminar.
        """
        return self._tablero.puede_limpiar()

    def get_casilla(self, x, y):
        """
        Regresa lo que se encuentre en la casilla (X,Y).
        
        Parameters
        ----------
        x : int
            Es el ancho a revisar.
        y : int
            Es el alto a revisar.
        """
        return self._tablero.get_casilla(x,y)

    def piezas_jugadas(self):
        """
        Regresa el número total de piezas jugadas.
        """
        return self._piezas_jugadas

    def set_historial(self, historial):
        """
        Asigna un historial a nuestra partida.
        
        Parameters
        ----------
        historial : list(Movimiento)
            Es una lista de movimientos previos jugados.
        """
        self._historial = historial

    def get_historial(self):
        """
        Regresa una lista de movimientos previos jugados.
        """
        return self._historial

    def elimina_historial(self, delta=1):
        """
        Elimina un número delta de movimientos del historial.
        
        Parameters
        ----------
        delta : float
            Es la variable que dice que tanto nos 
            alejaremos de la fuente original.
        """
        primer_fija_visto = False
        while get_random() > delta and len(self._historial) > 0:
            mov = self._historial.pop()
            if mov == Movimiento.FIJ and primer_fija_visto:
                self._historial.append(mov)
                return None
            elif mov == Movimiento.FIJ:
                primer_fija_visto = True
                continue
            else:
                valor = self._tablero.juega_movimiento_inverso(mov)
                if not valor:
                    return None

    def num_movimientos(self):
        """
        Nos dice el número de movimientos que se han hecho hasta ahora.
        """
        return len(self._historial)

    def requiere_pieza(self):
        """
        Regresa True si el juego necesita una pieza para continuar.
        """
        return self._tablero.requiere_pieza()

    def imprime_tablero(self):
        """
        Imprime en la consola una representación del tablero.
        """
        self._tablero.print()

    def movimiento_valido(self, move):
        """
        Regresa True si el movimiento recibido es válido para el juego.
        
        Parameters
        ----------
        move : Movimiento
            Es el movimiento a revisar.
        """
        return self._tablero.movimiento_valido(move)

    def cuenta_espacios(self, fila):
        """
        Cuenta cuantas casillas en blanco hay en una fila.
        
        Parameters
        ----------
        fila : int
            Es la fila a revisar.
        """
        return self._tablero.cuenta_espacios(fila)

    def cuenta_atrapados(self):
        """
        Cuenta cuantas casillas None están rodeadas.
        """
        return self._tablero.cuenta_atrapados()

    def cuenta_cubiertos(self):
        """
        Cuenta cuantas casillas None tienen arriba de ellas una no None.
        """
        return self._tablero.cuenta_cubiertos()

    def num_tetris(self):
        """
        Nos dice cuántas filas se han desaparecido hasta este punto.
        """
        return self._tablero.num_tetris()

    def __hash__(self):
        """
        Se sobrescribe el método hash para asegurar la reproducción
        del programa con las semillas.
        """
        return self.id

    def __eq__(self, other):
        """
        Se sobrescribe el método eq para comparar tetris por id.
        """
        if not isinstance(other, Tetris):
            return NotImplemented
        return self.id == other.id

    def __ne__(self, other):
        """
        Se sobrescribe el método ne para comparar tetris por id.
        """
        if not isinstance(other, Tetris):
            return NotImplemented
        return not self.__eq__(other)
