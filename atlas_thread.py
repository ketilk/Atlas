import threading
import logging

class AtlasThread(threading.Thread):
  def __init__(self, run_event):
    threading.Thread.__init__(self)
    self.logger = logging.getLogger(__name__)
    self.run_event = run_event
    self.work_event = threading.Event()
    self.work_event.set()
  
  def run(self):
    self.logger.debug('Starting Atlas thread.')
    while self.run_event.is_set() and self.work_event.is_set():
      self._do_work()
    self._clean_up()
  
  def _do_work(self): pass
  
  def _clean_up(self): pass