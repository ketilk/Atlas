import time
from numbers import Number
import logging

class Topic(object):
  
  def __init__(self, name, key, data=None):
    self.name = name
    self.key = key
    self.time = time.time()
    self.data = data
    
  def __eq__(self, other):
    if isinstance(other, Topic):
      return (self.name == other.name and
              self.key == other.key
              )
    else:
      return False
  
  def __str__(self):
    return str(self.time) + ', ' + self.name + ', ' + self.key + ', ' + str(self._data)
