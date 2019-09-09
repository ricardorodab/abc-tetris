# abejas-tetris

<p align="center">
<img src="http://seminarioenvejecimiento.unam.mx/3ciive/wp-content/uploads/2019/03/ciencias.png" height="300" width="300" />
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Escudo-UNAM-escalable.svg/200px-Escudo-UNAM-escalable.svg.png" width="283" height="283" />
</p>

Una implementación basado en el artículo escrito por Erik D. Demaine, Susan Hohenberger y
David LibenNowell sobre la clasificación de tetris como un problema NP-completo.
Se usa la heurística de Dervis Karaboga que habla sobre una colonia de abejas artificiales.

## Instalación

Se debe tener instalado Python 3.5.3 ó superior.
Se recomienda el uso de PIP como sistema manejador de paquetes.
Se recomienda el uso de ambientes virtuales de Python.


```shell
make
python3 -m venv ./.env
source ./.env/bin/activate
pip install -r requisitos.txt
```

## Uso

Si se desea cambiar el uso del programa, se debe modificar el archivo que se encuentra en la ruta ./etc/config.cfg .

### Terminal

```shell
(.env) user@host:~/path/to/repo$ python __main__.py
```
