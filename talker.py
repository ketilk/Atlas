import socket
import pickle

"""
The Talker is associated with a socket. When user sends a message via talk(), 
the reply will be available on listen() within the given timeout.
"""

class TalkerTimeout(Exception):
  pass
  
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
      raise TalkerTimeout()
    else:
      return pickle.loads(message)