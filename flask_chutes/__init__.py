from flask_sockets import Sockets
from redis import StrictRedis
from json import loads, dumps

def enable_chutes(app):
    connection = app.config['REDIS_CONN']
    r = StrictRedis(**connection)
    sockets = Sockets(app)
    
    @sockets.route('/chutes')
    def _chutes(ws):
            
        i = 0
        redis_key = None
        
        while True:
                   
            ##ws.receive is a blocking call - and we're only really ever going to care if
            ##the client sent us a message on the initial connect as that tells us which
            ##redis queue we're going to be pulling from.
            
            if i == 0:
                msg = ws.receive()
                print msg
                sign_on = loads(msg)
                channel = sign_on['channel']
                redis_key = 'chutes:%s'%channel
                i += 1
                
            resp = r.blpop(redis_key, 30)
            print resp
            
            if ws.closed:
                print 'Websocket Connection Closed by Client'
                break
            
            
            if resp and isinstance(resp[-1], (str, unicode)):
                print 'WS:', channel, '->', resp[-1]
                ws.send(resp[-1])
            else:
                ws.send(dumps({'data':None}))


            

