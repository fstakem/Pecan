#  .-------------------------------------------------------------------------.
#  |                                                                         |
#  |                          T R A N S M I T T E R                          |
#  |                                                                         |
#  '-------------------------------------------------------------------------'

#  By: Fred Stakem 
#  Date: 8.11.12

# Libraries
import time

# Classes
from TransmitterThread import TransmitterThread

class Transmitter(object):
    """This is a class that transmits mocap state information."""
    
    # Class constants
    
    # -----------------------------------------------------------------------
    #       Class Functions
    # -----------------------------------------------------------------------
    # None
    
    
    # -----------------------------------------------------------------------
    #       Instance Functions
    # -----------------------------------------------------------------------
    def __init__(self):
        self.client = None
        self.source = None
        self.addresses = None
        self.tx_thread = None
        self.start_time = 0
        
    def start(self):
        self.start_time = time.time()
        self.tx_thread = TransmitterThread(self.client, self.source, self.addresses, self.start_time)
        self.tx_thread.start()
    
    def play(self):
        pass
        
    def pause(self):
        pass
    
    
    
    
    