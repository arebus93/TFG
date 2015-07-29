#!/bin/bash

adddate() {
    while IFS= read -r line; do
        echo "$(date) $line"
    done
}

PIDS_FILE="/tmp/domoB105.pid"

#MATAMOS LOS PROCESOS ANTERIORES
if [[ -f $PIDS_FILE ]] ; then
    sudo kill -9 $(cat $PIDS_FILE)
    rm $PIDS_FILE
    echo "KILLING LAST PROCESS, RE-RUN SCRIPT"
    exit; 
fi

touch $PIDS_FILE


#Borramos el fichero de intercambio
cat /dev/null > ./exchange.txt
#Arrancamos node y script python
echo start.sh : Ejecutando servidor
/usr/local/bin/node /media/Kingston/TFG/server.js | adddate >> /var/log/domoB105/domoB105_web.log &
PID=`echo $!`
echo $PID >> $PIDS_FILE
#nohup node server.js &
echo start.sh : Ejecutando main.py 
#sudo ./main.py
sudo stdbuf -oL /media/Kingston/TFG/main.py | adddate >> /var/log/domoB105/domoB105_net.log &
PID=`echo $!`
echo $PID >> $PIDS_FILE
sleep 3
ps aux | grep -i TFG | awk {'print $2'} >> $PIDS_FILE

