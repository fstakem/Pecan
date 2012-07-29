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
    # None
    
    
    # -----------------------------------------------------------------------
    #       Instance Functions
    # -----------------------------------------------------------------------
    def __init__(self, operation_on_axis_str):
        self.value = None
        
        operation_on_axis = operation_on_axis_str.lower()
        if operation_on_axis == 'tx':
            self.value = OperationOnAxis.TX
        elif operation_on_axis == 'ty':
            self.value = OperationOnAxis.TY
        elif operation_on_axis == 'tz':
            self.value = OperationOnAxis.TZ
        elif operation_on_axis == 'rx':
            self.value = OperationOnAxis.RX
        elif operation_on_axis == 'ry':
            self.value = OperationOnAxis.RY
        elif operation_on_axis == 'rz':
            self.value = OperationOnAxis.RZ
        else:
            raise Exception('Incorrect value: %s' % (str(operation_on_axis_str)))
        
    def __str__(self):
        if self.value == OperationOnAxis.RX:
            return 'RX'
        elif self.value == OperationOnAxis.RY:
            return 'RY'
        elif self.value == OperationOnAxis.RZ:
            return 'RZ'
        elif self.value == OperationOnAxis.TX:
            return 'TX'
        elif self.value == OperationOnAxis.TY:
            return 'TY'
        elif self.value == OperationOnAxis.TZ:
            return 'TZ'
    
    def __eq__(self, other):
        if self.value == other.value:
            return True
        
        return False

