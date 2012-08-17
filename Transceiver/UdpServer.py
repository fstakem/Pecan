#  .-------------------------------------------------------------------------.
#  |                                                                         |
#  |                            U D P  S E R V E R                           |
#  |                                                                         |
#  '-------------------------------------------------------------------------'

#  By: Fred Stakem 
#  Date: 8.11.12

# Libraries
import logging
import SocketServer

# Classes
from UdpServerHandler import UdpServerHandler

class UdpServer(SocketServer.UDPServer, SocketServer.ThreadingMixIn):
    """This is a class that receives mocap state information with UDP."""
    
    # Setup logging
    logger = logging.getLogger('UdpServer')
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
    def __init__(self, server_address, handler_class=UdpServerHandler):
        SocketServer.UDPServer.__init__(self, server_address, handler_class)
        self.last_rcvd_msg = None
        
    def finish_request(self, request, client_address):
        handler = self.RequestHandlerClass(request, client_address, self)
        self.last_rcvd_msg = handler.rcvd_msg
        
    def _handle_request_noblock(self):
        return SocketServer.UDPServer._handle_request_noblock(self)
                   
    
    
    
    
    
    