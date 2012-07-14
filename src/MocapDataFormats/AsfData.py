#  .-------------------------------------------------------------------------.
#  |                                                                         |
#  |                             A S F  D A T A                              |
#  |                                                                         |
#  '-------------------------------------------------------------------------'

#  By: Fred Stakem 
#  Date: 7.13.12

# Libraries
import logging

# Classes

class AsfData(object):
    """This is a class that contains data in the ASF Mocap data format."""
    
    # Setup logging
    logger = logging.getLogger('AsfData')
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
        pass