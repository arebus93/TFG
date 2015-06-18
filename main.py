#!/usr/bin/python

import database as db
import serie as ser
import json
import os.path as path
import pyinotify

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
precarga_sensores =[ (1,11,'Temperatura', 1,-1),
                     (1,12,'Presencia', 1,-1),
                     (1,13,'Luminosidad', 1,-1),
                     (1,15,'Consumo', 1,-1),
                     (1,16,'Presion', 1,-1),
                     (1,17,'Humedad', 1,-1),
                     (2,21,'Temperatura', 2,-1),
                     (2,22,'Presencia', 2,-1),
                     (2,23,'Luminosidad', 2,-1),
                     (2,25,'Consumo', 2,-1),
                     (2,26,'Presion', 2,-1),
                     (2,27,'Humedad', 2,-1),
                     (3,31,'Temperatura', 3,-1),
                     (3,32,'Presencia', 3,-1),
                     (3,33,'Luminosidad', 3,-1),
                     (3,35,'Consumo', 3,-1),
                     (3,36,'Presion', 3,-1),
                     (3,37,'Humedad', 3,-1),
                     (4,41,'Temperatura',4,-1),
                     (4,42,'Presencia', 4,-1),
                     (4,43,'Luminosidad',4,-1),
                     (4,45,'Consumo', 4,-1),
                     (4,46,'Presion', 4,-1),
                     (4,47,'Humedad', 4,-1),
          	     (5,51,'Temperatura',5,-1),
		     (6,61,'Temperatura',6,-1),
                     (6,62,'Presencia', 6,-1),
                     (6,64,'Bateria',6,-1),
		     (0,01,'Temperatura',0,-1),
                     (0,02,'Presencia', 0,-1),
                     (0,04,'Bateria',0,-1)]
db.nuevoSensor(precarga_sensores)

#- A continuacion actualizamos la cache de sensores
#- con cargasensores()
r_sensores=db.cargarSensores()

#- Lista que guarda las medidas  para subir a la base de datos.
#- cuando tiene MAX_MEDIDAS
r_medidas=[]

#-Configuracion del notifier del fichero exchange.txt
change_flag=0
FWATCH= path.abspath('exchange.txt')
wm = pyinotify.WatchManager()
FEVENTS = pyinotify.IN_CLOSE_WRITE

#-Manejador de Eventos declarados anteriormente
class EventHandler(pyinotify.ProcessEvent):
  def process_IN_CLOSE_WRITE (self, event):
   global change_flag
   change_flag=1
   
notifier = pyinotify.ThreadedNotifier(wm, EventHandler())
notifier.start()
wdd = wm.add_watch(FWATCH,FEVENTS)

#-------------------------------------------
# Funciones utilizadas
#------------------------------------------

#-Leemos la UART para tomar nuevas medidas
def nuevasMedidas():
 try:
    cadena=ser.leerSerial()
    if (len(cadena)):
     print cadena
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
      #Actualizo el ID_red del sensor si ha cambiado
      if (int(parsed_json['N'])):
        db.updateId_red(Id,int(parsed_json['R']))
     else:
	  print "Sensor no esta en la base de datos"
 except ValueError, e:
	print "Error al parsear el JSON",e	

#-Aplicamos los cambios efectuados en el servidorWeb
def cambiosServidor():
 try:
   
   #Leemos el fichero
   f = open("exchange.txt","r")
   lines = f.readlines()
   f.close()
   
   #Vaciamos el fichero
   f = open("exchange.txt","w")
   f.close()
   global change_flag
   change_flag = 0
   
   #Aplicamos los cambios
   for line in lines:
    datos=line.split(',')
    fun=datos[0]

    #Elijo la funcion adecuada
    if(fun=="DELETE"):
     db.borrarSensor(int(datos[1]),datos[2])
    elif(fun=="INSERT"):
     id_nodo=datos[1]
     loc=datos[2]
     id_red=datos[3]
     s=[] 
     i=4
     l1=len(datos)-1
     while i<l1:
      s.append([id,datos[i],datos[i+1],loc])
      i=i+2
     db.nuevoSensor(s)
    elif(fun=="RESET"):
      print datos
    elif(fun=="SET"):
      print datos
    else:
     print"Opcion no contemplada"
   
   #Recargamos la cache
   global r_sensores 
   r_sensores=db.cargarSensores()
 
 except IOError:
  print "Error al abrir el archivo"

#------------------------------------------
#   Programa Principal
#-------------------------------------------
while True:
 #ser.comandosAT() #Mandar comandos AT
 try:
   nuevasMedidas() #Tomar medidas de la UART
   #Subir un conjunto de medidas
   if (len(r_medidas)>=MAX_MEDIDAS):
      db.nuevaMedida(r_medidas)
      r_medidas=[]
      db.TablaMedidas() 
   
   #Atendemos a los cambios del servidorWeb
   if(change_flag):
    cambiosServidor() 
  
 except KeyboardInterrupt:
  #- Dejamos de observar el fichero exchange.txt
  wm.rm_watch(wdd.values())
  notifier.stop()
  #- Cerramos el puerto serie y acabamos el programa
  ser.closeSerial(Puerto)

