#!/usr/bin/python

import time
import atlas

from math import sin
from math import pi
from topic import Topic

class TestDaemon(atlas.AtlasDaemon):
  
  def _init(self):
    self.topic = Topic("temperature", "tester")
    self.subscriber = self.get_subscriber(self.topic)
  
  def _loop(self):
    self.logger.info(self.subscriber.get_topic())

import logging
import sys
import os

file_name = os.path.splitext(os.path.basename(__file__))[0]
  
if __name__ == '__main__':
  logging.basicConfig(filename='/var/log/' + file_name + '.log',
    filemode='a',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO)
  logger = logging.getLogger(__name__)
  daemon = TestDaemon('/var/run/' + file_name + '.pid')
  if len(sys.argv) == 2:
    if 'start' == sys.argv[1]:
      daemon.start()
    elif 'stop' == sys.argv[1]:
      daemon.stop()
    elif 'restart' == sys.argv[1]:
      daemon.restart()
    else:
      print "Unknown command"
      sys.exit(2)
    sys.exit(0)
  else:
    print "usage: %s start|stop|restart" % sys.argv[0]
    sys.exit(2)