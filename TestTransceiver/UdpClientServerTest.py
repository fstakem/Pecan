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

# Classes
from Globals import *
from Utilities import *
from Transceiver import UdpServer
from Transceiver import UdpServerHandler
from Transceiver import UdpClient

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
    simple_msg = 'This is a test.'
    
    def setUp(self):
        self.client = UdpClient()
        self.server = UdpServer( (UdpClientServerTest.server_address, 0), UdpServerHandler)
        self.ip_address, self.port = self.server.server_address
        UdpClientServerTest.logger.debug( 'Server created with address: %s:%s' % (self.ip_address, self.port) )
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.setName(True)
        self.server_thread.start()
    
    def tearDown(self):
        pass
    
    @log_test(logger, globals.log_seperator)
    def testSimpleConnectivity(self):
        UdpClientServerTest.logger.debug( 'Sending msg: "%s"' % (self.simple_msg) )
        self.client.sendMsg(self.ip_address, int(self.port), UdpClientServerTest.simple_msg)
        request, client_address = self.server.get_request()
        data = request[0].strip()
        print 'Test: ' + str(data)
        
    
    
    
    
    
    