class Publisher(object):
  def __init__(self, topic, broadcast_topic):
    self._broadcast_topic = broadcast_topic
  
  def publish(self, topic):
    self._broadcast_topic(topic)

      