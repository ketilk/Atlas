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
  
class RegisterSubscriber(object):
  def __init__(self, topic_description):
    self.topic_description = topic_description
    
class RegisterSubscriberReply(object):
  def __init__(self, topic):
    self.topic = topic