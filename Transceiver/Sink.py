#  .-------------------------------------------------------------------------.
#  |                                                                         |
#  |                                 S I N K                                 |
#  |                                                                         |
#  '-------------------------------------------------------------------------'

#  By: Fred Stakem 
#  Date: 8.16.12

# Libraries

# Classes

class Sink(object):
    """This is a class that controls the flow of mocap state information."""
    
    # Class constants
    
    # -----------------------------------------------------------------------
    #       Class Functions
    # -----------------------------------------------------------------------
    # None
    
    
    # -----------------------------------------------------------------------
    #       Instance Functions
    # -----------------------------------------------------------------------
    def __init__(self, rx_alg):
        self.data = None
        self.rx_alg = rx_alg
        
    def setEvent(self, time_delta):
        pass
        