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
    UNDEFINED = 1000
    
    # -----------------------------------------------------------------------
    #       Class Functions
    # -----------------------------------------------------------------------
    @classmethod
    def getOperationOnAxisFromString(cls, operation_on_axis):
        operation_on_axis = operation_on_axis.lower()
        if operation_on_axis == 'tx':
            return cls.TX
        elif operation_on_axis == 'ty':
            return cls.TY
        elif operation_on_axis == 'tz':
            return cls.TZ
        elif operation_on_axis == 'rx':
            return cls.RX
        elif operation_on_axis == 'ry':
            return cls.RY
        elif operation_on_axis == 'rz':
            return cls.RZ
        
        return cls.UNDEFINED
    
    @classmethod
    def toString(cls, operation_on_axis):
        if operation_on_axis == cls.RX:
            return 'RX'
        elif operation_on_axis == cls.RY:
            return 'RY'
        elif operation_on_axis == cls.RZ:
            return 'RZ'
        elif operation_on_axis == cls.TX:
            return 'TX'
        elif operation_on_axis == cls.TY:
            return 'TY'
        elif operation_on_axis == cls.TZ:
            return 'TZ'
        
        return '?'

