class Discover(object):
  pass
    
class DiscoverReply(object):
  def __init__(self, available_topics):
    self.available_topics = available_topics

class InsertTopic(object):
  def __init__(self, topic):
    self.topic = topic
    
class RegisterPublisher(object):
  def __init__(self, topic):
    self.topic = topic

class RegisterPublisherReply(object):
  pass