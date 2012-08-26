#  .-------------------------------------------------------------------------.
#  |                                                                         |
#  |                       M E S S A G E  T E S T                            |
#  |                                                                         |
#  '-------------------------------------------------------------------------'

#  By: Fred Stakem 
#  Date: 8.25.12

# Libraries
import logging
import unittest

# Classes
from Globals import *
from Utilities import *

class MessageTest(unittest.TestCase):
       
    # Setup logging
    logger = logging.getLogger('MessageTest')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s %(asctime)s %(name)s Line: %(lineno)d |  %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    # Class constants
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    @log_test(logger, globals.log_seperator)
    def testXxx(self):
        pass