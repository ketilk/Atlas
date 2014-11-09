import logging
import socket
import pickle
import time
import threading
import topic
import ConfigParser

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

class TopicHandler(object):
  def __init__(name, key):
    self.name = name
    self.key = key
    self.topic = None
    self.event = threading.Event()
    self.event.clear()
    
  def update_topic(self, topic):
    if self.name == topic.name and self.key == topic.key:
      self.topic = topic
      self.event.set()
  
  def get_topic(self, timeout=None):
    if self.event.wait(timeout):
      return self.topic
    else:
      return None

class Atlas(object):
  
  def __init__(self):
    self.logger = logging.getLogger(__name__)
    self.participants = []
    self.lock = threading.Lock()
    self.heartbeat = None
    self.event = threading.Event()
    self.event.clear()
    self.topic = None
    self.topic_handlers = []
    
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
    except:
      self.logger.exception("Listen exception.")
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
    except:
      self.logger.exception("Heartbeat exception.")
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
      self.topic = message
      self.event.set()
      for handler in self.topic_handlers:
        handler.update_topic(self.topic)
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

  def get_topic(self, timeout=None):
    if self.event.wait(timeout):
      self.event.clear()
      return self.topic
    else:
      return None

  def get_subscriber(self, name, key):
    self.logger.info('Creating subscriber:' + name + ', ' + key)
    handler = TopicHandler(name, key)
    self.topic_handlers.append(handler)
    return Subscriber(th)

  def get_publisher(self, name, key):
    self.logger.info('Creating publisher: ' + name + ', ' + key)
    return Publisher(name, key, self._broadcast)

class AtlasDaemon(Daemon):

  def run(self):
    self.logger = logging.getLogger(__name__)
    self.atlas = Atlas()
    self.configuration = ConfigParser.ConfigParser()
    try:
      self.configuration.read('/etc/atlas.cfg')
    except:
      self.logger.warning('Error reading Atlas configuration file.')
    try:
      if not self._init():
        return
    except:
      self.logger.exception("Exception in daemon init.")
      return
    while True:
      try:
        self._loop()
      except:
        self.logger.exception("Caught exception in main thread.")
        break
  
  def get_publisher(self, name, key):
    return self.atlas.get_publisher(name, key)
  
  def get_subscriber(self, name, key):
    return self.atlas.get_subscriber(name, key)