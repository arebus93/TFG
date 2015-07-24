#!/bin/bash

adddate() {
    while IFS= read -r line; do
        echo "$(date) $line"
    done
}


#Borramos el fichero de intercambio
cat /dev/null > ./exchange.txt
#Arrancamos node y script python
echo start.sh : Ejecutando servidor
/usr/local/bin/node /media/Kingston/TFG/server.js | adddate >> /var/log/domoB105/domoB105_web.log &
#nohup node server.js &
echo start.sh : Ejecutando main.py 
#sudo ./main.py
sudo stdbuf -oL /media/Kingston/TFG/main.py | adddate >> /var/log/domoB105/domoB105_net.log &

