import socket
import pickle
import topic

class Publisher(object):
  def __init__(self, name, key, publishfn):
    self.name = name
    self.key = key
    self._publish = publishfn
    
  def publish(self, data):
    self._publish(topic.Topic(self.name, self.key, data))