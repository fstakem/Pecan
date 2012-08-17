#  .-------------------------------------------------------------------------.
#  |                                                                         |
#  |                  T R A N S M I T T E R  T H R E A D                     |
#  |                                                                         |
#  '-------------------------------------------------------------------------'

#  By: Fred Stakem 
#  Date: 8.16.12

# Libraries
import threading

# Classes

class TransmitterThread(threading.Thread):
    """This is a class that thread transmits mocap state information."""
    
    # Class constants
    
    # -----------------------------------------------------------------------
    #       Class Functions
    # -----------------------------------------------------------------------
    # None
    
    
    # -----------------------------------------------------------------------
    #       Instance Functions
    # -----------------------------------------------------------------------
    def __init__(self, client, source):
        self.client = client
        self.source = source
        threading.Thread.__init__(self)
        self.running = True
        
    def run(self):
        while self.running:
            pass

        
