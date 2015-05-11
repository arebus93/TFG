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

#--Funcion para insertar sensores

def nuevoSensor(ref, tipo,loc):

	bd = sqlite3.connect('database.sqlite3')
	cursor = bd.cursor()

	sql = "INSERT INTO Sensores(Referencia, Tipo, Localizacion) VALUES (1001, 'Temperatura', 1)"
	try:
   		cursor.execute(sql)
   		bd.commit()
	except sqlite3.Error, e:
		print "Error %s:" %e.args[0]
		bd.rollback()

	bd.close()

#--Funcion para borrar sensores
#--Borra el sensor de la tabla de sensores y todas las medidas asociadas

def mostrarSensores():

	bd = sqlite3.connect('database.sqlite3')
	cursor = bd.cursor()
	
	sql = "SELECT * FROM Sensores"
	try:
		cursor.execute(sql)
		#Obtenemos todos los registros en una lista de listas	
		rows=cursor.fetchall()
		for row in rows:
			 print "%d %d %s %d " % (row[0], row[1], row[2],row[3])

        except sqlite3.Error, e:
		print "Error %s:" %e.args[0]
		bd.rollback()

	bd.close()

def borrarSensor(ref):

	bd = sqlite3.connect('database.sqlite3')
	cursor = bd.cursor()

	sql = "DELETE FROM Sensores WHERE REFERENCIA=ref"
	sql1 = "DELETE FROM Medidas WHERE REFERENCIA=ref" 
	try:
		cursor.execute(sql)
		cursor.execute(sql1)
		bd.commit()

        except sqlite3.Error, e:
		print "Error %s:" %e.args[0]
		bd.rollback()

	bd.close()
