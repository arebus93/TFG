/** Autor: Adrián Arévalo Aguirre**/ 
var port = 8000;
var auth = require("http-auth");
var digest = auth.digest({
    realm: "B105 users only",
    file: __dirname + "/htpass",
    msg401: "ERROR 401: Unautorized Access:Para acceso sin privilegios de admin probar weather/weather"
});

var app = require('http').createServer(digest,handler).listen(port),
  io = require('socket.io').listen(app),
  fs = require('fs'),
  url = require('url'),
  sqlite3=require('sqlite3').verbose();

var connectCounter = 0;
var timerWeb =30000;//Tiempo de refresco en ms(30s).
var lastRead=0; //Ultimo Num_registro leido de Medidas.
var T_sensors=[['T','P','L','B','C','A','H','G'],['Temp','Pres','Lum','Bat','Cons','Atm','Hum','TCPU'],['Temperatura','Presencia','Luminosidad','Bateria','Consumo','Presion','Humedad','TCPU']]; 

//Si todo va bien al abrir el navegador, cargaremos el html adecuado.
function handler(req, res) {
 path = url.parse(req.url).pathname;
 user = req.user;
  switch(path) {
    case '/': //Carga la pagina principal de informacion.
      fs.readFile(__dirname+'/index.html', function(err, data) {
      if (err) {
        //Si hay error, mandaremos un mensaje de error 500
        console.log(err);
        res.writeHead(500);
        return res.end('Error loading index.html');
      }
      res.writeHead(200);
      res.end(data);
      });
      break;

    case '/2': //Carga la pagina del historico de informacion.
      fs.readFile(__dirname+'/index2.html',function(err, data) {
      if (err) {
        //Si hay error, mandaremos un mensaje de error 500
        console.log(err);
        res.writeHead(500);
        return res.end('Error loading index2.html');
      }
      res.writeHead(200);
      res.end(data);
      });
      break;

    case '/sensors': //Carga la pagina de sensores
      var p1='/nodes2.html'; //Cargo la pagina sin opciones de contol
      if(user === 'admin'){p1='/nodes.html'} //Cargo la de admin
      fs.readFile(__dirname+p1, function(err, data) {
      if (err) {
        //Si hay error, mandaremos un mensaje de error 500
        console.log(err);
        res.writeHead(500);
        return res.end('Error loading index.html');
      }
      res.writeHead(200);
      res.end(data);
      });
      break;

    case '/favicon.ico': //Carga el icono
     fs.readFile(__dirname+'/favicon.ico', function(err, data) {
      if (err) {
       //Si hay error,lo sacamos por consola
       console.log(err);
      }
      res.writeHead(200, {'Content-Type': 'image/x-icon'});
      res.end(data);
      });
      break;
    case '/distrNodos.jpg': //Carga la imagen
     fs.readFile(__dirname+'/distrNodos.jpg', function(err, data) {
      if (err) {
       //Si hay error,lo sacamos por consola
       console.log(err);
      }
      res.writeHead(200, {'Content-Type': 'image/x-icon'});
      res.end(data);
      });
      break;


    default: //No existe el path o no es accesible
      console.log('No existe el path'+path)
      res.writeHead(404);
      return res.end('Error path not found')
  }
}

