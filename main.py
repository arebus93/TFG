#!/usr/bin/python
# coding=utf-8

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
precarga_sensores =[ (0,01,'Temperatura',0,0,0),(0,02,'Presencia',0,0,0),(0,04,'Bateria',0,0,0),
		     (1,11,'Temperatura',1,-1,0),(1,12,'Presencia',1,-1,0),(1,14,'Bateria',1,-1,0),
		     (2,21,'Temperatura',2,-1,0),(2,22,'Presencia',2,-1,0),(2,24,'Bateria',2,-1,0),
		     (3,31,'Temperatura',3,-1,0),(3,32,'Presencia',3,-1,0),(3,34,'Bateria',3,-1,0),
                     (4,41,'Temperatura',4,-1,0),(4,42,'Presencia',4,-1,0),(4,44,'Bateria',4,-1,0),
                     (5,51,'Temperatura',5,-1,0),(5,52,'Presencia',5,-1,0),(5,54,'Bateria',5,-1,0),
                     (6,61,'Temperatura',6,-1,0),(6,62,'Presencia',6,-1,0),(6,64,'Bateria',6,-1,0),
                     (7,71,'Temperatura',7,-1,0),(7,72,'Presencia',7,-1,0),(7,74,'Bateria',7,-1,0),
                     (8,81,'Temperatura',8,-1,0),(8,82,'Presencia',8,-1,0),(8,84,'Bateria',8,-1,0),
                     (9,91,'Temperatura',9,-1,0),(9,92,'Presencia',9,-1,0),(9,94,'Bateria',9,-1,0),
		     (10,101,'Temperatura',10,-1,0),(10,104,'Bateria',10,-1,0),(10,105,'Consumo',10,-1,0),
		     (11,111,'Temperatura',11,-1,0),(11,114,'Bateria',11,-1,0),(11,115,'Consumo',11,-1,0)]
db.nuevoSensor(precarga_sensores)

#- A continuacion actualizamos la cache de sensores
#- con cargasensores()
r_sensores=db.cargarSensores()

#- Lista que guarda las medidas  para subir a la base de datos.
#- cuando tiene MAX_MEDIDAS
r_medidas=[]
estado=0
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
    cadena=ser.readSerial()
    if (len(cadena)>2):
     print cadena
     parsed_json = json.loads(cadena)
     Id=int(parsed_json['I'])
     #-Buscamos en la cache r_sensores si existe,
     #-su id-red y los sensores que tiene declarados
     if r_sensores.has_key(Id):
      rows=r_sensores[Id]
      #-Actualizo el ID_red del sensor si ha cambiado
      #-o no se ha inicializado
      if ((rows[0]== -1) or (int(parsed_json['N'])== 1)):
        db.updateId_red(Id,int(parsed_json['R']))
        #-Recargamos la cache
	global r_sensores
        r_sensores=db.cargarSensores()
      else:
       for i in rows[2:]:
        x=(i%10)-1
        tS=T_sensores[x] #Tipo
      	m=int(parsed_json[tS]) #Medida
    	t=ser.time.strftime('%H:%M:%S') #Time
    	d=ser.time.strftime('%Y/%-m/%-d') #Date
  	r_medidas.append([i,m,d,t])  			 
     else:
	  print "Sensor no esta en la base de datos"
 except ValueError, e:
	print "Error al parsear el JSON",e	
	
