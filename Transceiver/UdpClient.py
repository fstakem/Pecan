#  .-------------------------------------------------------------------------.
#  |                                                                         |
#  |                            U D P  C L I E N T                           |
#  |                                                                         |
#  '-------------------------------------------------------------------------'

#  By: Fred Stakem 
#  Date: 8.11.12

# Libraries
import logging
import socket
from datetime import datetime

# Classes
from Message import Message

class UdpClient(object):
    """This is a class that transmits mocap state information with UDP."""
    
    # Setup logging
    logger = logging.getLogger('UdpClient')
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
        UdpClient.logger.debug( 'Creating a UDP client.' )
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def sendMsg(self, server_address, server_port, msg): 
        UdpClient.logger.debug('Sending UDP packet to: %s:%s' % (server_address, str(server_port)))
        msg.tx_time = datetime.now()
        UdpClient.logger.debug('Packet:' + str(msg))
        bytes_sent = self.socket.sendto(msg.convertToJson(), (server_address, server_port))
        UdpClient.logger.debug('Sent %s bytes.' % (str(bytes_sent)))
        
    def close(self):
        self.socket.close()
        
        
        