DOMOlabo B105
===================

This project consist on a Node.js-based Raspberry Pi monitoring panel that allows to check the Temperature, Presence, Light, Battery, Power Consumption, Presure, Humidity. 

This is a very useful web app for checking the status not only of the B105 lab but also of a complete university campus.

# Author

This project has been developed by [Adrián Arévalo Aguirre](http://github.com/arebus93 "Adrián Arévalo Aguirre").

# Screenshots
![Graficas de Medidas en Tiempo Real](https://lh5.googleusercontent.com/Pbs-CcQ4v_jOKrM0-htmor1VUC86MNNN8nww3ziEqbLGFFNd5DR4L8KYQXBAc6J2U6BB7lfQmZPWnNA=w1256-h555-rw "Graficas en Tiempo Real")

![Graficas del Historico de medidas](https://lh4.googleusercontent.com/r3mWgXOo21uK5hODsQ_eTkHU9pyXod2MCW9AeA3VQVwkSwKlA7tedXybJk2ee8X2zPngZNr6qSsF02I=w1256-h555-rw "Graficas del Historico de medidas")

![Panel de Control](https://lh5.googleusercontent.com/jLqWJDiyEbF8PwRFUtODcsI_3S7fuJ91T2dHXof0q2X4QbJo8VdKwF2q2BHDYnTxX0-wqzAp7foolmE=w1256-h555-rw "Panel de Control")


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


