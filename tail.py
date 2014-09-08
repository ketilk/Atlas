#!/usr/bin/env python

from atlas import Atlas
import logging

logging.basicConfig(filename="tail.log",
  filemode='a',
  format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
  datefmt='%H:%M:%S',
  level=logging.DEBUG)
logger = logging.getLogger
    
atlas = Atlas()
for subscriber in atlas.get_subscribers():
  print subscriber.topic + "\n"
