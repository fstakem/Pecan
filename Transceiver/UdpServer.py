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
    def __init__(self, server_address, handler_class=UdpServerHandler, receiver=None):
        UdpServer.logger.debug( 'Creating a UDP server with address: %s:%s' % (server_address[0], server_address[1]) )
        SocketServer.UDPServer.__init__(self, server_address, handler_class)
        self.receiver = receiver
        self.last_rcvd_msg = None
        
    def finish_request(self, request, client_address):
        handler = self.RequestHandlerClass(request, client_address, self)
        self.last_rcvd_msg = handler.rcvd_msg
        
        UdpServer.logger.debug( 'Received a packet from: %s:%s' % (client_address[0], str(client_address[1])))
        UdpServer.logger.debug(str('Packet:' + str(self.last_rcvd_msg)))
        
        if self.receiver != None:
            self.receiver.newMsgRcvd(self.last_rcvd_msg)
        
    def _handle_request_noblock(self):
        return SocketServer.UDPServer._handle_request_noblock(self)
                   
    
    
    
    
    
    