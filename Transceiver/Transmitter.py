#  .-------------------------------------------------------------------------.
#  |                                                                         |
#  |                          T R A N S M I T T E R                          |
#  |                                                                         |
#  '-------------------------------------------------------------------------'

#  By: Fred Stakem 
#  Date: 8.11.12

# Libraries

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
        self.tx_thread = None
        
    def start(self):
        self.tx_thread = TransmitterThread(self.client, self.source)
        self.tx_thread.start()
    
    def play(self):
        pass
        
    def pause(self):
        pass
    
    
    
    
    