import threading
import pickle
import time

from daemon import Daemon
from listener import Listener
from talker import Talker

PORT_RANGE = range(20000, 20010)

class AtlasError(Exception):
  def __init__(self, message):
    Exception.__init__(self, message)
"""
Atlas is a thread that when running will operate as a bridge for communicating
messages between remote subscribers and publishers. When the thread is stopped
it only allows communication between local subscribers and publishers.
"""
class Atlas(object):
  
  def __init__(self):
    self.listener = None
    for port in PORT_RANGE:
      try:
        self.listener = Listener(port)
      except socket.error:
        self.logger.info('Error opening listener on ' + str(port))
      else:
        self.port = port
        self.logger.info('Listener up on ' + str(self.listener.address) + '.')
        self.listen_thread = threading.Thread(target=self._listen)
        self.listen_thread.setDaemon(True)
        self.listen_thread.start()
        break
    if not self.listener:
      self.logger.warning("No available sockets for Atlas.")
    self.topics = []
    self.others = []
    self.subscribers[]
    self.discover_thread = threading.Thread(target=self._discover)
    self.discover_thread.setDaemon(True)
  
  def _listen(self):
    self.logger.debug("Starting Atlas.")
    while True:
      message = self.listener.listen()
      self.logger.debug('Handling message: ' + str(message))
      if isinstance(message, Discover):
        self.logger.debug('Sending discover reply to ' + str(self.listener.sender))
        self.listener.reply(DiscoverReply(self.topics))
      elif isinstance(message, InsertTopic):
        self._insert_topic(message.topic)
  
  """
  When run this method will look for other remote instances of Atlas and 
  append these to self.others.
  """
  def _discover(self):
    self.logger.debug("Discovering remote instances of Atlas.")
    while True:
      for port in PORT_RANGE:
        if port == self.port:
          continue
        else:
          talker = Talker(('', port))
          self.logger.debug('Looking for participant at: ' + str(talker.recipient))
          talker.talk(Discover())
          reply = talker.listen()
          if isinstance(reply, DiscoverReply):
            self.logger.debug('Received discover reply from: ' + str(talker.recipient))
            if talker not in self.others:
              self.others.append(talker)
            for topic in reply.available_topics:
              if topic not in self.topics:
                self.topics.append(topic)
            self.logger.debug('Found participant at: ' + str(talker.recipient))
    time.sleep(10)

  """
  This method will update the local list of topics, and update all local
  subscribers with the new topic.
  """
  def _insert_topic(self, topic):
  if topic not in self.topics:
    self.topics.append(topic)
  else:
    [topic if _topic == topic else _topic for _topic in self.topics]
  for subscriber in subscribers:
    if subscriber.topic == topic:
      subscriber.set_topic(topic)

  """
  This method will first call _insert_topic to update local objects, then
  broadcast to remote instances of Atlas.
  """
  def broadcast_topic(self, topic):
    self._insert_topic(topic)
    for receiver in others:
      receiver.talk(topic)

  """
  This method will provide the user with a publisher object for the provided 
  topic.
  """
  def get_publisher(self, topic):
    self.logger.info("Creating publisher with topic " + str(topic))
    self.broadcast_topic(topic)
    return Publisher(topic, self)
   
  """
  Returns a subscriber for the given topic, if an entry for the given topic
  exists.
  """ 
  def get_subscriber(self, topic):
    subscriber = None
    for _topic in self.topics:
      if topic == _topic:
        self.logger.info("Creating subscriber with topic " + str(_topic))
        subscriber = Subscriber(_topic)
    if subscriber:
      self.subscribers.append(subscriber)
      return subscriber
    else:
      self.logger.debug(str(topic) + " does not exist.")
      raise AtlasError(str(topic) + " does not exist.")

class AtlasDaemon(Daemon):
  
  def _init(self):
    self.atlas = Atlas()
