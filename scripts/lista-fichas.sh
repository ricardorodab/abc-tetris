#!/bin/bash

touch ./etc/fichas.csv
limite=1000
for i in $(seq 1 $limite)
do
    n=$(($RANDOM%7))
    if [ $n -eq "0" ]; then
	echo -n "I" >> ./etc/fichas.csv;
    elif [ $n -eq "1" ]; then
	echo -n "RS" >> ./etc/fichas.csv;
    elif [ $n -eq "2" ]; then
	echo -n "LG" >> ./etc/fichas.csv;
    elif [ $n -eq "3" ]; then
	echo -n "T" >> ./etc/fichas.csv;
    elif [ $n -eq "4" ]; then
	echo -n "RG" >> ./etc/fichas.csv;
    elif [ $n -eq "5" ]; then
	echo -n "LS" >> ./etc/fichas.csv;
    else
	echo -n "Sq" >> ./etc/fichas.csv;
    fi

    if [ $i -ne $limite ]; then
	echo -n "," >> ./etc/fichas.csv;
    fi
done
