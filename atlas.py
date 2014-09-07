import logging
import socket
import pickle
import time
import threading

from listener import Listener
from talker import Talker
from communication import Discover
from communication import DiscoverReply
from communication import InsertTopic
from communication import RegisterPublisher
from subscriber import Subscriber
from publisher import Publisher
from daemon import Daemon

PORT_RANGE = range(20000, 20010)

class AtlasError(Exception):
  pass

class Atlas(object):
  def __init__(self):
    self.logger = logging.getLogger(__name__)
    
    for port in PORT_RANGE:
      try:
        self.listener = Listener(port)
      except socket.error, e:
        self.logger.info('Error opening listener on ' + str(port))
        self.error = e
        self.listener = None
      else:
        self.logger.info('Listener up on ' + str(self.listener.address) + '.')
        self.listen_thread = threading.Thread(target=self._listen)
        self.listen_thread.setDaemon(True)
        self.listen_thread.start()
        break
    
    if not self.listener:
      self.logger.warning('Failed to create listener.')
    
    self.participants = []
    self.participants.append(Talker(self.listener.address))
    self.discover_interval = 5
    self.discover_time = 0
    
    self.subscribers = []
    self.available_topics = []
    
    self.discover_thread = threading.Thread(target=self._discover_participants)
    self.discover_thread.setDaemon(True)
    self.discover_thread.start()
    self.logger.debug("Atlas instantiated.")
    
  def _listen(self):
    self.logger.debug("Going into listener method.")
    while True:
      message = self.listener.listen()
      if message:
        self.logger.debug('Handling message: ' + str(message))
        if isinstance(message, Discover):
          self.logger.debug('Sending discover reply to ' + str(self.listener.sender))
          self.listener.reply(DiscoverReply(self.available_topics))
        elif isinstance(message, RegisterPublisher):
          if message.topic not in self.available_topics:
            self.available_topics.add(message.topic)
        elif isinstance(message, InsertTopic):
          [message.topic 
            if _topic == message.topic else _topic 
            for _topic in self.available_topics]
          for subscriber in self.subscribers:
            if subscriber.topic == message.topic:
              subscriber.set_topic(message.topic)
    self.logger.debug("Leaving listener method.")

  def _discover_participants(self):
    self.logger.debug('Starting discover thread.')
    while True:
      if self.discover_time + self.discover_interval < time.time():
        self.discover_time = time.time()
        self.logger.debug('Looking for participants')
        for port in PORT_RANGE:
          talker = Talker(('', port))
          self.logger.debug('Looking for participant at: ' + str(talker.recipient))
          talker.talk(Discover())
          try:
            reply = talker.listen()
          except TalkerTimeout:
            continue
          else:
            if isinstance(reply, DiscoverReply):
              self.logger.debug('Received discover reply from: ' + str(talker.recipient))
              if talker not in self.participants:
                self.participants.append(talker)
              for available_topic in reply.available_topics:
                if available_topic not in self.available_topics:
                  self.available_topics.append(available_topic)
              self.logger.debug('Found participant at: ' + str(talker.recipient))
      else:
        time.sleep(0.1)
    self.logger.debug("Leaving discover method.")
  
  def get_subscriber(self, topic):
    subscriber = None
    for _topic in self.available_topics:
      if topic == _topic:
        self.logger.info('Creating subscriber with topic ' + str(_topic))
        subscriber = Subscriber(_topic)
    if subscriber:
      self.subscribers.append(subscriber)
      return subscriber
    else:
      self.logger.info(str(topic) + ' does not exist.')
      raise AtlasError()
  
  def get_publisher(self, topic):
    self.logger.info('Creating publisher with topic ' + str(topic))
    self.available_topics.append(topic)
    return Publisher(topic, self)
  
  def broadcast_topic(self, topic):
    for participant in self.participants:
      participant.talk(InsertTopic(topic))
  
class AtlasDaemon(Daemon):
  
  def _init(self):
    self.atlas = Atlas()
  
  def run(self):
      while True:
        try:
          self.logger.debug("looping.") 
          self._loop()
        except:
          self.logger.exception("Caught exception in Atlas daemon thread.")
  
  def _loop(self):
    pass
  
  def get_publisher(self, topic):
    return self.atlas.get_publisher(topic)
  
  def get_subscriber(self, topic):
    return self.atlas.get_subscriber(topic)