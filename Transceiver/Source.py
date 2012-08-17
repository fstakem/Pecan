#  .-------------------------------------------------------------------------.
#  |                                                                         |
#  |                               S O U R C E                               |
#  |                                                                         |
#  '-------------------------------------------------------------------------'

#  By: Fred Stakem 
#  Date: 8.16.12

# Libraries

# Classes

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
    def __init__(self):
        self.data = None
        self.tx_alg = None
        
    def getEvent(self, time_delta):
        pass
        