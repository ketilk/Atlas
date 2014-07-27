import socket
import pickle

class Listener(object):
  def __init__(self, port=0):
    self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    self.socket.bind(('', port))
    self.address = self.socket.getsockname()
    self.socket.settimeout(0.1)
    self.sender = None
  
  def listen(self):
    try:
      message, self.sender = self.socket.recvfrom(4096)
    except socket.timeout:
      return None
    else:
      if message == 'ping':
        self.reply('ping')
      else:
        return pickle.loads(message)
  
  def reply(self, message):
    self.socket.sendto(pickle.dumps(message), self.sender)
    
    
    