#!/usr/bin/python
 
import sqlite3
import os

#--Funcion para crear las tablas en la base de datos

def crearTablas():
	#Conexion base de datos
	bd = sqlite3.connect('database.sqlite3')
	cursor = bd.cursor()

	sql = """CREATE TABLE IF NOT EXISTS Sensores(
		Id INTEGER NOT NULL,
		Referencia INTEGER PRIMARY KEY,
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

#--Funcion para crear nuevos sensores

def nuevoSensor(r_sensores):

	bd = sqlite3.connect('database.sqlite3')
	cursor = bd.cursor()

	sql = 'INSERT INTO Sensores VALUES(?,?,?,?)'

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

        sql = "SELECT Id, Referencia FROM Sensores ORDER BY Referencia ASC"

	try:
   		cursor.execute(sql)	
		rows=cursor.fetchall()

		d={}
		for x,y in rows:
		 d.setdefault(x,[]).append(y)
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
			 print "%d %d %s %d " % (row[0], row[1], row[2],row[3])
			 
        except sqlite3.Error, e:
		print "Error %s:" %e.args[0]
		
	bd.close()

#--Funcion para borrar sensores
#--Borra el sensor de la tabla de sensores y/o todas las medidas asociadas
#- en funcion de flag

def borrarSensor(id,flag):

	bd = sqlite3.connect('database.sqlite3')
	cursor = bd.cursor()
        ident=(id,)
        sql =  "DELETE FROM Sensores WHERE Id=?"
	if (flag):
	 refs=(id*10,id*10+11)
	 sql1 = "DELETE FROM Medidas WHERE Referencia > ? AND Referencia < ?" 
	try:
		cursor.execute(sql,ident)
		if(flag):
		  cursor.execute(sql1,refs)
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
