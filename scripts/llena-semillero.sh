#!/bin/bash

# Este script genera numeros aleatorios y los coloca en un archivo que
# llamaremos semillero para que el programa sea repetible.

touch ./etc/semillas.cfg;
echo -n "" > ./etc/semillas.cfg
i=$RANDOM;
while [ $i != 0 ]; do
    echo -n $RANDOM, >> ./etc/semillas.cfg;
    let i-=1;
done
echo -n $RANDOM >> ./etc/semillas.cfg;
