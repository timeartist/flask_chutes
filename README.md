flask_chutes
============

Redis/Socket.IO Pipeline Mixin for Flask

###Server


     from flask_chutes import enable_chutes
     from flask import Flask
    
     app = Flask(__name__)
     app.config['REDIS_CONN'] = {'host':'redis-host', 'db':0}
     enable_chutes(app)
    
###Client


    <!DOCTYPE html>
    <html>
      <head>
        <script type="text/javascript" src="http://code.jquery.com/jquery-1.4.2.min.js"></script>
        <script type="text/javascript">
           var ws = new WebSocket("ws://localhost:8000/chutes");
           ws.onopen = function() {
               //ws.send("{\"channel\": \"test\"}");
               ws.send(JSON.stringify({"channel":"MY_CHANNEL"}));
           };
           ws.onmessage = function(e) {
                $('#messages').append('<br>Received :' + JSON.parse(e.data)['data']);
           }
           ws.onclose = function(evt) {
               alert("socket closed");
           };
        </script>
      </head>
      <body>
        <div id="messages">
        </div>
      </body>
    </html>
    
    
### A-Sync Worker

     from flask_chutes import Chute
     chute = Chute('MY_CHANNEL', **{'host':'redis-host', 'db':0})
     chute.send({'my':'data'})

#### or

     from flask_chutes import send_response_to_chute
     send_response_to_chute('MY_CHANNEL', {'my':'data'}, **{'host':'redis-host', 'db':0, 'timeout':90})


### Running the Server

     gunicorn -k flask_sockets.worker example:app

Adapted from https://github.com/kennethreitz/flask-sockets.

Note, this is a one to one style communication - it's not a pub/sub model.  Each client will likely need their own uniqued channel name.  I'm looking to add the pub/sub version in, but I need to figure out a better way to handle socket closures.

    