//Cuando abramos el navegador estableceremos una conexión con socket.io. 
io.sockets.on('connection', function(socket) {
  var address = socket.handshake.address;
  console.log("New connection from " + address.address + ":" + address.port);
  connectCounter++;
  console.log("NUMBER OF CONNECTIONS++: "+connectCounter);

 //Añadimos un sensor a la base de datos
 socket.on('SNew', function (data){
   var id_nodo=data[0];
   var tipos=data[1].split(", ");
   var loc=data[2];
   var id_red=data[3];
   var datos=[];

   for(var i=0,l3=tipos.length-1;i<l3;i++){
    var t=(T_sensors[1].indexOf(tipos[i]));
    var tipo=T_sensors[2][t];
    var id_sensor=id_nodo*10+(t+1);
    datos.push([id_sensor,tipo]);
   }
   //Lo escribimos en el fichero exchange.txt
   var linea="INSERT,"+id_nodo+","+loc+","+id_red+","+datos+",\n";
   fs.appendFile('exchange.txt',linea,function(err){
    if(err){console.log('exec error: ' + err);}
   });
 }); 
 
 //Eliminamos un dispositivo final ED
 socket.on('SDelete', function (id_nodo, flag){
  //Lo escribimos en el fichero exchange.txt
  var linea="DELETE,"+id_nodo+","+flag+",\n"  
  fs.appendFile('exchange.txt',linea,function(err){
   if(err){console.log('exec error: ' + err);}
   });
 });

 //Resetear un nodo de la red (ED o AP)
 socket.on('SReset', function (id_red){
  if(id_red < 0){
   console.log("Nodo no inicializado");
  }else{
  //Lo escribimos en el fichero exchange.txt
  var linea="RESET,"+id_red+",\n"  
  fs.appendFile('exchange.txt',linea,function(err){
   if(err){console.log('exec error: ' + err);}
   });
  }
 });

 //Set de los tiempos de Tsleep y Twake de un dispositivo ED
 socket.on('STimer', function (id_red,TSleep,TWake){
  if(id_red < 0){
   console.log("Nodo no inicializado");
  }else{
  //Lo escribimos en el fichero exchange.txt
  var linea="SET,TIME,"+id_red+","+TSleep+","+TWake+",\n"  
  fs.appendFile('exchange.txt',linea,function(err){
   if(err){console.log('exec error: ' + err);}
   });
  }
 });

 //Set del Rele ON/OFF
  socket.on('SRele', function (id_red,id_nodo,flag){
  if(id_red < 0){
   console.log("Nodo no inicializado");
  }else{
  //Lo escribimos en el fichero exchange.txt
  var linea="SET,RELE,"+id_red+","+id_nodo+","+flag+",\n"
  fs.appendFile('exchange.txt',linea,function(err){
   if(err){console.log('exec error: ' + err);}
   });
  }
 });

 //Set de Led ED  ON/OFF
  socket.on('SLeds', function (id_red,id_nodo,flag){
  if(id_red < 0){
   console.log("Nodo no inicializado");
  }else{
  //Lo escribimos en el fichero exchange.txt
  var linea="SET,LEDS,"+id_red+","+id_nodo+","+flag+",\n"
  fs.appendFile('exchange.txt',linea,function(err){
   if(err){console.log('exec error: ' + err);}
   });
  }
 });

//Recarga un intervalo de medidas solicitado en una de las graficas 
 socket.on('Reload', function(t,min,max) {
  var dmin=new Date(min);
  var dmax=new Date(max);
  var fmin=dmin.getFullYear()+"/"+(dmin.getMonth()+1)+"/"+dmin.getDate();
  var fmax=dmax.getFullYear()+"/"+(dmax.getMonth()+1)+"/"+dmax.getDate();
  //var hmin=dmin.toLocaleTimeString();
  //var hmax=dmax.toLocaleTimeString();
  console.log(fmin,fmax);
  var tipo=T_sensors[2][T_sensors[0].indexOf(t)];
  var db = new sqlite3.Database('database.sqlite3',sqlite3.OPEN_READONLY);
  db.all("SELECT Id_sensor FROM Sensores WHERE Tipo ='"+tipo+"'ORDER BY Id_sensor", function (err,refs) {
   if(err){
       console.log('exec error: ' + err);
   }else{ //cargamos los sensores
      for(var i=0, l1=refs.length; i<l1;i++){
	console.log(refs);
        var r=refs[i].Id_sensor;
        (function(r){
	  db.all("SELECT Num_registro, Valor, Fecha, Hora FROM Medidas WHERE Id_sensor='"+r+"' AND (FECHA BETWEEN '"+fmin+"' AND '"+fmax+"') ORDER BY Num_registro" , function ( err2,rows) {
    	    if(err) {
              console.log('exec error: ' + err2);
            }else {
             //console.log(rows);
             socket_selector(socket,rows,r,'Load2');
            }
          })
        })(r);
      }
    }
  });
 db.close();
 });

 //Eliminamos la conexion
 socket.on('disconnect', function() {
  connectCounter--;
  console.log("NUMBER OF CONNECTIONS--: "+connectCounter);
 });

 // Visualizacion de los datos del sistema.
 if (typeof path != 'undefined'){
    switch(path){
    case '/': //Cargamos y actualizamos las graficas Tiempo real.
      infoTreal(socket);
    break;
    case '/2': //Cargamos y actualizamos las graficas Historico.
      infoHist(socket);
    break;
    case '/sensors': //Cargamos y actualizamos los sensores.
     sensores(socket);
     break;
  }
 }
});

