import enum
import pickle
import random
import string
import zlib

import zmq

import thalesians.tsa.checks as checks
from thalesians.tsa.strings import ToStringHelper 

class Direction(enum.Enum):
    INCOMING = 1
    OUTGOING = 2

class Pype(object):
    def __init__(self, direction, name=None, host=None, port=22184, zipped=False):
        if name is None: name = random.choice(string.ascii_uppercase) + \
                ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3))
        checks.check_string(name, allow_none=False)
        checks.check(lambda: name.isalnum(), 'Pype\'s name is not alphanumeric')
        checks.check(lambda: len(name) > 0, 'Pype\'s name is an empty string')
        
        self._name = name
        self._main_topic = self._name
        self._main_topic_bytes = (self._main_topic + ' ').encode('utf-8')
        self._eof_topic = self._name + '!'
        self._eof_topic_bytes = (self._eof_topic + ' ').encode('utf-8')
        
        self._port = port
        self._context = zmq.Context()
        if direction == Direction.INCOMING:
            if host is None: host = 'localhost'
            self._host = host
            self._socket = self._context.socket(zmq.SUB)
            self._socket.connect('tcp://%s:%d' % (self._host, self._port))
            self._socket.setsockopt_string(zmq.SUBSCRIBE, self._name)
            self._socket.setsockopt_string(zmq.SUBSCRIBE, self._eof_topic)
        elif direction == Direction.OUTGOING:
            if host is None: host = '*'
            self._host = host
            self._socket = self._context.socket(zmq.PUB)
            self._socket.bind('tcp://%s:%d' % (self._host, self._port))
        else:
            raise ValueError('Unexpected direction: %s' % str(direction))
        self._direction = direction
        self._closed = False
        
        self._zipped = zipped
        
        self._to_string_helper_Pype = None
        self._str_Pype = None
        
    def close(self):
        if not self._closed:
            if self._direction == Direction.OUTGOING:
                self._socket.send(self._eof_topic_bytes)
            self._socket.close()
            self._context.term()
            self._closed = True
        
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):  # @UnusedVariable @ReservedAssignment
        self.close()
        
    def send(self, obj):
        if self._closed: raise ValueError('I/O operation on closed pype')
        ba = bytearray(self._main_topic_bytes)
        p = pickle.dumps(obj, protocol=-1)
        if self._zipped: p = zlib.compress(p)
        ba.extend(p)
        return self._socket.send(ba, flags=0)
    
    def receive(self, notify_of_eof=False):
        if self._closed: raise ValueError('I/O operation on closed pype')
        s = self._socket.recv()
        topic, p = s.split(b' ', 1)
        topic = topic.decode("utf-8")
        if topic == self._eof_topic:
            o = None
            eof = True
            self.close()
        else:
            if self._zipped: p = zlib.decompress(p)
            o = pickle.loads(p)
            eof = False
        return (o, eof) if notify_of_eof else o
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._closed: raise StopIteration
        o, eof = self.receive(notify_of_eof=True)
        if eof: raise StopIteration
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
    
    @property
    def closed(self):
        return self._closed
    
    def to_string_helper(self):
        if self._to_string_helper_Pype is None:
            self._to_string_helper_Pype = ToStringHelper(self) \
                    .add('name', self._name) \
                    .add('direction', self._direction) \
                    .add('host', self._host) \
                    .add('port', self._port)
        return self._to_string_helper_Pype
    
    def __str__(self):
        if self._str_Pype is None: self._str_Pype = self.to_string_helper().to_string()
        return self._str_Pype 

    def __repr__(self):
        return str(self)
