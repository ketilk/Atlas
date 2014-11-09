import threading
import logging

class Subscriber(object):
  def __init__(self, topic_handler):
    self.logger = logging.getLogger(__name__)
    self.topic_handler = topic_handler
  
  def get_data(self, timeout=None):
    topic = self.topic_handler.get_topic(timeout)
    if topic:
      return topic.data
    else:
      return None