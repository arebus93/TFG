#!/usr/bin/python

import database as db
import serie as ser

#-----------------------------------------
#  Inicializacion
#----------------------------------------

Puerto= '/dev/ttyAMA0'
Vel=9600
Timeout=1

#-Inicializacion UART
ser.initSerial(Puerto,Vel,Timeout)

#-Creacion de la base datos Sensores y Medidas
#-si no lo estan

db.crearTablas()
db.cargarSensores()
print("Sensores")
db.mostrarSensores()



#------------------------------------------
#   Programa Principal
#-------------------------------------------
while True:
	ser.comandosAT()
       
	#ser.leerSerial()

#db.nuevaMedida(1001,44,'01/01/2000','00:00:00')
#db.nuevaMedida(1002,28,'01/01/2000','00:00:03')
#db.borrarMedida(1001,'01/01/2000','00:00:03')
#print("Medidas del sensor 1001")
#db.medidasSensor(1001)
ser.closeSerial()

