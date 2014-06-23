from threading import Event

class Subscriber(object):
  def __init__(self, topic):
    self.topic_event = Event()
    self.topic = topic
    
  def set_topic(self, topic):
    self.topic = topic
    self.topic_event.set()