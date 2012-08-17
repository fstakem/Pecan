#  .-------------------------------------------------------------------------.
#  |                                                                         |
#  |                             R E C E I V E R                             |
#  |                                                                         |
#  '-------------------------------------------------------------------------'

#  By: Fred Stakem 
#  Date: 8.11.12

# Libraries

# Classes

class Receiver(object):
    """This is a class that receives mocap state information."""
    
    # Class constants
    
    # -----------------------------------------------------------------------
    #       Class Functions
    # -----------------------------------------------------------------------
    # None
    
    
    # -----------------------------------------------------------------------
    #       Instance Functions
    # -----------------------------------------------------------------------
    def __init__(self):
        self.server = None
        self.sink = None
        self.clients = []
        
    def start(self):
        self.clients = []