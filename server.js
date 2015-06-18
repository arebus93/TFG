/** Autor: Adrián Arévalo Aguirre**/ 
var port = 8000;
var app = require('http').createServer(handler).listen(port),
  io = require('socket.io').listen(app),
  fs = require('fs'),
  url = require('url'),
  sqlite3=require('sqlite3').verbose();

var connectCounter = 0;
var timerWeb =30000;//Tiempo de refresco en ms(30s).
var lastRead=0; //Ultimo Num_registro leido de Medidas.
var T_sensors=[['T','P','L','B','C','A','H'],['Temp','Pres','Lum','Bat','Cons','Atm','Hum'],['Temperatura','Presencia','Luminosidad','Bateria','Consumo','Presion','Humedad']]; 

//Si todo va bien al abrir el navegador, cargaremos el html adecuado.
function handler(req, res) {
 path = url.parse(req.url).pathname;
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
    case '/sensors': //Carga la pagina de sensores
      fs.readFile(__dirname+'/nodes.html', function(err, data) {
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
 
 //Eliminamos un sensor
 socket.on('SDelete', function (id_nodo, flag){
  //Lo escribimos en el fichero exchange.txt
  var linea="DELETE,"+id_nodo+","+flag+",\n"  
  fs.appendFile('exchange.txt',linea,function(err){
   if(err){console.log('exec error: ' + err);}
   });
 });

  //Reseteamos el punto de acceso AP
 socket.on('ResetAP', function(){
  //Lo escribimos en el fichero exchange.txt
  var linea="RESET,AP,\n"  
  fs.appendFile('exchange.txt',linea,function(err){
   if(err){console.log('exec error: ' + err);}
   });
 });

 //Resetear un dispositivo final ED
 socket.on('SReset', function (id_red){
  //Lo escribimos en el fichero exchange.txt
  var linea="RESET,"+id_red+",\n"  
  fs.appendFile('exchange.txt',linea,function(err){
   if(err){console.log('exec error: ' + err);}
   });
 });

 socket.on('STimer', function (id_red,TSleep,TWake){
  //Lo escribimos en el fichero exchange.txt
  var linea="SET,"+id_red+","+TSleep+","+TWake+",\n"  
  fs.appendFile('exchange.txt',linea,function(err){
   if(err){console.log('exec error: ' + err);}
   });
 });
 //Eliminamos la conexion
 socket.on('disconnect', function() {
  connectCounter--;
  console.log("NUMBER OF CONNECTIONS--: "+connectCounter);
 });
 // Visualizacion de los datos del sistema.
 if (typeof path != 'undefined'){
    switch(path){
    case '/': //Cargamos y actualizamos las graficas.
   info(socket);
   break;
  case '/sensors': //Cargamos y actualizamos los sensores.
   sensores(socket);
   break;
  }
 }
});

// Funcion para cargar las graficas de medidas con los ultimos valores
//Cada timerWeb milisegundos mandaremos a la gráfica un nuevo valor.
function info(socket) {
 var db = new sqlite3.Database('database.sqlite3',sqlite3.OPEN_READONLY);
 db.all("SELECT Id_sensor FROM Sensores ORDER BY Id_sensor", function (err,refs) {
    if(err){
       console.log('exec error: ' + err);
    }else{ //cargamos los sensores
      for(var i=0, l1=refs.length; i<l1;i++){
        var r=refs[i].Id_sensor;
        (function(r){
            db.all("SELECT Num_registro, Valor, Fecha, Hora FROM Medidas WHERE Id_sensor='" + r + "'ORDER BY Num_registro" , function ( err2,rows) {
            if(err) {
              console.log('exec error: ' + err2);
            }else {
              //console.log(rows);
              //console.log(r);
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
  db.all("SELECT Num_registro, Id_sensor, Valor, Fecha, Hora FROM Medidas WHERE Num_registro>'" + lastRead + "'" , function ( err2,rows) {
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

// Funcion para enviar datos del array (rows) a los sockets en funcion
// de la referencia (r) y aplicar la funcion (Load/Update). Ademas actualiza el
// el ultimoregistro leido.

function socket_selector(socket,rows,r,func) {
  var datos=[];
  var l2=rows.length;
   //Actualizo el ultimo registro leido.
  if (l2>0){//Compruebo si hay medidas para ese sensor, si no lo inicializo
    if(lastRead <rows[(l2-1)].Num_registro)
      {lastRead=rows[(l2-1)].Num_registro;}
  }else{
    if(func=='Load')
     {socket.emit(T_sensors[0][((r%10)-1)]+func,T_sensors[0][((r%10)-1)]+(parseInt(r/10)),[])};
  }
  for(var j=0;j<l2;j++){
    if(func=='Update')
      {r=rows[j].Id_sensor;}
    var tipo=r%10;
    switch(tipo){
      case 1: //Temperatura
        var temp=parseFloat(rows[j].Valor)/10;
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
      case 5: //Consumo
        var cons=parseFloat(rows[j].Valor)/10;
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
  var tipos=""; //cadena con los tipos de sensores del nodo
  var idS=0; //Id del siguiente leido
  var bat=5; //Bateria valor por defecto
 
  db.all("SELECT Id_nodo,Id_sensor, Localizacion,Id_red FROM Sensores ORDER BY Id_sensor",function (err,referencias){
    if(err){
       console.log('exec error: ' + err);
    }else{//cargamos los sensores
    	refs=referencias;
    	//console.log(refs);
      for(var i=0, l1=refs.length; i<l1;i++){
       var id=refs[i].Id_nodo;
	     if(i==l1-1){idS=0;}
	     else{idS=refs[i+1].Id_nodo;}
        r=(refs[i].Id_sensor)%10;
         (function(r){
           if (r==4){
            db.all("SELECT TOP 1 Valor FROM Medidas WHERE Id_sensor='"+r+"' ORDER BY Fecha, Hora",function (err2,rows) {
              if(err2) {
              console.log('exec error: ' + err2);
              }else {
               bat=rows.Valor;
              }
            });
          }
          else {tipos=tipos+T_sensors[1][(r-1)]+", ";}
         })(r);
         if( idS!=id){ //Hemos terminado el nodo
	  loc=refs[i].Localizacion;
	  id_red=refs[i].Id_red;
          socket.emit('SLoad',[id,tipos,loc,bat,id_red]);
          tipos="";
          bat=5;
         }
	}
      }
  });
  db.close();
}

