import time

class Topic(object):
  def __init__(self, name, key, payload=None):
    self.name = name
    self.key = key
    self.timestamp = time.time()
    self.payload = payload
    
  def __eq__(self, other):
    if isinstance(other, TopicDescription):
      return (self.name == other.name and
              self.key == other.key
              )
    else:
      return False
      
    def update_payload(self, payload):
      self.payload = payload
      self.time = time.time()