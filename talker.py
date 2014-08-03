import socket
import pickle

class Talker(object):
  def __init__(self, recipient):
    self.recipient = recipient
    self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    self.socket.settimeout(0.1)
  
  def __eq__(self, other):
    return self.recipient == other.recipient
    
  def talk(self, message):
    self.socket.sendto(pickle.dumps(message), self.recipient)
  
  def listen(self):
    try:
      message, sender = self.socket.recvfrom(4096)
    except socket.timeout:
      return None
    else:
      return pickle.loads(message)
  
  def has_listener(self):
    for i in range(0,5):
      self.talk('ping')
      reply = self.listen()
      if reply == 'ping':
        return True
    return False