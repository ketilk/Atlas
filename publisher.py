class Publisher(object):
  def __init__(self, topic, broadcast_message):
    self._broadcast_message = broadcast_message
  
  def publish(self, topic):
    self._broadcast_topic(topic)

      