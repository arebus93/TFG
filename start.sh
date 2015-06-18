#!/bin/bash

#Borramos el fichero de intercambio
cat /dev/null > ./exchange.txt
#Arrancamos node y script python
echo start.sh : Ejecutando servidor
node server.js &
echo start.sh : Ejecutando main.py 
sudo ./main.py

