var http = require('http');
var url = require('url');
var fs = require('fs');

http.createServer(function (req, res) {
  var q = url.parse(req.url, true);
  
   if(q.pathname=="/"){
    console.log("empty!");
    fs.readFile("./ind.html", function(err, data) {
        if (err) {
          res.writeHead(404, {'Content-Type': 'text/html'});
          return res.end("404 Not Found");
        } 
        res.writeHead(200, {'Content-Type': 'text/html'});
        res.write(data);    
        return res.end();
        });
    }
    else if (q.pathname=="/json"){ 
      res.writeHead(200, {'Content-Type': 'application/json'});
      fs.readFile("./graph.json", function(err, data) {
        res.write(data);    
        return res.end();
      });
    }
    else if (q.pathname=="/miserables.json"){ 
        console.log("not empty");
        res.writeHead(200, {'Content-Type': 'application/json'});

        var options = {
            host: 'fd00::212:7401:1:101',
            // host: 'http://google.com',
            path: '/'
        }
        callback = function(response) {
            var str = '';
          
            //another chunk of data has been received, so append it to `str`
            response.on('data', function (chunk) {
              str += chunk;
            });

            const parseJsonAsync = (jsonString) => {
              return new Promise(resolve => {
                setTimeout(() => {
                  resolve(JSON.parse(jsonString))
                })
              })
            }

            //the whole response has been received, so we just print it out here
            response.on('end', function () {              
              parseJsonAsync(str).then(jsonData => jsonData.forEach(element => {
                console.log(element)
              }))
              res.write(str,function(err) {res.end();});
            });
          }
          
          http.request(options, callback).end();
        //   return res.end();
    }
}).listen(3000);