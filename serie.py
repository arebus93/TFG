#!/usr/bin/python

import serial
import RPi.GPIO as GPIO
import time
import sys 

#--Funcion para leer el puerto serie
def readSerial():
 if(s.inWaiting()):
  return s.readline()
 else:
  return ""

def writeSerial(cadena):
 s.write(cadena)
 return

#--Configuracion del modulo HC-11 con comandos AT
def comandosAT():
 GPIO.output(17,GPIO.LOW)
 time.sleep(0.7)
 print "Inicio de comandos AT" 

 comando=raw_input()
 s.write(comando)
 print s.readline()
 #print s.readline() #Descomentar para comandos
 #print s.readline() #con mas valores de retorno 
 #print s.readline()
 #print s.readline()

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

 print "Configuracion UART"
 print "Puerto: %s" %(puerto) #Puerto
 print "Velocidad: %s" %(vel) #Baudrate
 print "Timeout: %s\n" %(timer) #Timeout 
 
#-- Funcion para cerrar el puerto serie
def closeSerial(puerto):
 try:
  s.close() 

 except serial.SerialException:
   sys.stderr.write("Error al cerrar puerto (%s)\n" % str(puerto))
   sys.exit(1)

 print "Puerto: %s cerrado" %(puerto)
 sys.exit(0)

