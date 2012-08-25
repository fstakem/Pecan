#  .-------------------------------------------------------------------------.
#  |                                                                         |
#  |                             R E C E I V E R                             |
#  |                                                                         |
#  '-------------------------------------------------------------------------'

#  By: Fred Stakem 
#  Date: 8.11.12

# Libraries
import threading
import time

# Classes
from Message import Message

class Receiver(threading.Thread):
    """This is a class that receives mocap state information."""
    
    # Class constants
    
    # -----------------------------------------------------------------------
    #       Class Functions
    # -----------------------------------------------------------------------
    # None
    
    
    # -----------------------------------------------------------------------
    #       Instance Functions
    # -----------------------------------------------------------------------
    def __init__(self, server, sink):
        self.server = server
        self.sink = sink
        self.remote_hosts = []
        self.running = False
        threading.Thread.__init__(self)
        
    def start(self):
        self.running = True
        threading.Thread.start(self)
        
    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            pass
        
    def newMsgRcvd(self, msg):
        self.sink.setNextMessage(msg)
        
        
        
        