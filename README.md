DOMOlabo B105
===================

This project consist on a Node.js-based Raspberry Pi monitoring panel that allows to check the Temperature, Presence, Light, Battery, Power Consumption, Presure, Humidity. 

This is a very useful web app for checking the status not only of the B105 lab but also of a complete university campus.

# Author

This project has been developed by [Adrián Arévalo Aguirre](http://github.com/arebus93 "Adrián Arévalo Aguirre").

# Screenshots
[Graficas de Medidas en Tiempo Real](http://i1.wp.com/geekytheory.com/wp-content/uploads/2013/12/panel-monitorizacion-raspberry//-pi-node-js.png "Graficas en Tiempo Real")

![Graficas del Historico de medidas](http://i1.wp.com/geekytheory.com/wp-content/uploads/2013/12/panel-monitorizacion-raspberry//-pi-node-js.png "Graficas del Historico de medidas")

# How to install

**STEP 1: Actualizar la raspbery**
~~~
$ sudo apt-get update 
$ sudo apt-get upgrade
~~~
**STEP 2: Instalacion Node v0.10.24**
~~~
$ cd
$ sudo wget http://nodejs.org/dist/v0.10.24/node-v0.10.24-linux-arm-pi.tar.gz
$ cd /usr/local
$ sudo tar xvzf ~/node-v0.10.24-linux-arm-pi.tar.gz --strip=1
~~~
Para comprobar que se ha instalado correctamente, comprobar con:
~~~
node -v
~~~
**STEP 3: Instalar GIT y clonar el repositorio**
~~~
$ sudo apt-get install git
~~~
Clonar el repositorio remoto en la carpeta que queramos
~~~
$ cd /media/Transcend/DomoB105/
$ sudo git clone https://github.com/arebus93/TFG.git
~~~
**STEP 4: Entrar en la carpeta TFG, donde esta el codigo del proyecto**
~~~
$ cd TFG
~~~
**STEP 5: Instalar las dependencias**
~~~
$ sudo npm install
~~~
If everything is OK, go to step 6. If it throws an error:
~~~
npm config set registry http://registry.npmjs.org/
~~~
~~~
npm install
~~~
**STEP 6: Eejcutar el servidor**
~~~
$ nodejs server.js
~~~
**STEP 7: Conectarse desde un navegador**

Open a browser with your Raspberry Pi's IP and start to listen the port 8000. For example: [http://192.168.1.100:8000](http://192.168.1.100:8000)


