import time

class TopicDescription(object):
  def __init__(self, name, key):
    self.name = name
    self.key = key
    
  def __eq__(self, other):
    if isinstance(other, TopicDescription):
      return (self.name == other.name and
              self.key == other.key
              )
    else:
      return False
  
  def __str__(self):
    return self.name + ', ' + str(self.key)

class Topic(TopicDescription):
  def __init__(self, topic, payload):
    TopicDescription.__init__(self, topic.name, topic.key)
    self.timestamp = time.time()
    self.payload = payload
    
  def __str__(self):
    return super(Topic, self).__str__() + ', ' + str(self.payload)
    