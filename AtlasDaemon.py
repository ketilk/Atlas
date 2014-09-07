import threading

from daemon import Daemon
from listener import Listener

PORT_RANGE = range(20000, 20010)

class Broadcaster(object):
  def __init__(self):
    self.recipients = []
  
  def add_recipient(self, recipient):
    if recipient not in self.recipients:
      self.recipients.append(recipient)
  
  def broadcast(self, message):
    for recipient in self.recipients:
      recipient.talk(message)

class Atlas(threading.Thread):
  
  def __init__(self, listener):
    threading.Thread.__init__(self)
    self.listener = None
    for port in PORT_RANGE:
      try:
        self.listener = Listener(port)
      except socket.error:
        self.logger.info('Error opening listener on ' + str(port))
      else:
        self.logger.info('Listener up on ' + str(self.listener.address) + '.')
        break
    if not self.listener:
      raise Exception("No available sockets."):
    self.topics = []
    self.others = []
  
  def run(self):
    self.run = True
    self.logger.debug("Starting Atlas Listener.")
    while self.run:
      message = self.listener.listen()
      self.logger.debug('Handling message: ' + str(message))
      if isinstance(message, Discover):
        self.logger.debug('Sending discover reply to ' + str(self.listener.sender))
        self.listener.reply(DiscoverReply(self.available_topics))
      elif isinstance(message, InsertTopic):
        self.insert_topic(message.topic)
            
  def insert_topic(self, topic):
    if topic not in self.topics:
      self.topics.append(topic)
    else:
      [topic if _topic == topic else _topic for _topic in self.topics]

class AtlasDaemon(Daemon):
  
  def _init(self):
    self.logger = logging.getLogger(__name__)
    self.state = "ok"
    try:
      self.listen_thread = ListenThread()
    except Exception:
      self.logger.exception("Exception when instantiating Atlas Deamon.")
      self.state = "error"
    self.others = []

  def _loop(self):
    if self.state == "error":
      raise Exception("AtlasDaemon in error state.")
    elif self.state == "ok":