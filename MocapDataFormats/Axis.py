#  .-------------------------------------------------------------------------.
#  |                                                                         |
#  |                              A X I S                                    |
#  |                                                                         |
#  '-------------------------------------------------------------------------'

#  By: Fred Stakem 
#  Date: 7.13.12

# Libraries

# Classes

class Axis(object):
    """This is a class that contains for Axis information in Acclaim Mocap format."""
    
    # Class constants
    X = 1
    Y = 2
    Z = 3
    UNDEFINED = 1000
    
    # -----------------------------------------------------------------------
    #       Class Functions
    # -----------------------------------------------------------------------
    @classmethod
    def getAxisFromString(cls, axis):
        axis = axis.lower()
        if axis == 'x':
            return cls.X
        elif axis == 'y':
            return cls.Y
        elif axis == 'z':
            return cls.Z
        
        return cls.UNDEFINED
    
    @classmethod
    def toString(cls, axis):
        if axis == cls.X:
            return 'X'
        elif axis == cls.Y:
            return 'Y'
        elif axis == cls.Z:
            return 'Z'
        
        return '?'