// Funcion para cargar las graficas de medidas en Tiempo real
//Cada timerWeb milisegundos mandaremos a la gráfica un nuevo valor.
function infoTreal(socket) {
  var f = new Date();
  var factual=f.getFullYear() + "/" + (f.getMonth() +1) + "/" + f.getDate();
  // var factual= 2015+"/"+7+"/"+15; //Forzar la carga de un dia
  console.log(factual);
  var db = new sqlite3.Database('database.sqlite3',sqlite3.OPEN_READONLY);
 db.all("SELECT Id_sensor FROM Sensores ORDER BY Id_sensor", function (err,refs) {
    if(err){
       console.log('exec error: ' + err);
    }else{ //cargamos los sensores
      for(var i=0, l1=refs.length; i<l1;i++){
        var r=refs[i].Id_sensor;
        (function(r){
	  db.all("SELECT Num_registro, Valor, Fecha, Hora FROM Medidas WHERE (Id_sensor='"+r+"') AND (FECHA='"+factual+"') ORDER BY Num_registro" , function ( err2,rows) {
            if(err) {
              console.log('exec error: ' + err2);
            }else {
              //console.log(rows);
              socket_selector(socket,rows,r,'Load');
            }
          })
        })(r);
      }
    }
  });
 db.close();

 //Actualizacion de datos en la pagina Web
 setInterval(function(){
 var db= new sqlite3.Database('database.sqlite3',sqlite3.OPEN_READONLY);
  db.all("SELECT Num_registro, Id_sensor, Valor, Fecha, Hora FROM Medidas WHERE FECHA='"+factual+"' AND (Num_registro>'" + lastRead + "') ORDER BY Num_registro" , function ( err2,rows) {
    if(err2) {
      console.log('exec error: ' + err2);
    }else {
     //console.log(rows);
     socket_selector(socket,rows,0,'Update')
    }
  });
  db.close();
 },timerWeb);
}

//Funcion para cargar las graficas del historico de medidas
function infoHist(socket) {
 var db = new sqlite3.Database('database.sqlite3',sqlite3.OPEN_READONLY);
 db.all("SELECT Id_sensor FROM Sensores ORDER BY Id_sensor", function (err,refs) {
    if(err){
       console.log('exec error: ' + err);
    }else{ //cargamos los sensores
      for(var i=0, l1=refs.length; i<l1;i++){
        var r=refs[i].Id_sensor;
        (function(r){
          db.all("SELECT Num_registro, Valor, Fecha, Hora FROM Medidas WHERE Num_registro IN( SELECT min(Num_registro)FROM Medidas WHERE Id_sensor='"+r+"'GROUP BY FECHA)ORDER BY Num_registro" , function ( err2,rows) {
            if(err) {
              console.log('exec error: ' + err2);
            }else {
             //console.log(rows);
              socket_selector(socket,rows,r,'Load');
            }
          })
        })(r);
      }
    }
  });
 db.close();
}


// Funcion para enviar datos del array (rows) a los sockets en funcion
// de la referencia (r) y aplicar la funcion (Load/Update). Ademas actualiza el
// el ultimoregistro leido.

