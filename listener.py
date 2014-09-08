import socket
import pickle

class Listener(object):
  def __init__(self, port=0):
    self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    self.socket.bind(('', port))
    self.address = self.socket.getsockname()
    self.sender = None
  
  def __del__(self):
    self.socket.close()
  
  def listen(self):
    message, self.sender = self.socket.recvfrom(4096)
    return message
  
  def reply(self, message):
    self.socket.sendto(pickle.dumps(message), self.sender)