#-Aplicamos los cambios efectuados en el servidorWeb
def cambiosServidor():
 try:
   #-Leemos el fichero
   f = open("exchange.txt","r")
   lines = f.readlines()
   f.close()
   
   #-Vaciamos el fichero
   f = open("exchange.txt","w")
   f.close()
   global change_flag
   change_flag = 0
   
   #-Aplicamos los cambios
   for line in lines:
    datos=line.split(',')
    fun=datos[0]

    #-Elijo la funcion adecuada
 
    if(fun=="DELETE"):
     #-Borramos el sensor de la BD
     db.borrarSensor(int(datos[1]),datos[2])
     #-Recargamos la cache
     global r_sensores
     r_sensores=db.cargarSensores()

    elif(fun=="INSERT"):
     id_nodo=datos[1]
     loc=datos[2]
     id_red=datos[3]
     estado=datos[4]
     s=[] 
     i=5
     l1=len(datos)-1
     while i<l1:
      s.append([id_nodo,datos[i],datos[i+1],loc,id_red,estado])
      i=i+2
     #-Añadimos el sensor a la BD
     db.nuevoSensor(s)
     #-Recargamos la cache
     global r_sensores
     r_sensores=db.cargarSensores()

    elif(fun=="RESET"):
      id_red=datos[1]
      if(id_red=='0'): #-Reset AP
	cadena='{\"RST\"}\n'
	db.updateId_red(-1,-1)	
      else:     #-Reset ED
	cadena='{\"ID\":'+ id_red + ',\"CNF\",{\"RST\"}}\n'
      print cadena
      #-Enviamos el comando de RESET a traves de la UART
      ser.writeSerial(cadena+chr(23))#-ETB

    elif(fun=="SET"):
      acc = datos[1]
      id_red = datos[2]

      if(acc=="TIME"):
       Tsleep =datos[3]
       Twake = datos[4]   
       cadena='{\"ID\":'+ id_red + ',\"CNF\",{\"AT\":'+ Twake +',"ST\":'+ Tsleep +'}}\n'

      elif(acc=="RELE"):
       flag = int(datos[3])
       id_nodo = int (datos[4])
       cadena = '{\"ID\":'+ id_red + ',\"CNF\",{\"A\":'+ datos[3] +'}}\n'
       #- Actualiza el estado nodo
       estado=r_sensores[id_nodo][1]
       if(estado==0):   #RELE OFF/LED OFF
        if(flag == 1):
	  estado=1
       elif(estado==1): #RELE ON/LED OFF
        if(flag==0):
	  estado=0
       elif(estado==2):  #RELE OFF/LED ON
        if(flag==1):
	  estado=3
       else:             #RELE ON/LED ON
        if(flag==0):
	  estado=2
       db.updateEstado(id_nodo,estado)

      elif(acc=="LEDS"):
	flag = int(datos[3])
	id_nodo = int(datos[4])
        cadena = '{\"ID\":'+ id_red + ',\"CNF\",{\"LD\":'+ datos[3] +'}}\n'
	#- Actualiza el estado nodo
	estado=r_sensores[int(id_nodo)][1]
	if(estado==0): #RELE OFF/LED OFF
	 if(flag==1):
	  estado=2
	elif(estado==1): #RELE ON/LED OFF
         if(flag==1):
          estado=3
	elif(estado==2):  #RELE OFF/LED ON
         if(flag==0):
          estado=0
	else:             #RELE ON/LED ON
	 if(flag==0):
	  estado=1
      	db.updateEstado(id_nodo,estado)
      else:
	print "Opcion SET no contemplada" 

      print cadena
      #-Enviamos el comando de SET a traves de la UART
      ser.writeSerial(cadena+chr(23))#- ETB

    else:
     print"Opcion del fichero exchnge no contemplada"
   
 except IOError:
  print "Error al abrir el archivo"

#------------------------------------------
#   Programa Principal
#-------------------------------------------
while True:
 #ser.comandosAT() #-Mandar comandos AT
 try:
   nuevasMedidas() #-Tomar medidas de la UART
   #Subir un conjunto de medidas
   if (len(r_medidas)>=MAX_MEDIDAS):
      db.nuevaMedida(r_medidas)
      r_medidas=[]
     # db.TablaMedidas() 
   
   #-Atendemos a los cambios del servidorWeb
   if(change_flag):
    cambiosServidor() 
  
 except KeyboardInterrupt:
  #- Dejamos de observar el fichero exchange.txt
  wm.rm_watch(wdd.values())
  notifier.stop()
  #- Cerramos el puerto serie y acabamos el programa
  ser.closeSerial(Puerto)

