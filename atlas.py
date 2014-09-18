import logging
import socket
import pickle
import time
import threading
import topic

from subscriber import Subscriber
from publisher import Publisher
from daemon import Daemon

PORT_RANGE = range(20000, 20010)

class AtlasError(Exception):
  
  def __init__(self, text):
    Exception.__init__(self, text)

class Heartbeat(topic.Topic):
  
  def __init__(self, key):
    topic.Topic.__init__(self, "heartbeat", key, 1)

class Atlas(object):
  
  def __init__(self):
    self.logger = logging.getLogger(__name__)
    self.participants = []
    self.topic_handlers = []
    self.lock = threading.Lock()
    self.heartbeat = None
    
    thread = threading.Thread(target=self._listen)
    thread.setDaemon(True)
    thread.start()

    thread = threading.Thread(target=self._heartbeat)
    thread.setDaemon(True)
    thread.start()
    
    self.logger.debug("         === Atlas instantiated ===")
  
  def _listen(self):
    _socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    bound = False
    
    for port in PORT_RANGE:
      try:
        _socket.bind(('', port))
      except socket.error:
        self.logger.debug("Error opening socket on " + str(port))
        continue
      else:
        self.logger.info("Listener up on " + str(port))
        self.heartbeat = Heartbeat(_socket.getsockname())
        bound = True
        break
        
    if not bound:
      raise socket.error("No sockets available to Atlas.")
    
    try:
      while True:
        self.logger.debug("Listening...")
        data, sender = _socket.recvfrom(4096)
        if data:
          self.logger.debug("Received data.")
          self._handle_message(sender, pickle.loads(data))
        else:
          self.logger.debug("Received empty data block.")
    finally:
      _socket.close()

  def _heartbeat(self):
    _socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    try:
      while True:
        if self.heartbeat:
          self.heartbeat.data = 1
          for port in PORT_RANGE:
            _socket.sendto(pickle.dumps(self.heartbeat), ('', port))
        time.sleep(1)
    finally:
      _socket.close()

  def _handle_message(self, sender, message):
    if isinstance(message, Heartbeat):
      self.logger.debug("Handling heartbeat topic from: " + str(message.key))
      self.lock.acquire()
      if message.key not in self.participants:
        self.participants.append(message.key)
      self.lock.release()
    elif isinstance(message, topic.Topic):
      self.logger.debug("Handling a topic.")
      for handler in self.topic_handlers:
        handler(message)
    else:
      self.logger.info("Message handler called on unknown object.")

  def _broadcast(self, message):
    self.logger.debug("Broadcasting...")
    _socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    self.lock.acquire()
    for addr in self.participants:
      _socket.sendto(pickle.dumps(message), addr)
    self.lock.release()
    _socket.close()

  def register_topic_handler(self, handler):
    self.topic_handlers.append(handler)
    self.logger.debug("Topic handler registered.")

  def get_subscriber(self, topic):
    self.logger.info('Creating subscriber with topic ' + str(topic))
    return Subscriber(topic, self)

  def get_publisher(self, topic):
    self.logger.info('Creating publisher with topic: ' + str(topic))
    return Publisher(topic, self)

class AtlasDaemon(Daemon):

  def run(self):
    self.atlas = Atlas()
    self._init()
    while True:
      try:
        self._loop()
      except:
        self.logger.exception("Caught exception in Atlas daemon thread.")
  
  def _loop(self):
    pass
  
  def get_publisher(self, topic):
    return self.atlas.get_publisher(topic)
  
  def get_subscriber(self, topic):
    return self.atlas.get_subscriber(topic)