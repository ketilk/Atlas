import socket
import pickle
import topic

class Publisher(object):
  def __init__(self, topic, atlas):
    self.topic = topic
    self.atlas = atlas
    
  def publish(self, data):
    self.topic.data = data
    self.atlas._broadcast(self.topic)