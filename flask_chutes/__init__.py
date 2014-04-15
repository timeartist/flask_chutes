from flask_sockets import Sockets
from flask import Flask
from redis import StrictRedis
from json import loads, dumps
from multiprocessing import Process
from gevent import sleep, Greenlet
from geventwebsocket.exceptions import WebSocketError

processes = {}

def enable_chutes(app):
    '''
    Factory method to add the chutes socket endpoint to your existing Flask app
    
    Input:
        app - Flask App Object to be extended
        
    Returns:
        None
    '''
    
    assert isinstance(app, Flask)
    
    connection = app.config['REDIS_CONN']
    r = StrictRedis(**connection)
    sockets = Sockets(app)
    
    @sockets.route('/chutes')
    def _chutes(ws):
        try:
            
            i = 0
            redis_key = None
            channel = None
            
            while True:
                
                if i == 0:
                    msg = ws.receive()
                    print msg
                    sign_on = loads(msg)
                    channel = sign_on['channel']
                    if channel not in processes:
                        processes[channel] = []

                    redis_key = 'c:%s'%channel
                    i += 1
                    
                    ps = r.pubsub()
                    ps.subscribe(redis_key)
                    process = Greenlet(socket_sentinel_publish, *(ws, ps))
                    process.start()
                    processes[channel].append(process)
                    
                    process = Greenlet(socket_sentinel_client_listener, *(ws, r, redis_key))
                    process.start()
                    processes[channel].append(process)
                    
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
                    
        except WebSocketError, e:
            _processes = processes[channel]            
            for process in _processes:
                process.kill()

class Chute(object):
    def __init__(self, channel, **kwargs):
        self.r = StrictRedis(**kwargs)
        self.channel = channel
        self._r_key = 'c:%s'%channel
        
    def send(self, data, timeout=90):
        self.r.lpush(self._r_key, data)
        self.r.expire(self._r_key, timeout)
        
    def publish(self, data):
        self.r.publish(self._r_key, data)
    
    def listen(self):
        ps = self.r.pubsub()
        ps.subscribe(channel)
        
        for item in ps.listen():
            yield item
    
    

def socket_sentinel_publish(ws, ps):
    for msg in ps.listen():
        print msg
        if msg:
            ws.send(msg)

def socket_sentinel_client_listener(ws, r, channel):
    while True:
        msg = ws.receive()
        print msg
        r.publish(channel, msg)