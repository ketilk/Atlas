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
    
class TemperatureTopic(TopicDescription):
  def __init__(self, key):
    TopicDescription.__init__(self, 'Temperature topic', key)
    self.temp = 0