#  .-------------------------------------------------------------------------.
#  |                                                                         |
#  |                       A C C L A I M  F R A M E                          |
#  |                                                                         |
#  '-------------------------------------------------------------------------'

#  By: Fred Stakem 
#  Date: 7.28.12

# Libraries
import logging
from collections import OrderedDict

# Classes
from MocapMath import Vector

class AcclaimFrame(object):
    """This is a class that contains data in the Acclaim frame Mocap data format."""
    
    # Setup logging
    logger = logging.getLogger('AcclaimFrame')
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
        self.number = 0
        self.bone_orientations = OrderedDict()
        
    def __str__(self):
        output = 'Number: ' + str(self.number) + ' '
        
        for key in self.bone_orientations.keys():
            output += key + ': '
            for i, value in enumerate(self.bone_orientations[key]):
                output += str(value) + ' '
        
        return output
    
    
    