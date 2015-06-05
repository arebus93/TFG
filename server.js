/** Autor: Adrián Arévalo Aguirre**/

var port = 8000;
var app = require('http').createServer(handler).listen(port),
  io = require('socket.io').listen(app),
  fs = require('fs'),
  url = require('url'),
  sqlite3=require('sqlite3').verbose();

var db= new sqlite3.Database('database.sqlite3');
var connectCounter = 0;
var timerWeb =30000; //Tiempo de refresco en ms(30s).
var lastRead=0; //Ultimo Num_registro leido de Medidas.
var T_sensors=['T','P','L','B','C','A','H'];

//Si todo va bien al abrir el navegador, cargaremos el html adecuado.
function handler(req, res) {
  var path = url.parse(req.url).pathname;
  switch(path) {

    case '/': //Carga la pagina principal de sensores.
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

    case '/sensors': //Por implementar
     break;  

     default: //No existe el path o no es accesible
      console.log('No existe el path'+path)
      res.writeHead(404);
      return res.end('Error path not found')
  }
}

//Cuando abramos el navegador estableceremos una conexión con socket.io.
//Cada X segundos mandaremos a la gráfica un nuevo valor. 

io.sockets.on('connection', function(socket) {
  var address = socket.handshake.address;

  console.log("New connection from " + address.address + ":" + address.port);
  connectCounter++; 
  console.log("NUMBER OF CONNECTIONS++: "+connectCounter);
 
 socket.on('disconnect', function() {
  connectCounter--;
  console.log("NUMBER OF CONNECTIONS--: "+connectCounter);
 });

// Precarga de los datos almacenados.
db.all("SELECT Referencia FROM Sensores ORDER BY Referencia", function (err,refs) {
    if(err){
       console.log('exec error: ' + err);
    }else{ //cargamos los sensores
      for(var i=0, l1=refs.length; i<l1;i++){
        var r=refs[i].Referencia;
        (function(r){
            db.all("SELECT Num_registro, Valor, Fecha, Hora FROM Medidas WHERE Referencia='" + r + "'ORDER BY Num_registro" , function ( err2,rows) {
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
 var db= new sqlite3.Database('database.sqlite3');
  db.all("SELECT Num_registro, Referencia, Valor, Fecha, Hora FROM Medidas WHERE Num_registro>'" + lastRead + "'" , function ( err2,rows) {
    if(err2) {
      console.log('exec error: ' + err2);
    }else {
     //console.log(rows);
     socket_selector(socket,rows,0,'Update')
    }
  });
  db.close();
 },timerWeb);
});

// Funcion para enviar datos del array (rows) a los sockets en funcion
// de la referencia (r) y aplicar la funcion (Load/Update). Ademas actualiza el
// el ultimo registro leido.

function socket_selector(socket,rows,r,func) {
  var datos=[];
  var l2=rows.length;

   //Actualizo el ultimo registro leido.
  if (l2>0){//Compruebo si hay medidas para ese sensor, si no lo inicializo
    if(lastRead <rows[(l2-1)].Num_registro)
      {lastRead=rows[(l2-1)].Num_registro;}
  }else{
    if(func=='Load')
     {socket.emit(T_sensors[((r%10)-1)]+func,T_sensors[((r%10)-1)]+(parseInt(r/10)),[])};
  }

  for(var j=0;j<l2;j++){
    if(func=='Update')  
      {r=rows[j].Referencia;}
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

      case 4: //Bateria
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
    socket.emit(T_sensors[tipo-1]+func,T_sensors[(tipo-1)]+(parseInt(r/10)), datos);
    datos=[];
    }
  }
}
