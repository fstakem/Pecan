#  .-------------------------------------------------------------------------.
#  |                                                                         |
#  |                                  H O S T                                |
#  |                                                                         |
#  '-------------------------------------------------------------------------'

#  By: Fred Stakem 
#  Date: 8.11.12

# Libraries

# Classes

class Host(object):
    """This is a class that controls the transmission and reception of 
       mocap state information."""
    
    # Class constants
    
    # -----------------------------------------------------------------------
    #       Class Functions
    # -----------------------------------------------------------------------
    # None
    
    
    # -----------------------------------------------------------------------
    #       Instance Functions
    # -----------------------------------------------------------------------
    def __init__(self):
        self.peers = []
        self.transmitter = None
        self.receiver = None