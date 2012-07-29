#  .-------------------------------------------------------------------------.
#  |                                                                         |
#  |                        A C C L A I M  R O O T                           |
#  |                                                                         |
#  '-------------------------------------------------------------------------'

#  By: Fred Stakem 
#  Date: 7.13.12

# Libraries
import logging

# Classes
from MocapMath import Vector
from MocapDataFormats import Axis
from MocapDataFormats import OperationOnAxis

class AcclaimRoot(object):
    """This is a class that contains data in the Acclaim root Mocap data format."""
    
    # Setup logging
    logger = logging.getLogger('AcclaimRoot')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s %(asctime)s %(name)s Line: %(lineno)d |  %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    # Class constants
    
    # -----------------------------------------------------------------------
    #       Class Functions
    # -----------------------------------------------------------------------
    # None
    
        
    # -----------------------------------------------------------------------
    #       Instance Functions
    # -----------------------------------------------------------------------
    def __init__(self):
        self.amc_data_order = []
        self.orientation_order = []
        self.position = Vector()
        self.orientation = Vector()
        
    def __str__(self):
        output = ''
        
        token_str = ''
        for i, order in enumerate(self.amc_data_order):
            token_str += str(order) 
            if i < len(self.amc_data_order) - 1:
                token_str += ' '
        
        output += 'Data Order: %s ' %( token_str )
        
        token_str = ''
        for i, order in enumerate(self.orientation_order):
            token_str += str(order)
            if i < len(self.orientation_order) - 1:
                token_str += ' '
        
        output += 'Orientation Order: %s ' %( token_str )
        output += 'Position: %s ' %( self.position.toString('(', ', ', ')') )
        output += 'Orientation: %s' %( self.orientation.toString('(', ', ', ')') )
        
        return output
    
    
    
    