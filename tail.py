#!/usr/bin/env python

from atlas import Atlas
import logging
import time

logging.basicConfig(filename="tail.log",
  filemode='a',
  format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
  datefmt='%H:%M:%S',
  level=logging.DEBUG)
logger = logging.getLogger
    
atlas = Atlas()
time.sleep(10)
print len(atlas.available_topics)
"""for subscriber in atlas.get_subscribers():
  print subscriber.topic + "\n"""
