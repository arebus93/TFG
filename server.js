/** Autor: Adrián Arévalo Aguirre**/

var port = 8000;
var app = require('http').createServer(handler).listen(port),
  io = require('socket.io').listen(app),
  fs = require('fs'),
  sqlite3=require('sqlite3').verbose();
  var db= new sqlite3.Database('database.sqlite3');
  var connectCounter = 0;
  var Tsensores=['T','P','L','B','C','A','H'];

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
 db.all('SELECT Referencia FROM Sensores', function (err,refs) {
    if(err){
       console.log('exec error: ' + err);
    }else{ //cargamos los sensores
  for(var i=0, l=refs.length; i<l;i++){
    var r=refs[i].Referencia;
    db.all("SELECT Referencia, Valor, Fecha, Hora FROM Medidas WHERE Referencia='" + r + "'" , function ( err2,rows) {
          if(err) {
            console.log('exec error: ' + err2);
          }else {
            //console.log(rows);
            var datos=[];
            for(var j=0;j<rows.length;j++){
             var ref=rows[j].Referencia;
             switch (ref%10){
                
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
                  var pres=parseFloat(rows[j].Valor)/10;
                  var date=new Date(rows[j].Fecha+" "+rows[j].Hora).getTime();
                  datos.push([date,pres]);
              break;

              case 7: //Humedad
                  var hum=rows[j].Valor;
                  var date=new Date(rows[j].Fecha+" "+rows[j].Hora).getTime();
                  datos.push([date,hum]);
              break; 

              default: console.log('error referencia'+ref%10);
            }
      } 
      tipo=Tsensores[(ref%10)-1];
            socket.emit(tipo+'Load',tipo+(parseInt(ref/10)), datos);
        }
      })  
    }
  }
})
});
