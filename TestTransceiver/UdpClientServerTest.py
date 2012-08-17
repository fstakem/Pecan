#  .-------------------------------------------------------------------------.
#  |                                                                         |
#  |               U D P  C L I E N T  S E R V E R  T E S T                  |
#  |                                                                         |
#  '-------------------------------------------------------------------------'

#  By: Fred Stakem 
#  Date: 7.17.12

# Libraries
import logging
import unittest
import threading
import time

# Classes
from Globals import *
from Utilities import *
from Transceiver import UdpServer
from Transceiver import UdpServerHandler
from Transceiver import UdpClient
from Transceiver import Message

class UdpClientServerTest(unittest.TestCase):
       
    # Setup logging
    logger = logging.getLogger('UdpClientServerTest')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s %(asctime)s %(name)s Line: %(lineno)d |  %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    # Class constants
    server_address = 'localhost'
    simple_msg = Message('This is a test.')
    
    def setUp(self):
        self.client = UdpClient()
        self.server = UdpServer( (UdpClientServerTest.server_address, 0), UdpServerHandler)
        self.ip_address, self.port = self.server.server_address
        UdpClientServerTest.logger.debug( 'Server created with address: %s:%s' % (self.ip_address, self.port) )
        self.server_thread = threading.Thread(name='udp server', target=self.server.serve_forever)
        self.server_thread.start()
    
    def tearDown(self):
        self.server.shutdown()
        self.client.close()
    
    @log_test(logger, globals.log_seperator)
    def testSimpleConnectivity(self):
        wait_time_for_msg = 0.5
        UdpClientServerTest.logger.debug( 'Sending message: "%s"' % (self.simple_msg.convertToJson()) )
        self.client.sendMsg(self.ip_address, int(self.port), UdpClientServerTest.simple_msg)
        
        time.sleep(wait_time_for_msg)
        if self.server.last_rcvd_msg == None:
            assert False, 'No message received.'
            
        rcvd_msg = self.server.last_rcvd_msg
        UdpClientServerTest.logger.debug( 'Received message: "%s"' % (rcvd_msg.convertToJson()) )
        assert UdpClientServerTest.simple_msg == rcvd_msg, 'Incorrect message value: %s' % \
               (rcvd_msg.convertToJson())
        
    
    
    
    
    
    