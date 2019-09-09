from abejas_tetris.abejas_tetris import *
from abejas_tetris.parse_config import *
from abejas_tetris.my_random import *
import re,sys
import logging

def set_logging(level):
    """ Crea un loggin para leer en terminal. """
    logging.basicConfig()
    level = None
    if level == 'INFO':
        level = logging.INFO
    elif level == 'DEBUG':
        level = logging.DEBUG
    elif level == 'WARN':
        level = logging.WARN
    else:
        level = logging.INFO
    logging.getLogger().setLevel(level)
        

def get_fichas():
    """ Regresa las fichas en forma de lista de cadenas. """
    fichas_lista = []
    file = open("./etc/fichas.csv", "r")
    lineas = file.readlines()
    for linea in lineas:
        fichas_lista = linea.split(',')
    return fichas_lista

def get_config_hash():
    """ Regresa los parámetros principales. """
    return get_config("./etc/config.cfg")

def get_juego(data):
    """ Regresa una instancia de la inferfaz de heurística-juego. """
    online = data['online']
    size_colmena = data['size_colmena']
    limite_it = data['limite_it']
    delta = data['delta']
    alto = data['alto']
    ancho = data['ancho']
    abc = Abejas_Tetris(online=online, size_colmena=size_colmena, limite_it=limite_it, delta=delta, alto=alto, ancho=ancho)
    abc.set_lista_piezas(get_fichas())
    return abc

def imprime_datos(solucion):
    """ Imprime en pantalla algunos datos del tablero. """
    nectar_local = funcion_nectar_online(solucion)
    piezas_local = solucion.piezas_jugadas()
    logging.info('Nectar final: ' + str(nectar_local))
    logging.info('Piezas jugadas: ' + str(piezas_local))
    logging.info('Filas eliminadas: ' + str(solucion.num_tetris()))
    solucion.imprime_tablero()

def busca_semilla(data):
    """ Busca las mejores semillas a jugar. """
    itera_range = data['semilla_itera']
    semillero = data['semilla_ubicacion']
    logging.warning('Iniciando busqueda de mejor semilla')
    logging.warning('Este proceso puede tardar dependiendo de la variable SEMILLA_ITERA')
    semilla = 0
    nectar = 0
    piezas = 0
    it = 0
    file = open(semillero, "r")
    lineas = file.readlines()
    for linea in lineas:
        fichas_lista = linea.split(',')
        for r in range(itera_range):
            sem = fichas_lista[r]
            set_random(int(sem))
            abc = get_juego(data)
            if data['online']:
                iteraciones = data['iteraciones']
                solucion = abc.juega_online(iteraciones=iteraciones)
                nectar_local = funcion_nectar_online(solucion)
                piezas_local = solucion.piezas_jugadas()
                it = it + 1
                if (it % 5) == 0:
                    logging.info('Semillas probadas: ' + str(it))
                cond1 = nectar_local > nectar
                cond2 = nectar_local == nectar and piezas < piezas_local
                if cond1 or cond2:
                    logging.info('Semilla mejorada: ' + str(sem))
                    logging.info('Nectar final: ' + str(nectar_local))
                    logging.info('Piezas jugadas: ' + str(piezas_local))
                    logging.info('Filas eliminadas: ' + str(solucion.num_tetris()))
                    nectar = nectar_local
                    semilla = int(sem)
                    piezas = piezas_local
    logging.info('La mejor semilla encontrada es: ' + str(semilla))
    return semilla

def set_random_local(data):
    """ Asigna una semilla al generador de números aleatorios. """
    semilla = data['semilla']
    if not data['random_var']:
        if semilla == -1:
            semilla = busca_semilla(data)
        set_random(semilla)

# Punto de entrada del proyecto:
if __name__ == "__main__":
    data = get_config_hash()

    set_logging(data['logging_level'])
    set_random_local(data)
    abc = get_juego(data)
    
    if data['interactivo']:
        abc.interactivo()
    elif data['online']:
        solucion = abc.juega_online(iteraciones=data['iteraciones'])
        imprime_datos(solucion)
        if data['gui']:  
            abc.pinta_solucion(solucion)