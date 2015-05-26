//Server Node.js

//Modulos y Puerto
var port = 8000;
var app = require('http').createServer(handler).listen(port);
var io = require('socket.io').listen(app);
var fs = require('fs');
var sqlite3=require('sqlite3').verbose();
var db=sqlite3.Database('database')
var connectCounter = 0;

// Al inicio cargaremos el archivo index.html
function handler(req, res) {
	fs.readFile(__dirname+'/index.html', function(err, data) {
		
    if (err) {//Si hay error, mandaremos un mensaje de error 500
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
  var temp=0;
  
  //Añado una nueva conexion
  console.log("New connection from " + address.address + ":" + address.port);
  connectCounter++; 
  console.log("NUMBER OF CONNECTIONS++: "+connectCounter);
  
  //Elimino la conexion de la lista de sockets
  socket.on('disconnect', function() {
  connectCounter--;  
  console.log("NUMBER OF CONNECTIONS--: "+connectCounter);
  });

  // Funcion de precarga de los datos almacenados
  
  //Para definir hasta donde pintamos las medidas en dias

  db.all("SELECT * FROM Medidas", function (err,rows) {
    if(err){
     console.log('exec error: ' + err);
    }else{
      for(row in rows){
        if((row[1]%10)==1){
          temp=parseFloat(row[2])/100;
          date=new Date (row[3]+row[4]);
          console.log(temp+"  "+date);
          socket.emit('temperatureUpdate',date,temp)
	}
      }
    }
  })
 
// Funcion para medir la temperatura 
  //   setInterval(function(){
  //   var date = new Date().getTime();
        
  //   //Es necesario mandar el tiempo (eje X) y un valor de temperatura (eje Y).
    
  //   var temp = parseFloat(stdout)/1000;
  //   socket.emit('temperatureUpdate', date, temp); 
    
  // });}, 5000);

});

