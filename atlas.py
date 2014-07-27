import logging
import socket
import pickle
import time
from atlas_thread import AtlasThread
from listener import Listener
from talker import Talker
from communication import Discover
from communication import DiscoverReply
from communication import InsertTopic
from subscriber import Subscriber
from publisher import Publisher

PORT_RANGE = range(20000, 20010)

class Atlas(AtlasThread):
  def __init__(self):
    self.logger = logging.getLogger(__name__)
    for port in PORT_RANGE:
      try:
        self.listener = Listener(port)
      except port.error:
        pass
      else:
        break
    self.listener.start()
    
    self.participants = []
    self.discover_interval = 5
    self.discover_time = time.time() - self.discover_interval
    
    self.subscribers = []
    self.available_topics = []
    
def _do_work(self):
  message = listener.listen()
  if message:
    self._handle_message(message)
  
  if self.discover_time + self.discover_interval < time.time():
    self._discover_participants()
    self.discover_time = time.time()
    
def _handle_message(self, message):
  if isinstance(message, Discover):
    listener.reply(DiscoverReply(self.available_topics))
  elif isinstance(message, DiscoverReply):
    for available_topic in message.available_topics:
      if available_topic not in self.available_topics:
        available_topics.add(available_topic)
  elif isinstance(message, RegisterPublisher):
    if message.topic not in self.available_topics:
      self.available_topics.add(message.topic)
  elif isinstance(message, InsertTopic):
    for subscriber in self.subscribers:
      if subscriber.topic == InsertTopic.topic:
        subscriber.set_topic(InsertTopic.topic)

def _discover_participants(self):
  for port in PORT_RANGE:
    talker = Talker(('', port))
    talker.talk(Discover())
    reply = talker.listen()
    if isinstance(reply, DiscoverReply):
      self.participants.add(talker)
      for available_topic in reply.available_topics:
        if available_topic not in self.available_topics:
          self.available_topics.add(available_topic)
    
  
  def get_subscriber(self, topic):
    subscriber = Subscriber(topic)
    self.subscribers.append(subscriber)
    return subscriber
  
  def get_publisher(self, topic):
    available_topics.add(topic)
    return Publisher(topic, self)
  
  def broadcast(self, message):
    for participant in self.participants:
      participant.talk(message)
  
  def get_available_topics(self):
    return self.available_topics
    