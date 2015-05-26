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

MAX_MEDIDAS=4

#-Diccionario de tipos de sensor
T_sensores={11:'T', 12:'P',13:'L', 14:'B',15:'C',16:'A',17:'H'}

#-Inicializacion UART
ser.initSerial(Puerto,Vel,Timeout)

#-Creacion de la base datos Sensores y Medidas
#-si no lo estan
db.crearTablas()

#- Precarga de sensores
#- A continuacion actualizamos la cache de sensores
#- con cargasensores()

precarga_sensores =[ (1,11,'Temperatura', 1),
        	     (1,17,'Humedad', 1),
        	     (1,16,'Presion', 1),
              	     (1,13,'Luminosidad',1)]

db.nuevoSensor(precarga_sensores)
r_sensores=db.cargarSensores()
print "Cache de sensores"
print r_sensores

print("\nTabla de Sensores")
db.TablaSensores()

#- Lista que guarda las medidas  para subir a la base de datos.
#- cuando tiene MAX_MEDIDAS
r_medidas=[]

#-------------------------------------------
# Funciones utilizadas
#------------------------------------------

def guardarMedida(cadena):
 try:
        #print cadena
	parsed_json = json.loads(cadena)
	Id=int(parsed_json['I'])

  #-Buscamos en la cache r_sensores si existe
  #-y los sensores que tiene declarados
  	if r_sensores.has_key(Id):
   		rows=r_sensores[Id] 
   		for i in rows:
			tS=T_sensores[i]
   			m=int(parsed_json[tS]) #Medida
    			t=ser.time.strftime('%H:%M:%S') #Time
    			d=ser.time.strftime('%d/%m/%Y') #Date
  			r_medidas.append([i,m,t,d])    			
  	else:
		print "Sensor no esta en la base de datos"
 
 except:
	print "Error al parsear el JSON"	

#------------------------------------------
#   Programa Principal
#-------------------------------------------
while True:
 #ser.comandosAT() #Mandar comandos AT

 cadena=ser.leerSerial()

 if (len(cadena)):
	guardarMedida(cadena)
	#print r_medidas  
	#print len(r_medidas)
	if (len(r_medidas)>=MAX_MEDIDAS):
		db.nuevaMedida(r_medidas)
   		r_medidas=[]
  		#print "\nMedidas"
  		#db.TablaMedidas()

ser.closeSerial()

