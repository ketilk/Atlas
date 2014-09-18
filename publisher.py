import socket
import pickle
import topic

class Publisher(object):
  def __init__(self, topic, atlas):
    self.atlas = atlas
    
  def publish(self, topic):
    self.atlas._broadcast(topic)