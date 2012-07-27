#  .-------------------------------------------------------------------------.
#  |                                                                         |
#  |                        A C C L A I M  B O N E                           |
#  |                                                                         |
#  '-------------------------------------------------------------------------'

#  By: Fred Stakem 
#  Date: 7.13.12

# Libraries
import logging

# Classes
from MocapMath import Vector

class AcclaimBone(object):
    """This is a class that contains data in the Acclaim bone Mocap data format."""
    
    # Setup logging
    logger = logging.getLogger('AcclaimBone')
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
        self.id = 0
        self.name = ''
        self.direction = Vector()
        self.length = 0
        self.orientation = Vector()
        self.orientation_order = []
        self.dof = []
        self.limits = []
        
    def __str__(self):
        output = 'Bone: %s (%d)\n' % (self.name, self.id)
        output += 'Direction: %s  Length: %d\n' % (self.direction.toString('(', ', ', ')'), self.length)
        output += 'Orientation: %s  Order: %s\n' % (self.orientation.toString('(', ', ', ')'), ' '.join(self.orientation_order))
        output += 'Dof: %s\n' % (' '.join( str(self.dof)[1:-1].split(',') ))
        
        for limit in self.limits:
            limit_str = ' '.join( str(limit)[1:-1].split(',') )
            output += 'Limits: %s\n' % (limit_str)
        
        return output
        
        