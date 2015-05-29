/** Autor: Adrián Arévalo Aguirre**/

var port = 8000;
var app = require('http').createServer(handler).listen(port),
  io = require('socket.io').listen(app),
  fs = require('fs'),
  sqlite3=require('sqlite3').verbose();
  var db= new sqlite3.Database('database.sqlite3');
  var connectCounter = 0;

//Si todo va bien al abrir el navegador, cargaremos el archivo index.html
function handler(req, res) {
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
db.all("SELECT * FROM Medidas", function (err,rows) {
    if(err){
     console.log('exec error: ' + err);
    }else{
      for(i in rows){
        if(((rows[i].Referencia)%10)==1){
          temp=parseFloat(rows[i].Valor)/10;
          date=new Date(rows[i].Fecha+" "+rows[i].Hora).getTime();
          //console.log(temp+"  "+date);
          socket.emit('temperatureUpdate',date,temp);
        }
      }
    }
  });
});
