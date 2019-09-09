#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "José Ricardo Rodríguez Abreu"
__email__ = "ricardo_rodab@ciencias.unam.mx"

from abejas_tetris.tetris.tablero import *

from abejas_tetris.my_random import get_random, get_randrange, get_randbits

class Tetris:
    def __init__(self, x, y, tablero=None):
        if tablero == None: 
            self._tablero = Tablero(x,y)
        else:
            self._tablero = tablero
        self._x = x
        self._y = y
        self._historial = []
        self._piezas_jugadas = 0
        self._game_over = False

    def desactiva_limpieza_automatica(self):
        self._tablero.set_limpieza_automatica(False)

    def activa_limpieza_automatica(self):
        self._tablero.set_limpieza_automatica()

    def get_altura(self):
        return self._y

    def get_ancho(self):
        return self._x

    def game_over(self):
        return self._game_over

    def set_piezas_jugadas(self, number):
        self._piezas_jugadas = number

    def altura_maxima(self):
        return self._tablero.altura_maxima()

    def altura_minima(self):
        return self._tablero.altura_minima()

    def ultimo_movimiento(self):
        item = self._historial.pop()
        self._historial.append(item)
        return item

    def clona(self):
        clon = Tetris(self._x, self._y, self._tablero.clona())
        historial_clone = []
        for i in self._historial:
            historial_clone.append(i)
        clon.set_historial(historial_clone)
        clon.set_piezas_jugadas(self._piezas_jugadas)
        return clon

    def set_pieza(self, tipo=None):
        if self._tablero.requiere_pieza() and not self._game_over:
            if tipo == None:
                piezas = [Tipo.I, Tipo.LG, Tipo.LS, Tipo.T, Tipo.RS, Tipo.RG, Tipo.Sq]
                tipo = piezas[get_randrange(len(piezas))]
            self._piezas_jugadas = self._piezas_jugadas + 1
            self._game_over = not self._tablero.set_pieza(tipo)
            return self._game_over
        return False

    def puede_fijar(self):
        return self._tablero.puede_fijar()

    '''
    Para la vista
    '''
    def mueve(self, move):
        if move == None:
            raise Exception()
        self._tablero.juega_movimiento(move)

    '''
    Para la vista
    '''
    def fija(self):
        if self._tablero.puede_fijar():
            self._tablero.fijar()        

    def mueve_o_fija(self, move=None):
        moves = [Movimiento.CAE, Movimiento.DER, Movimiento.IZQ, Movimiento.GIR]
        moves_posibles = []
        for i in moves:
            if self._tablero.movimiento_valido(i):
                moves_posibles.append(i)
        fijar = self._tablero.puede_fijar()
        if fijar and move == Movimiento.FIJ:
            self._tablero.fijar()
            self._historial.append(Movimiento.FIJ)
            return True
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

    def siguiente_random(self, tipo=None, move=None):
        if self._tablero.requiere_pieza():
            if tipo == None:
                piezas = [Tipo.I, Tipo.LG, Tipo.LS, Tipo.T, Tipo.RS, Tipo.RG, Tipo.Sq]
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
        self._tablero.limpia()

    def get_casilla(self, x, y):
        return self._tablero.get_casilla(x,y)

    def piezas_jugadas(self):
        return self._piezas_jugadas

    def set_historial(self, historial):
        self._historial = historial

    def get_historial(self):
        return self._historial

    def elimina_historial(self, delta=1):
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
        return len(self._historial)

    def requiere_pieza(self):
        return self._tablero.requiere_pieza()

    def imprime_tablero(self):
        self._tablero.print()

    def movimiento_valido(self, move):
        return self._tablero.movimiento_valido(move)

    def cuenta_espacios(self, fila):
        return self._tablero.cuenta_espacios(fila)

    def cuenta_atrapados(self):
        return self._tablero.cuenta_atrapados()

    def cuenta_cubiertos(self):
        return self._tablero.cuenta_cubiertos()

    def num_tetris(self):
        return self._tablero.num_tetris()


                
        


