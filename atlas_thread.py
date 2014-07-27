import threading
import logging

class AtlasThread(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    self.logger = logging.getLogger(__name__)
    self.run_event = threading.Event()
    self.run_event.set()
  
  def run(self):
    self.logger.debug('Starting Atlas thread.')
    while self.run_event.is_set():
      self._do_work()
    self._clean_up()
  
  def stop(self):
    self.run_event.clear()
  
  def _do_work(self): pass
  
  def _clean_up(self): pass