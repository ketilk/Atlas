from topic import Topic

class Publisher(object):
  def __init__(self, topic, atlas):
    self.last_topic = topic
    self.atlas = atlas
  
  def publish(self, payload):
    self.last_topic = Topic(self.last_topic, payload)
    self.atlas.broadcast_topic(self.last_topic)