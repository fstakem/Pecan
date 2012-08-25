#  .-------------------------------------------------------------------------.
#  |                                                                         |
#  |                               S O U R C E                               |
#  |                                                                         |
#  '-------------------------------------------------------------------------'

#  By: Fred Stakem 
#  Date: 8.16.12

# Libraries

# Classes
from Message import Message

class Source(object):
    """This is a class that controls the flow of mocap state information."""
    
    # Class constants
    
    # -----------------------------------------------------------------------
    #       Class Functions
    # -----------------------------------------------------------------------
    # None
    
    
    # -----------------------------------------------------------------------
    #       Instance Functions
    # -----------------------------------------------------------------------
    def __init__(self, data, tx_alg):
        self.data = data
        self.tx_alg = tx_alg
        
    def getNextMessage(self, playback_time):
        return Message(str(playback_time) + ": " + self.data)
        