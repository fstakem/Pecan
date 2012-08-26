#  .-------------------------------------------------------------------------.
#  |                                                                         |
#  |              R E C O N S T R U C T I O N  A L G O R I T M               |
#  |                                                                         |
#  '-------------------------------------------------------------------------'

#  By: Fred Stakem 
#  Date: 8.22.12

# Libraries

# Classes

class ReconstructionAlgorithm(object):
    """This is a class that dictates how mocap state information should be
       reconstructed."""
    
    # Class constants
    
    # -----------------------------------------------------------------------
    #       Class Functions
    # -----------------------------------------------------------------------
    # None
    
    
    # -----------------------------------------------------------------------
    #       Instance Functions
    # -----------------------------------------------------------------------
    def __init__(self):
        self.data = []
        self.msgs = []
        self.playback_time = 0
        
    def setNextMessage(self, msg):
        return None
        
        