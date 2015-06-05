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

#- Numero maximo de medidas que se guardan en cache antes
#- de subir a la base de datos
MAX_MEDIDAS=6

#-Tupla de tipos de sensor
T_sensores=('T','P','L','B','C','A','H')

#-Inicializacion UART
ser.initSerial(Puerto,Vel,Timeout)

#-Creacion de la base datos Sensores y Medidas
#-si no lo estan
db.crearTablas()

#- Precarga de sensores
#- A continuacion actualizamos la cache de sensores
#- con cargasensores()

precarga_sensores =[ (1,11,'Temperatura', 1),
                     (1,12,'Presencia', 1),
                     (1,13,'Luminosidad', 1),
                     (1,15,'Consumo', 1),
                     (1,16,'Presion', 1),
                     (1,17,'Humedad', 1),
        	     (2,21,'Temperatura', 2),
                     (2,22,'Presencia', 2),
                     (2,23,'Luminosidad', 2),
                     (2,25,'Consumo', 2),
                     (2,26,'Presion', 2),
                     (2,27,'Humedad', 2),
                     (3,31,'Temperatura', 3),
                     (3,32,'Presencia', 3),
                     (3,33,'Luminosidad', 3),
                     (3,35,'Consumo', 3),
                     (3,36,'Presion', 3),
                     (3,37,'Humedad', 3),
                     (4,41,'Temperatura', 4),
                     (4,42,'Presencia', 4),
                     (4,43,'Luminosidad', 4),
                     (4,45,'Consumo', 4),
                     (4,46,'Presion', 4),
                     (4,47,'Humedad', 4),
		     (5,51,'Temperatura',5)]

db.nuevoSensor(precarga_sensores)
r_sensores=db.cargarSensores()
print "Cache de sensores"
print r_sensores

#print("\nTabla de Sensores")
#db.TablaSensores()

#- Lista que guarda las medidas  para subir a la base de datos.
#- cuando tiene MAX_MEDIDAS
r_medidas=[]

#-------------------------------------------
# Funciones utilizadas
#------------------------------------------

def guardarMedida(cadena):
 try:
       # print cadena
	parsed_json = json.loads(cadena)
	Id=int(parsed_json['I'])

  #-Buscamos en la cache r_sensores si existe
  #-y los sensores que tiene declarados
  	if r_sensores.has_key(Id):
   		rows=r_sensores[Id] 
   		for i in rows:
			x=(i%10)-1
			tS=T_sensores[x] #Tipo
			m=int(parsed_json[tS]) #Medida
    			t=ser.time.strftime('%H:%M:%S') #Time
    			d=ser.time.strftime('%Y/%m/%d') #Date
  			r_medidas.append([i,m,d,t])    			
  	else:
		print "Sensor no esta en la base de datos"
 
 except ValueError, e:
	print "Error al parsear el JSON"	

#------------------------------------------
#   Programa Principal
#-------------------------------------------
while True:
 #ser.comandosAT() #Mandar comandos AT
 try:

  cadena=ser.leerSerial()

  if (len(cadena)):
       guardarMedida(cadena)

       if (len(r_medidas)>=MAX_MEDIDAS):

             db.nuevaMedida(r_medidas)
             r_medidas=[]
             #print "\nMedidas"
             #db.TablaMedidas()


 except KeyboardInterrupt:
  #- Cerramos el puerto serie y acabamos el programa
  ser.closeSerial(Puerto)
 	



