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
    
    # -----------------------------------------------------------------------
    #       Class Functions
    # -----------------------------------------------------------------------
    # None
    
    
    # -----------------------------------------------------------------------
    #       Instance Functions
    # -----------------------------------------------------------------------
    def __init__(self, axis_str):
        self.value = None
        
        axis = axis_str.lower()
        if axis == 'x':
            self.value = Axis.X
        elif axis == 'y':
            self.value = Axis.Y
        elif axis == 'z':
            self.value = Axis.Z
        else:
            raise Exception('Incorrect value: %s' % (str(axis_str)))
        
    def __str__(self):
        if self.value == Axis.X:
            return 'X'
        elif self.value == Axis.Y:
            return 'Y'
        elif self.value == Axis.Z:
            return 'Z'
    
    def __eq__(self, other):
        if self.value == other.value:
            return True
        
        return False
    
    
    



