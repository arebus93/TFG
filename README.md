Raspberry Pi Monitoring Panel
===================

This project consist on a Node.js-based Raspberry Pi monitoring panel that allows to check the temperature, presence, light, Battery, Power Consumption, Presure, Humidity. 

This is a very useful web app for checking the status not only of the B105 lab but also of a complete university campus .

# Author

This project has been developed by [Adrián Arévalo Aguirre](http://github.com/arebus93 "Adrián Arévalo Aguirre").

#### Contributors

# Screenshot
![Raspberry Pi Monitoring Panel](http://i1.wp.com/geekytheory.com/wp-content/uploads/2013/12/panel-monitorizacion-raspberry-pi-node-js.png "Raspberry Pi Monitoring Panel")

# How to install

**STEP 1:**
~~~
$ sudo apt-get update && sudo apt-get upgrade
~~~
**STEP 2:**
~~~
$ sudo apt-get install nodejs npm git
~~~
**STEP 3:**
~~~
$ git clone https://github.com/arebus93/TFG.git
~~~
**STEP 4:**
~~~
$ cd serverNode
~~~
**STEP 5:**
~~~
$ npm install
~~~
If everything is OK, go to step 6. If it throws an error:
~~~
npm config set registry http://registry.npmjs.org/
~~~
~~~
npm install
~~~
**STEP 6:**
~~~
$ nodejs server.js
~~~
**STEP 7:**

Open a browser with your Raspberry Pi's IP and start to listen the port 8000. For example: [http://192.168.1.100:8000](http://192.168.1.100:8000)


