#!/usr/bin/python

import serial
import RPi.GPIO as GPIO
import time

 
#--Funcion para leer el puerto serie

def leerSerial():
 print "Inicio de lectura puerto serie"
 while True:
   if s.inWaiting():
    print s.readline()

#--Configuracion del modulo HC-11 con comandos AT

def comandosAT():
 GPIO.output(17,GPIO.LOW)
 time.sleep(0.5)
 print "Inicio de comandos AT" 
 while True:
  comando=raw_input()
  s.write(comando)
  print s.readline()
  print s.readline() #Descomentar para comandos
  print s.readline() #con mas valores de retorno 
  print s.readline()
  print s.readline()

#--Funcion para inicializar el puerto serie y los GPIOs necesarios

def initSerial(puerto,vel,timer):

 #-- Definicion de GPIOs y valores por defecto
 GPIO.setmode(GPIO.BCM)
 GPIO.setwarnings(False)
 GPIO.setup(17,GPIO.OUT)
 GPIO.output(17,GPIO.HIGH)
 time.sleep(0.5)

 try:
  global s
  s=serial.Serial(puerto,vel)
  s.timeout=timer
  s.open()

 except serial.SerialException:
   sys.stderr.write("Error al abrir puerto (%s)\n" % str(puerto))
   sys.exit(1)

 print "Puerto: %s" %(puerto) #Puerto
 print "Velocidad: %s" %(vel) #Baudrate
 print "Timeout: %s" %(timer) #Timeout 

#-- Funcion para cerrar el puerto serie

def closeSerial(puerto):
 s.close() 
 print "Puerto: %s cerrado" %(puerto)
