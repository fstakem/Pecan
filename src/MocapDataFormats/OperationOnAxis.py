#  .-------------------------------------------------------------------------.
#  |                                                                         |
#  |                   O P E R A T I O N  O N  A X I S                       |
#  |                                                                         |
#  '-------------------------------------------------------------------------'

#  By: Fred Stakem 
#  Date: 7.13.12

# Libraries

# Classes

class OperationOnAxis(object):
    """This is a class that contains for OperationOnAxis information in Acclaim Mocap format."""
    
    # Class constants
    TX = 1
    TY = 2
    TZ = 3
    RX = 4
    RY = 5
    RZ = 6
    
    # -----------------------------------------------------------------------
    #       Class Functions
    # -----------------------------------------------------------------------
    @classmethod
    def getOperationOnAxisFromString(cls, operation_on_axis):
        pass
    
    @classmethod
    def toString(cls, axis):
        pass

