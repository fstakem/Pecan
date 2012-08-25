#  .-------------------------------------------------------------------------.
#  |                                                                         |
#  |                    U D P  S E R V E R  H A N D L E R                    |
#  |                                                                         |
#  '-------------------------------------------------------------------------'

#  By: Fred Stakem 
#  Date: 8.11.12

# Libraries
import logging
from datetime import datetime
import SocketServer

# Classes
from Message import Message

class UdpServerHandler(SocketServer.BaseRequestHandler):
    """This is a class handles mocap state information received from UDP."""
    
    # Setup logging
    logger = logging.getLogger('UdpServerHandler')
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
    def __init__(self, request, client_address, server):
        self.rcvd_msg = None
        SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)
        
    def setup(self):
        SocketServer.BaseRequestHandler.setup(self)
        
    def handle(self):
        UdpServerHandler.logger.debug('Handling a UDP packet.')
        
        json_message = self.request[0].strip()
        self.rcvd_msg = Message()
        self.rcvd_msg.getFromJson(json_message)
        self.rcvd_msg.rx_time = datetime.now()
    
    def finish(self):
        SocketServer.BaseRequestHandler.finish(self)
        
        
        
        
        
        
    
    
    
    
    
    
    