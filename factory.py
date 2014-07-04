import logging
import socket
import pickle
import time
from threading import Event
from threading import Thread
from atlas_thread import AtlasThread
from communication import Discover
from communication import DiscoverReply
from communication import InsertTopic
from subscriber import Subscriber
from publisher import Publisher

PORT_RANGE = range(20000, 20010)

def get_socket_in_range():
  socket_ = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
  for port in PORT_RANGE:
    try:
      socket_.bind(('', port))
    except socket.error:
      continue
    else:
      return socket_
  raise socket.error()
  
class Listener(AtlasThread):
  def __init__(self, run_event):
    AtlasThread.__init__(self, run_event)
    self.insert_topic_event = Event()
    self.inserted_topic = None
    try:
      self.socket = get_socket_in_range()
    except socket.error, e:
      self.work_event.clear()
      raise e
    else:
      self.logger.info('Listener instantiated on addr: ' +
        str(self.socket.getsockname())
        )
      self.socket.settimeout(1)
  
  def _do_work(self):
    try:
      message, addr = self.socket.recvfrom(4096)
    except socket.timeout:
      pass
    else:
      self.logger.debug('Handling incoming message to Listener.')
      message = pickle.loads(message)
      if isinstance(message, Discover):
        self.logger.debug('Listener received Discover message from ' + 
          str(addr) + '.'
          )
        self._discover_reply(addr)
      if isinstance(message, InsertTopic):
        self.logger.debug('Listener received InsertTopic message')
        self.inserted_topic = message.topic
        self.logger.debug('Val: ' + str(self.inserted_topic.temp))
        self.insert_topic_event.set()
  
  def _clean_up(self):
    self.logger.info('Cleaning up Listener.')
    self.socket.close()
  
  def _discover_reply(self, addr):
    self.logger.debug('DiscoverListener replying to ' + str(addr) + '.')
    reply = pickle.dumps(DiscoverReply())
    self.socket.sendto(reply, addr)
    
class Discoverer(AtlasThread):
  def __init__(self, run_event):
    AtlasThread.__init__(self, run_event)
    self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    self.socket.settimeout(0.2)
    self.discover_reply_event = Event()
    self.factories = []
    self.logger.info('Discoverer instantiated.')
  
  def _do_work(self):
    for port in PORT_RANGE:
      addr = ('', port)
      self.logger.debug('Sending to: ' + str(addr) + '.')
      self.socket.sendto(pickle.dumps(Discover()), addr)
      try:
        reply, addr = self.socket.recvfrom(4096)
      except socket.timeout:
        pass
      else:
        reply = pickle.loads(reply)
        if isinstance(reply, DiscoverReply):
          self.logger.debug('Discoverer received reply.')
          if addr not in self.factories:
            self.factories.append(addr)          
          self.discover_reply_event.set()
    time.sleep(5)
  
  def broadcast_message(self, message):
    for addr in self.factories:
      self.logger.debug('Sending message to: ' + str(addr) + '.')
      self.socket.sendto(pickle.dumps(InsertTopic(message)), addr)

class Factory(object):
  def __init__(self):
    self.logger = logging.getLogger(__name__)
    self.run_event = Event()
    self.run_event.set()
    self.listener = Listener(self.run_event)
    self.listener.start()
    self.discoverer = Discoverer(self.run_event)
    self.discoverer.start()
    self.subscribers = []
    
    Thread(target=self._event_handler).start()
  
  def release(self):
    self.run_event.clear()
    
  def _event_handler(self):
    while self.run_event.is_set():
      if self.listener.insert_topic_event.wait(1):
        self.listener.insert_topic_event.clear()
        self.logger.debug('Insert topic event occurring.')
        for subscriber in self.subscribers:
          if subscriber.topic == self.listener.inserted_topic:
            self.logger.debug('Setting subscriber topic, ' + 
              str(self.listener.inserted_topic.temp)
              )
            subscriber.set_topic(self.listener.inserted_topic)
  
  def get_subscriber(self, topic):
    subscriber = Subscriber(topic)
    self.subscribers.append(subscriber)
    return subscriber
  
  def get_publisher(self, topic):
    return Publisher(topic, self.discoverer.broadcast_topic)
    