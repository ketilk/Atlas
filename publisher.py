class Publisher(object):
  def __init__(self, atlas):
    self.atlas = atlas
  
  def publish(self, topic):
    self.atlas.broadcast(InsertTopic(topic))