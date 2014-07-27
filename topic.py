import time

class TopicDescription(object):
  def __init__(self, name, key):
    self.name = name
    selfe.key = key
    
  def __eq__(self, other):
    if isinstance(other, TopicDescription):
      return (self.name == other.name and
              self.key == other.key
              )
    else:
      return False

class Topic(TopicDescription):
  def __init__(self, name, key, payload):
    Topicescription.__init__(name, key)
    self.name = name
    self.key = key
    self.timestamp = time.time()
    self.payload = payload
      
    def update_payload(self, payload):
      self.payload = payload
      self.time = time.time()