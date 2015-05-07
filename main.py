#!/usr/bin/python

#import database
import serial
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17,GPIO.OUT)
GPIO.output(17,GPIO.HIGH) 
time.sleep(0.5)

def leerSerial(): 
 print "Inicio de lectura puerto serie"
 while True:
   if s.inWaiting():
    print  s.readline()

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

#------------------------------------------
#   Programa Principal
#-------------------------------------------
Puerto= '/dev/ttyAMA0' 
Vel=9600
Timeout=1

try:
	s=serial.Serial(Puerto,Vel)
	s.timeout=Timeout
	s.open()

except serial.SerialException:
   #-- Error al abrir el puerto serie
   sys.stderr.write("Error al abrir puerto (%s)\n" % str(Puerto))
   sys.exit(1)

   #-- Mostrar el nombre del dispositivo serie utilizado
print "Puerto: %s" %(Puerto)

#comandosAT() #--Configuracion del modulo HC-11 con comandos AT
leerSerial()
s.close() #-- Cerramos el puerto serie
print "Puerto: %s cerrado" %(Puerto)

