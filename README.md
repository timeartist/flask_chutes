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


    
