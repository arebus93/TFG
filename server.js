/** Autor: Adrián Arévalo Aguirre**/

var port = 8000;
var app = require('http').createServer(handler).listen(port),
  io = require('socket.io').listen(app),
  fs = require('fs'),
  url = require('url'),
  sqlite3=require('sqlite3').verbose();

var db= new sqlite3.Database('database.sqlite3');
var connectCounter = 0;
var Tsensores=['T','P','L','B','C','A','H'];
var r=0; //Referencia de sensor
var lastRead=0; //Ultimo Num_registro leido de Medidas

//Si todo va bien al abrir el navegador, cargaremos el archivo index.html
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


// Funcion de precarga de los datos almacenados
db.all('SELECT Referencia FROM Sensores ORDER BY Referencia ASC', function (err,refs) {
    if(err){
       console.log('exec error: ' + err);
    }else{ //cargamos los sensores
      for(var i=0, l=refs.length; i<l;i++){
        var r=refs[i].Referencia;
        (function(r){
            db.all("SELECT Valor, Fecha, Hora FROM Medidas WHERE Referencia='" + r + "'" , function ( err2,rows) {
            if(err) {
              console.log('exec error: ' + err2);
            }else {
              console.log(rows);
              console.log(r);
              var datos=[];
              switch(r%10){

                case 1: //Temperatura
                  for(var j=0;j<rows.length;j++){
                    var temp=parseFloat(rows[j].Valor)/10;
                    var date=new Date(rows[j].Fecha+" "+rows[j].Hora).getTime();
                    datos.push([date,temp]);
                  }
                 break;

                case 2: //Presencia
                  for(var j=0;j<rows.length;j++){
                    var pres=rows[j].Valor;
                    var date=new Date(rows[j].Fecha+" "+rows[j].Hora).getTime();
                    datos.push([date,pres]);
                  }
                break;

                case 3: //Luminosidad
                  for(var j=0;j<rows.length;j++){
                    var lum=rows[j].Valor;
                    var date=new Date(rows[j].Fecha+" "+rows[j].Hora).getTime();
                    datos.push([date,lum]);
                  }
                break;

                case 4: //Bateria
                break;
              
                case 5: //Consumo
                  for(var j=0;j<rows.length;j++){
                    var cons=parseFloat(rows[j].Valor)/10;
                    var date=new Date(rows[j].Fecha+" "+rows[j].Hora).getTime();
                    datos.push([date,cons]);
                  }
                break;

                case 6: //Presion
                  for(var j=0;j<rows.length;j++){
                  var pres=parseFloat(rows[j].Valor)/10;
                  var date=new Date(rows[j].Fecha+" "+rows[j].Hora).getTime();
                  datos.push([date,pres]);
                  }
                break;

                case 7: //Humedad
                  for(var j=0;j<rows.length;j++){
                    var hum=rows[j].Valor;
                    var date=new Date(rows[j].Fecha+" "+rows[j].Hora).getTime();
                    datos.push([date,hum]);
                  }
                break; 

                default: console.log('error referencia');
              }
              tipo=Tsensores[(r%10)-1];
              socket.emit(tipo+'Load',tipo+(parseInt(r/10)), datos);
            }
          })  
        })(r);
      }
    }
  });
});
