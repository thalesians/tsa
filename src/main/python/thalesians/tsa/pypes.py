import enum
import pickle
import random
import string
import zlib

import zmq

import thalesians.tsa.checks as checks

class Direction(enum.Enum):
    INCOMING = 1
    OUTGOING = 2

class Pype(object):
    def __init__(self, direction, name=None, host=None, port=22184):
        if name is None: name = random.choice(string.ascii_uppercase) + \
                ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3))
        checks.check(lambda: name.isalnum(), 'Pype\'s name is not alphanumeric')
        self._name = name
        self._name_bytes = (name + ' ').encode('utf-8')
        
        self._port = port
        self._context = zmq.Context()
        if direction == Direction.INCOMING:
            if host is None: host = 'localhost'
            self._host = host
            self._socket = self._context.socket(zmq.SUB)
            self._socket.connect('tcp://%s:%d' % (self._host, self._port))
            self._socket.setsockopt_string(zmq.SUBSCRIBE, self._name)
        elif direction == Direction.OUTGOING:
            if host is None: host = '*'
            self._host = host
            self._socket = self._context.socket(zmq.PUB)
            self._socket.bind('tcp://%s:%d' % (self._host, self._port))
        else:
            raise ValueError('Unexpected direction: %s' % str(direction))
        self._direction = direction
        
    def send(self, obj):
        ba = bytearray(self._name_bytes)
        p = pickle.dumps(obj, protocol=-1)
        z = zlib.compress(p)
        ba.extend(z)
        return self._socket.send(ba, flags=0)
    
    def receive(self):
        s = self._socket.recv()
        _, data = s.split(b' ', 1)
        p = zlib.decompress(data)
        o = pickle.loads(p)
        return o
        
    @property
    def name(self):
        return self._name
    
    @property
    def direction(self):
        return self._direction
    
    @property
    def host(self):
        return self._host
    
    @property
    def port(self):
        return self._port
    
    def __str__(self):
        return 'Pype(name="%s", direction=%s, host="%s", port=%d)' % (self._name, self._direction, self._host, self._port)
    
    def __repr__(self):
        return str(self)
