#  .-------------------------------------------------------------------------.
#  |                                                                         |
#  |                           T X  R X  T E S T                             |
#  |                                                                         |
#  '-------------------------------------------------------------------------'

#  By: Fred Stakem 
#  Date: 8.22.12

# Libraries
import logging
import unittest

# Classes
from Globals import *
from Utilities import *
from Tranceiver import Transmitter
from Transceiver import TransmitterThread
from Transceiver import Receiver
from Transceiver import ReceiverThread

class TxRxTest(unittest.TestCase):
    
    # Setup logging
    logger = logging.getLogger('TxRxTest')
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
    def testxxx(self):
        pass