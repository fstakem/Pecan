#  .-------------------------------------------------------------------------.
#  |                                                                         |
#  |     S Y N C H R O N O U S  T R A N S M I S S I O N  A L G O R I T M     |
#  |                                                                         |
#  '-------------------------------------------------------------------------'

#  By: Fred Stakem 
#  Date: 8.25.12

# Libraries

# Classes
from Transceiver import Message
from TransmissionAlgorithm import TransmissionAlgorithm

class SynchronousTxAlg(TransmissionAlgorithm):
    """This is a class that dictates when mocap state information should be
       transmitted."""
    
    # Class constants
    
    # -----------------------------------------------------------------------
    #       Class Functions
    # -----------------------------------------------------------------------
    # None
    
    
    # -----------------------------------------------------------------------
    #       Instance Functions
    # -----------------------------------------------------------------------
    def __init__(self, data):
        self.data = data
        self.playback_time = 0
        
    def getNextMessage(self, new_time):
        return None
        
        