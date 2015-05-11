#!/usr/bin/python

import database as db
import serie as ser

#------------------------------------------
#   Programa Principal
#-------------------------------------------
Puerto= '/dev/ttyAMA0' 
Vel=9600
Timeout=1

db.crearTablas()
db.nuevoSensor(1001,'Temperatura', 1)
db.mostrarSensores()

#ser.initSerial(Puerto,Vel,Timeout)
#ser.comandosAT()
#ser.leerSerial()
#ser.closeSerial()

