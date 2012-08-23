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
from Transceiver import Transmitter
from Transceiver import Receiver
from Transceiver import Message
from Transceiver import UdpClient
from Transceiver import UdpServer
from Transceiver import UdpServerHandler
from Transceiver import Source
from Transceiver import Sink
from NetworkingAlgorithms import TransmissionAlgorithm
from NetworkingAlgorithms import ReconstructionAlgorithm


class TxRxTest(unittest.TestCase):
    
    # Setup logging
    logger = logging.getLogger('TxRxTest')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s %(asctime)s %(name)s Line: %(lineno)d |  %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    # Class constants
    server_address = 'localhost'
    server_port = 8080
    simple_msg = Message('This is a test.')
    
    def setUp(self):
        # Setup the transmitter
        self.client = UdpClient()
        self.data = TxRxTest.simple_msg
        self.tx_alg = TransmissionAlgorithm()
        self.source = Source(self.data, self.tx_alg)
        self.remote_hosts = [ (TxRxTest.server_address, TxRxTest.server_port) ]
        self.transmitter = Transmitter(self.client, self.source, self.remote_hosts)
        
        # Setup the receiver
        self.server = UdpServer((TxRxTest.server_address, TxRxTest.server_port), UdpServerHandler)
        self.rx_alg = ReconstructionAlgorithm()
        self.sink = Sink(self.rx_alg)
        self.receiver = Receiver(self.server, self.sink)
    
    def tearDown(self):
        pass
    
    @log_test(logger, globals.log_seperator)
    def testxxx(self):
        pass