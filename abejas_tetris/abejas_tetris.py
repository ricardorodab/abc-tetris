#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "José Ricardo Rodríguez Abreu"
__email__ = "ricardo_rodab@ciencias.unam.mx"

import abejas_tetris as abeja_tetris
import abejas_tetris.tetris as tetris
from abejas_tetris.tetris.tipo_pieza import *
from abejas_tetris.tetris.movimiento import *
from abejas_tetris.tetris.casilla import *
from abejas_tetris.tetris.punto import *
from abejas_tetris.constantes import *
from abejas_tetris.abc.colmena import *
from abejas_tetris.funciones_online import *
import time
from abejas_tetris.my_random import get_random, get_randrange, get_randbits
import pygame
from pygame.locals import *
import math

lista_piezas = []

def get_piezas():
    global lista_piezas
    return lista_piezas

class Abejas_Tetris():
    """ La interfaz de comunicación entre la heurística y el juego. """
    def __init__(self, online=True, size_colmena=150, \
        limite_it=50, delta=0.1, alto=20, ancho=10):
        """
        Parameters
        ----------
        online : bool
            Es una bandera de modo del juego.
        size_colmena : int
            Es el tamaño que tendrá la colmena de abejas.
        limite_it : int
            Es el límite de iteraciones que una abeja hace sobre una fuente.
        delta : float
            Es qué tan lejos llegará la abeja observadora.
        alto : int
            Es el alto del tablero.
        ancho : int
            Es el ancho del tablero.
        """
        self._x = ancho
        self._y = alto
        t = tetris.Tetris(self._x, self._y)
        self._tetris = t
        self.pierde = False
        self.online = online
        self.colmena = Colmena(size_colmena, self._tetris, limite_it, delta)
        self.lista_piezas = []

    def set_lista_piezas(self, piezas):
        global lista_piezas
        lista_piezas = []
        self.lista_piezas = []
        """
        Asigna una lista de piezas a la lista global de piezas.
        Parameters
        ----------
        piezas : list(str)
            Es la lista de piezas en su representación de string.
        """
        for i in piezas:
            if i == 'I':
                self.lista_piezas.append(Tipo.I)
                lista_piezas.append(Tipo.I)
            elif i == 'LG':
                self.lista_piezas.append(Tipo.LG)
                lista_piezas.append(Tipo.LG)
            elif i == 'LS':
                self.lista_piezas.append(Tipo.LS)
                lista_piezas.append(Tipo.LS)
            elif i == 'RG':
                self.lista_piezas.append(Tipo.RG)
                lista_piezas.append(Tipo.RG)
            elif i == 'RS':
                self.lista_piezas.append(Tipo.RS)
                lista_piezas.append(Tipo.RS)
            elif i == 'T':
                self.lista_piezas.append(Tipo.T)
                lista_piezas.append(Tipo.T)
            else:
                self.lista_piezas.append(Tipo.Sq)
                lista_piezas.append(Tipo.Sq)

    def init_colmena(self):
        """
        Inicializa los valores de las funciones de la colmena.
        """
        if self.online:
            self.colmena.set_funcion_nectar(funcion_nectar_online)
            self.colmena.set_funcion_buscar_fuente(funcion_buscar_fuente_online)
            self.colmena.set_funcion_observacion(funcion_observacion_online)
            self.colmena.set_funcion_termino_iteracion(funcion_limpiadora)  
            self.colmena.set_funcion_explotar_fuente(explota_tablero)
            self.colmena.set_funcion_comparativa(num_tetris)
            self.colmena.inizializa_abejas()
    
    def juega_online(self, iteraciones=None, limpieza=False):
        """
        Juega Tetris con abejas de manera online.
        
        Parameters
        ----------
        iteraciones=None : int
            Es el número de iteraciones que correrá la partida.
        """
        if not limpieza:
            self._tetris.desactiva_limpieza_automatica()
            self.colmena.actualiza_fuente_inicial(self._tetris)
        else:
            self._tetris.activa_limpieza_automatica()
        self.init_colmena()
        if iteraciones == None:
            cond = self._tetris.game_over()
            while not cond:
                self.colmena.itera_colmena()
                cond = self.colmena.get_solucion_final().game_over()
        else:
            for i in range(iteraciones):
                self.colmena.itera_colmena()
                if self._tetris.game_over():
                    return self.colmena.get_solucion_final()
        return self.colmena.get_solucion_final()

    def interactivo(self):
        """
        Hace una pequeña interfaz para ver el funcionamiento paso a paso del 
        juego.
        """
        tetris_tmp = self._tetris
        self._tetris = tetris.Tetris(self._x, self._y)
        self.set_gui()
        pieza = 0
        while not self._tetris.game_over():
            if self._tetris.requiere_pieza():
                tipo = self.lista_piezas[pieza]
                pieza = pieza + 1
                self._tetris.set_pieza(tipo=tipo)
            moves = [Movimiento.CAE, Movimiento.DER, \
                Movimiento.IZQ, Movimiento.GIR]
            moves_posibles = []
            for i in moves:
                if self._tetris.movimiento_valido(i):
                    moves_posibles.append(i)
            if self._tetris.puede_fijar():
                moves_posibles.append(Movimiento.FIJ)
            print("¿Cuál es el siguiente movimiento?")
            print("Movimientos válidos:")
            j = 0
            for i in moves_posibles:
                print(str(j) + ":" + str(i))
                j = j + 1
            print("Ingrese número de movimiento:")
            mov = int(input())
            move = moves_posibles[mov]
            if move != Movimiento.FIJ:
                self._tetris.mueve(move=move)
            else:
                self._tetris.fija()
                print('###### NECTAR ######')
                print(funcion_nectar_online(self._tetris))
                print('###### FILAS ELIMINADAS #####')
                print(self._tetris.num_tetris())
            self.dibuja()
            time.sleep(0.05)
        self.quit_gui()
        self._tetris = tetris_tmp

    def pinta_historia(self, historia=[]):
        """
        Pinta una lista de movimientos.

        Parameters
        ----------
        historial : list(Movimiento)
            Es el historial de movimientos hechos que pintar.
        """
        print("Pintando el historial:")
        tetris_tmp = self._tetris
        self._tetris = tetris.Tetris(self._x, self._y)
        self.set_gui()
        pieza = 1
        tipo = self.lista_piezas[0]
        self._tetris.set_pieza(tipo=tipo)
        moves = historia
        while len(moves) > 0:
            move = moves.pop(0)
            if move == Movimiento.FIJ:
                self._tetris.fija()
                tipo = self.lista_piezas[pieza]
                self._tetris.set_pieza(tipo=tipo)
                pieza = pieza + 1
            else:
                self._tetris.mueve(move=move)
            self.dibuja()
            time.sleep(0.05)
        print('###### NECTAR ######')
        print(funcion_nectar_online(self._tetris))
        print('###### FILAS ELIMINADAS #####')
        print(self._tetris.num_tetris())
        time.sleep(5)
        self.quit_gui()
        self._tetris = tetris_tmp

    def pinta_solucion(self, solucion):
        """
        Dada una solución de un juego de Tetris, crea una GUI y la muestra.

        Parameters
        ----------
        solucion : Tetris
            Es el juego de Tetris a dibujar.
        """
        tetris_tmp = self._tetris
        historial = solucion.get_historial()
        moves = []
        for i in historial:
            moves.append(i)
        self._tetris = tetris.Tetris(self._x, self._y)
        self.set_gui()
        tipo = self.lista_piezas[self._tetris.piezas_jugadas()]
        self._tetris.set_pieza(tipo=tipo)
        while len(moves) > 0:
            move = moves.pop(0)
            if move == Movimiento.FIJ:
                self._tetris.fija()
                tipo = self.lista_piezas[self._tetris.piezas_jugadas()]
                self._tetris.set_pieza(tipo=tipo)
            else:
                self._tetris.mueve(move=move)
            self.dibuja()
            time.sleep(0.05)
        print('###### NECTAR ######')
        print(funcion_nectar_online(self._tetris))
        print('###### FILAS ELIMINADAS #####')
        print(self._tetris.num_tetris())
        time.sleep(5)
        self.quit_gui()
        self._tetris = tetris_tmp
        

    def random(self):
        """
        Juega de forma completamente aleatoria.
        """
        while not self.pierde:
            tipo = self.__random_tipo()
            move = self.__random_move()
            self.pierde = not self._tetris.siguiente_random(tipo=tipo, \
                move=move)
            self.dibuja()
            time.sleep(0.05)

    def quit_gui(self):
        """
        Sale de la interfaz gráfica.
        """
        pygame.font.quit()
        pygame.display.quit()
        pygame.mixer.quit()

    def set_gui(self):
        """
        Inizializa los valores que pygame debe tener al principio.
        """
        self._gui = True
        # Tablero:
        self.resx = self._x*ANCHO_BLOQUE+2*TABLERO_ALTURA+TABLERO_MARGEN
        self.resy = self._y*ALTO_BLOQUE+2*TABLERO_ALTURA+TABLERO_MARGEN
        # Lineas:                                                           
        self.frontera_arriba = pygame.Rect(0,0,self.resx,TABLERO_ALTURA)
        self.frontera_abajo = \
            pygame.Rect(0,self.resy-TABLERO_ALTURA,self.resx,TABLERO_ALTURA)
        self.frontera_izq = pygame.Rect(0,0,TABLERO_ALTURA,self.resy)
        self.frontera_der = \
            pygame.Rect(self.resx-TABLERO_ALTURA,0,TABLERO_ALTURA,self.resy)
        self.inicio_x = math.ceil(self.resx/2.0)
        self.inicio_y = TABLERO_MARGEN_SUPERIOR+TABLERO_ALTURA + TABLERO_MARGEN
        # False means no rotate and True allows the rotation.     
        self.colores = {
            Tipo.I : ROJO,     # I                                                                                                   
            Tipo.RS : VERDE,  # S                                                                                                    
            Tipo.LG : AZUL,    # J                                                                                                     
            Tipo.Sq : NARANJA, # O                                                                                                    
            Tipo.LS : DORADO,   # Z block                                                                                                  
            Tipo.T : MORADO,  # T block                                                                                                    
            Tipo.RG : AZUL_CIAN    # J block                                                                                               
        }
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        pygame.mixer.music.load("./etc/tetris-theme.mp3")
        pygame.mixer.music.play()
        time.sleep(1)
        self.pantalla = pygame.display.set_mode((self.resx,self.resy))
        pygame.display.set_caption("Tetris")

    def dibuja(self):
        """
        Dibuja todo lo que haya en el tablero del juego.
        """
        self.pantalla.fill(NEGRO)
        self.__dibuja_tablero()
        self.__dibuja_fichas()   
        pygame.display.flip()

    # Funciones auxiliares

    # Dibuja las fichas.
    def __dibuja_fichas(self):
        for x in range(self._x):
            for y in range(self._y):
                if self._tetris.get_casilla(x,y) != None:
                    tipo = self._tetris.get_casilla(x, y).get_tipo()
                    bloque = self._get_block(x, y)
                    pygame.draw.rect(self.pantalla, \
                        self.colores.get(tipo), bloque)
                    pygame.draw.rect(self.pantalla, \
                        NEGRO, bloque, MARGEN_BLOQUE)
    
    # Dibuja todos los bloques de las fichas.
    def _get_block(self, x, y):
        bx = (x + 0.3)*ALTO_BLOQUE + TABLERO_MARGEN
        by = (y + 0.4)*ANCHO_BLOQUE + 0 
        return pygame.Rect(bx,by,ANCHO_BLOQUE,ALTO_BLOQUE)

    # Dibuja el tablero.  
    def __dibuja_tablero(self):
        pygame.draw.rect(self.pantalla, BLANCO, self.frontera_arriba)
        pygame.draw.rect(self.pantalla, BLANCO, self.frontera_abajo)
        pygame.draw.rect(self.pantalla, BLANCO, self.frontera_izq)
        pygame.draw.rect(self.pantalla, BLANCO, self.frontera_der)

    # Función que regresa los puntos de la casillas.
    def __get_puntos(self, casillas):
        puntos = []
        for i in casillas:
            puntos.append(i.get_punto())
        return puntos

    # Regresa un Tipo de manera aleatoria.
    def __random_tipo(self):
        piezas = [Tipo.I, Tipo.LG, Tipo.LS, Tipo.T, Tipo.RS, Tipo.RG, Tipo.Sq]
        return piezas[get_randrange(len(piezas))]

    # Regresa un Movimiento (menos FIJ) de forma aleatoria.
    def __random_move(self):
        moves = [Movimiento.CAE, Movimiento.DER, Movimiento.IZQ, Movimiento.GIR]
        moves_posibles = []
        for i in moves:
            if self._tetris.movimiento_valido(i):
                moves_posibles.append(i)
        if len(moves_posibles) > 0:
            return moves_posibles[get_randrange(len(moves_posibles))]
        return None
