#!/usr/bin/python

import database as db
import serie as ser
import json


#-----------------------------------------
#  Inicializacion
#----------------------------------------

Puerto= '/dev/ttyAMA0'
Vel=9600
Timeout=1

Tsensores={'Temperatura':'T','Presencia':'P','Luminosidad':'L',
           'Bateria':'B','Presion':'A','Humedad':'H'}

#-Inicializacion UART
ser.initSerial(Puerto,Vel,Timeout)

#-Creacion de la base datos Sensores y Medidas
#-si no lo estan
db.crearTablas()

#-Precarga de sensores
db.cargarSensores()
print("Sensores")
db.TablaSensores()

#-------------------------------------------
# Funciones utilizadas
#------------------------------------------

def guardarMedida(cadena):
 try:
  parsed_json = json.loads(cadena)
  Id=int(parsed_json['I'])
  rows=db.infoSensor(Id)

  if len(rows):
   r_medidas=[] #- Lista que guarda las medidas
		#- para subir a la base de datos.
   for row in rows:
        tS=Tsensores[row[1]]
        m=int(parsed_json[tS])
       	t=ser.time.strftime('%H:%M:%S') #Time
        d=ser.time.strftime('%d/%m/%Y') #Date
        r_medidas.append((row[0],m,d,t))
   
   db.nuevaMedida(r_medidas) 
 
  else:
	print "Sensor no esta en la base de datos"
 
 except:
	"Error al parsear el JSON"	

#------------------------------------------
#   Programa Principal
#-------------------------------------------
while True:
 #ser.comandosAT() #Mandar comandos AT

 cadena=ser.leerSerial()

 if (len(cadena)):
  guardarMedida(cadena)  
  print "\nMedidas"
  db.TablaMedidas()

ser.closeSerial()

