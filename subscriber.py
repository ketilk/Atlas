import threading
import logging

class Subscriber(object):
  def __init__(self, topic, atlas):
    self.logger = logging.getLogger(__name__)
    self._topic = topic
    self._topic_event = threading.Event()
    self._topic_event.clear()
    self._topic_handlers = []
    atlas.register_topic_handler(self._topic_handler)
    
    
  def _topic_handler(self, topic):
    self.logger.debug("Topic handler called...\n" +
                      "      " + str(topic) + " V " + str(self._topic))
    if topic == self._topic:
      self.logger.debug("...with matching topic.")
      self._topic = topic
      self._topic_event.set()
      for topic_handler in self._topic_handlers:
        topic_handler(topic)
  
  def register_topic_handler(self, topic_handler):
    if topic_handler not in self.topic_handlers:
      self.topic_handlers.append(topic_handler)
  
  def get_topic(self):
    self._topic_event.wait()
    self._topic_event.clear()
    return self._topic
  
  def matches(self, topic):
    return self._topic == topic
  
  topic = property(get_topic)