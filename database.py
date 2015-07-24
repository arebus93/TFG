#!/usr/bin/python
 
import sqlite3
import os

#--Funcion para crear las tablas en la base de datos

def crearTablas():
	#Conexion base de datos
	bd = sqlite3.connect('database.sqlite3')
	cursor = bd.cursor()

	sql = """CREATE TABLE IF NOT EXISTS Sensores(
		Id_nodo INTEGER NOT NULL,
		Id_sensor INTEGER PRIMARY KEY,
		Tipo VARCHAR(40) NOT NULL,
		Localizacion INTEGER NOT NULL,
		Id_red INTEGER NOT NULL,
		Estado INTEGER NOT NULL)
		"""
	sql1 = """CREATE TABLE IF NOT EXISTS Medidas(
		Num_registro INTEGER PRIMARY KEY,
		Id_sensor INTEGER NOT NULL,
		Valor INTEGER NOT NULL,
		Fecha DATE NOT NULL,
		Hora TIME NOT NULL)
		"""
	try:
		#Ejecutamos los comandos 
	   	cursor.execute(sql)
	   	cursor.execute(sql1)
	   	#Efectuamos los cambios en la base de datos
	   	bd.commit()
	except sqlite3.Error, e:
		#Si se genero algun error lo imprimimos y  revertimos la operacion
		bd.rollback()
		print "Error %s:" % e.args[0]
   	#Desconexion base de datos
 	bd.close()
	
	#Proporcionamos permisos de lectura escritura
	os.chmod("database.sqlite3",0666)


#------------------------------------------------------
#- Funciones Sensores
#-------------------------------------------------------

#--Funcion para crear nuevos sensores
def nuevoSensor(r_sensores):

	bd = sqlite3.connect('database.sqlite3')
	cursor = bd.cursor()

	sql = 'INSERT INTO Sensores VALUES(?,?,?,?,?,?)'

        try:
            cursor.executemany(sql,r_sensores)
            bd.commit()                
                                
        except sqlite3.Error, e:
                print "Error %s:\n" %e.args[0]
                bd.rollback()

        bd.close()

#--Funcion para cargar la cache de sensores
def cargarSensores():

	bd = sqlite3.connect('database.sqlite3')
	cursor = bd.cursor()

        sql = "SELECT Id_nodo,Id_sensor,Id_red,Estado FROM Sensores ORDER BY Id_sensor ASC"

	try:
   		cursor.execute(sql)	
		rows=cursor.fetchall()
		d={}
		#-Creamos la cache de sensores, donde el primer elemento
		#- es el id_red y el resto son los sensores del nodo
		for x,y,z,w in rows:
		 if x in d.keys():
        	   d[x].append(y)
    		 else:
        	   d[x]=[z,w,y]
	        print d
		return d

	except sqlite3.Error, e:
		print "Error %s:" %e.args[0]
		
	bd.close()

#--Funcion para mostrar Tabla Sensores
def TablaSensores():

	bd = sqlite3.connect('database.sqlite3')
	cursor = bd.cursor()
	
	sql = "SELECT * FROM Sensores"
	
	try:
		cursor.execute(sql)
		rows=cursor.fetchall()
		for row in rows:
			 print "%d %d %s %d %d %d" % (row[0], row[1], row[2],row[3],row[4],row[5])
			 
        except sqlite3.Error, e:
		print "Error %s:" %e.args[0]
		
	bd.close()

#--Funcion para borrar sensores
#--Borra el sensor de la tabla de sensores y/o todas las medidas asociadas
#- en funcion de flag
def borrarSensor(id_nodo,flag):

	bd = sqlite3.connect('database.sqlite3')
	cursor = bd.cursor()
        ident=(id_nodo,)
        sql =  "DELETE FROM Sensores WHERE Id_nodo=?"
	if (flag):
	 refs=(id_nodo*10,id_nodo*10+11)
	 sql1 = "DELETE FROM Medidas WHERE Id_sensor > ? AND Id_sensor < ?" 
	try:
		cursor.execute(sql,ident)
		if(flag):
		  cursor.execute(sql1,refs)
	          bd.commit()

        except sqlite3.Error, e:
		print "Error %s:" %e.args[0]
		bd.rollback()

	bd.close()

#--Funcion para actualizar el ID_red
def updateId_red(id_nodo,id_red):

	bd = sqlite3.connect('database.sqlite3')
	cursor = bd.cursor()
	if(id_red == -1 and id_nodo == -1):
	 ident=(id_red,)
	 sql= "UPDATE Sensores SET Id_red = ?"
	else:
         ident=(id_red,id_nodo)
         sql = "UPDATE Sensores SET Id_red = ? WHERE Id_nodo= ?"
	try:
   		cursor.execute(sql,ident)
   		bd.commit()
	except sqlite3.Error, e:
		print "Error %s:" %e.args[0]
   		bd.rollback()

   	bd.close()

#--Funcion para actualizar el estado
def updateEstado(id_nodo,estado):

        bd = sqlite3.connect('database.sqlite3')
        cursor = bd.cursor()
        ident=(estado,id_nodo)
        sql = "UPDATE Sensores SET Estado = ? WHERE Id_nodo= ?"
        try:
                cursor.execute(sql,ident)
                bd.commit()
        except sqlite3.Error, e:
                print "Error %s:" %e.args[0]
                bd.rollback()

        bd.close()

#-------------------------------------------------------
#- Funciones Medidas
#-------------------------------------------------------

#--Funcion para insertar varias medidas
def nuevaMedida(r_medidas):
	
	bd = sqlite3.connect('database.sqlite3')
	cursor = bd.cursor()
	
	sql = "INSERT INTO Medidas (Id_sensor, Valor, Fecha, Hora) VALUES(?,?,?,?)"
	
	try:
   		cursor.executemany(sql,r_medidas)
   		bd.commit()
	except sqlite3.Error, e:
		print "Error %s:" %e.args[0]
   		bd.rollback()

   	bd.close()

#--Funcion para borrar medidas
def borrarMedida(id_sensor, fecha, hora):

	bd = sqlite3.connect('database.sqlite3')
	cursor = bd.cursor()
	medida=(id_sensor,fecha,hora)
	
	sql = "DELETE FROM Medidas WHERE (Id_sensor=? AND Fecha=? AND  Hora=?)";
	
	try:
	   cursor.execute(sql, medida)
	   bd.commit()

        except sqlite3.Error, e:
                print "Error %s:" %e.args[0]
                bd.rollback()

	bd.close()

#-- Funcion mostrar medidas recogidas por un sensor
def medidasSensor(id_sensor):
	bd = sqlite3.connect('database.sqlite3')
	cursor = bd.cursor()
	ident=(id_sensor,)
	
	sql = "SELECT * FROM Medidas WHERE id_sensor=?"
	
	try:
		cursor.execute(sql,ident)
		rows=cursor.fetchall()
		for row in rows:
			print "%d %d %d %s %s " % (row[0], row[1], row[2],row[3],row[4])
	
	except sqlite3.Error, e:
        	print "Error %s:" %e.args[0]
        bd.close()

#--Funcion para mostrar Tabla Medidas
def TablaMedidas():

	bd = sqlite3.connect('database.sqlite3')
	cursor = bd.cursor()
	
	sql = "SELECT * FROM Medidas"
	
	try:
		cursor.execute(sql)
		rows=cursor.fetchall()
		for row in rows:
		  print "%d %d %d %s %s " % (row[0], row[1], row[2],row[3],row[4])

        except sqlite3.Error, e:
		print "Error %s:" %e.args[0]
	bd.close()

