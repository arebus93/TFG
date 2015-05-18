#!/usr/bin/python
 
import sqlite3
import os

#--Funcion para crear las tablas en la base de datos

def crearTablas():
	#Conexion base de datos
	bd = sqlite3.connect('database.sqlite3')
	cursor = bd.cursor()

	sql = """CREATE TABLE IF NOT EXISTS Sensores(
		Num_registro INTEGER PRIMARY KEY,
		Id INTEGER NOT NULL,
		Referencia INTEGER NOT NULL UNIQUE,
		Tipo VARCHAR(40) NOT NULL,
		Localizacion INTEGER NOT NULL)
		"""
	sql1 = """CREATE TABLE IF NOT EXISTS Medidas(
		Num_registro INTEGER PRIMARY KEY,
		Referencia INTEGER NOT NULL,
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

#--Funcion para crear un sensor nuevo
def nuevoSensor(id,ref,tipo,loc):
	bd = sqlite3.connect('database.sqlite3')
	cursor = bd.cursor()
	sensor=(id,ref,tipo,loc)
	sql = 'INSERT INTO Sensores(Id, Referencia, Tipo, Localizacion) VALUES(?,?,?,?)'
        try:
                cursor.execute(sql,sensor)
                #Obtenemos todos los registros en una lista de listas
                rows=cursor.fetchall()
                return rows

        except sqlite3.Error, e:
                print "Error %s:" %e.args[0]
                bd.rollback()

        bd.close()

#--Funcion para cargar la red de sensores

def cargarSensores():

	bd = sqlite3.connect('database.sqlite3')
	cursor = bd.cursor()

	r_sensores =[ (1,11,'Temperatura', 1),
		      (1,17,'Humedad', 1),
		      (1,16,'Presion', 1),
               	      (1,13,'Luminosidad',1)]

	sql = 'INSERT INTO Sensores(Id, Referencia, Tipo, Localizacion) VALUES(?,?,?,?)'
	try:
   		cursor.executemany(sql,r_sensores)
   		bd.commit()
	except sqlite3.Error, e:
		print "Error %s:" %e.args[0]
		bd.rollback()

	bd.close()


#-- Funcion que devuelve sensores del dispositivo con  ese id

def infoSensor(id):

	bd = sqlite3.connect('database.sqlite3')
	cursor = bd.cursor()
	ident=(id,)
	sql = "SELECT Referencia, Tipo FROM Sensores WHERE Id=?"
	try:
		cursor.execute(sql,ident)
		#Obtenemos todos los registros en una lista de listas	
		rows=cursor.fetchall()
		return rows
		
	except sqlite3.Error, e:
		print "Error %s:" %e.args[0]
		bd.rollback()

	bd.close()

#--Funcion para mostrar Tabla Sensores

def TablaSensores():

	bd = sqlite3.connect('database.sqlite3')
	cursor = bd.cursor()
	
	sql = "SELECT * FROM Sensores"
	try:
		cursor.execute(sql)
		#Obtenemos todos los registros en una lista de listas	
		rows=cursor.fetchall()
		for row in rows:
			 print "%d %d %d %s %d " % (row[0], row[1], row[2],row[3], row[4])
			 
        except sqlite3.Error, e:
		print "Error %s:" %e.args[0]
		bd.rollback()

	bd.close()

#--Funcion para borrar sensores
#--Borra el sensor de la tabla de sensores y todas las medidas asociadas

def borrarSensor(ref):

	bd = sqlite3.connect('database.sqlite3')
	cursor = bd.cursor()
        refer=(ref,)
	sql = "DELETE FROM Sensores WHERE Referencia=?"
	sql1 = "DELETE FROM Medidas WHERE Referencia=?" 
	try:
		cursor.execute(sql,refer)
		cursor.execute(sql1,refer)
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
	sql = "INSERT INTO Medidas (Referencia, Valor, Fecha, Hora) VALUES(?,?,?,?)"
	try:
   		cursor.executemany(sql,r_medidas)
   		bd.commit()
	except sqlite3.Error, e:
		print "Error %s:" %e.args[0]
   		bd.rollback()

   	bd.close()

#--Funcion para borrar medidas

def borrarMedida(ref, fecha, hora):

	bd = sqlite3.connect('database.sqlite3')
	cursor = bd.cursor()
	medida=(ref,fecha,hora)
	sql = "DELETE FROM Medidas WHERE (Referencia=? AND Fecha=? AND  Hora=?)";
	try:
	   cursor.execute(sql, medida)
	   bd.commit()

        except sqlite3.Error, e:
                print "Error %s:" %e.args[0]
                bd.rollback()

	bd.close()

#-- Funcion mostrar medidas recogidas por un sensor

def medidasSensor(ref):
	bd = sqlite3.connect('database.sqlite3')
	cursor = bd.cursor()
	refer=(ref,)
	sql = "SELECT * FROM Medidas WHERE Referencia=?"
	try:
		cursor.execute(sql,refer)
		rows=cursor.fetchall()
		for row in rows:
			print "%d %d %d %s %s " % (row[0], row[1], row[2],row[3],row[4])
	except sqlite3.Error, e:
        	print "Error %s:" %e.args[0]
        	bd.rollback()
	bd.close()

#--Funcion para mostrar Tabla Medidas

def TablaMedidas():

	bd = sqlite3.connect('database.sqlite3')
	cursor = bd.cursor()
	
	sql = "SELECT * FROM Medidas"
	try:
		cursor.execute(sql)
		#Obtenemos todos los registros en una lista de listas	
		rows=cursor.fetchall()
		for row in rows:
			 print "%d %d %d %s %s " % (row[0], row[1], row[2],row[3],row[4])

        except sqlite3.Error, e:
		print "Error %s:" %e.args[0]
		bd.rollback()
	bd.close()