function socket_selector(socket,rows,r,func) {
  var datos=[];
  if (typeof(rows) === "undefined") {var l2=0;}
  else {var l2=rows.length;}

  if(func=='Load' || func=="Load2"){
   //Actualizo el ultimo registro leido.
   if (l2>0){//Compruebo si hay medidas para ese sensor, si no lo inicializo
    if(lastRead <rows[(l2-1)].Num_registro)
      {lastRead=rows[(l2-1)].Num_registro;}
   }else{
    socket.emit(T_sensors[0][((r%10)-1)]+func,T_sensors[0][((r%10)-1)]+(parseInt(r/10)),[]);
   }//Actualizo el ultimo registro leido
 
  }else if(func=='Update'){
    if(l2>0){
     lastRead=rows[l2-1].Num_registro;
    }
  }else{console.log("Funcion no contemplada") }
 
  for(var j=0;j<l2;j++){
    if(func=='Update')
      {r=rows[j].Id_sensor;}
    var tipo=r%10;
    switch(tipo){
      case 1: //Temperatura
        var temp=parseFloat(rows[j].Valor)/100;
        var date=new Date(rows[j].Fecha+" "+rows[j].Hora).getTime();
        datos.push([date,temp]);
      break;
      case 2: //Presencia
        var pres=rows[j].Valor;
        var date=new Date(rows[j].Fecha+" "+rows[j].Hora).getTime();
        datos.push([date,pres]);
      break;
      case 3: //Luminosidad
        var lum=rows[j].Valor;
        var date=new Date(rows[j].Fecha+" "+rows[j].Hora).getTime();
        datos.push([date,lum]);
      break;
      case 4: //Bateria
        var bat=parseFloat(rows[j].Valor)/1000;
        var date=new Date(rows[j].Fecha+" "+rows[j].Hora).getTime();
        datos.push([date,bat]);
      break;
      case 5: //Consumo
        var cons=parseFloat(rows[j].Valor);
        var date=new Date(rows[j].Fecha+" "+rows[j].Hora).getTime();
        datos.push([date,cons]);
      break;
      case 6: //Presion
        var atm=parseFloat(rows[j].Valor)/10;
        var date=new Date(rows[j].Fecha+" "+rows[j].Hora).getTime();
        datos.push([date,atm]);
      break;
      case 7: //Humedad
        var hum=rows[j].Valor;
        var date=new Date(rows[j].Fecha+" "+rows[j].Hora).getTime();
        datos.push([date,hum]);
      break;
      case 8: //TCPU
	var tcpu=rows[j].Valor/100;
        var date=new Date(rows[j].Fecha+" "+rows[j].Hora).getTime();
        datos.push([date,tcpu]);
      break;
      default: console.log('error referencia');
    }
  if ( func=='Update' || j==(l2-1)){
    socket.emit(T_sensors[0][tipo-1]+func,T_sensors[0][(tipo-1)]+(parseInt(r/10)),datos);
    datos=[];
    }
  }
}

// Funcion para cargar la tabla de sensores

function sensores(socket) {
  var db= new sqlite3.Database('database.sqlite3',sqlite3.OPEN_READONLY);
  var idA=0; //Id del siguiente leido   
  var tipos=""; //cadena con los tipos de sensores del nodo
  var loc=0;
  var id_red=0;
  var id=0;
  var bat=[];
  var datos=[];
  var estado=0;	
  db.each("SELECT Id_nodo,Id_sensor,Localizacion,Id_red,Estado FROM Sensores ORDER BY Id_sensor ASC",function(err,referencias){
    if(err){
       console.log('exec error: ' + err);
    }else{//cargamos los sensores
       var id=referencias.Id_nodo;
       if( idA!=id){ //Nuevo nodo
       datos.push([idA,tipos,loc,null,id_red,estado]);
       idA=id;//Actualizamos el idAnterior
       tipos="";
   }
      loc =referencias.Localizacion;
      id_red=referencias.Id_red;
      estado=referencias.Estado;
      var r=(referencias.Id_sensor)%10;
      tipos=tipos+T_sensors[1][(r-1)]+", ";
    } 
  },function(error,nrows){
    datos.push([idA,tipos,loc,null,id_red,estado]);
    for(j=0,l2=datos.length;j<l2;j++){
     var id_sensor=(datos[j][0])*10+4;
    (function(id_sensor,j){
     db.all("SELECT Valor FROM Medidas WHERE Id_sensor='"+id_sensor+"' ORDER BY Fecha, Hora LIMIT 1",function (err2,rows) {
      if(err2) {
        console.log('exec error: ' + err2);
      }else {
        if(rows.length){bat.push(rows[0].Valor/1000);}
	else{bat.push(0);}
	if(j==l2-1){socket.emit('SLoad',datos,bat)}
       }
    });
  })(id_sensor,j);
   }
  });
 db.close();
}
