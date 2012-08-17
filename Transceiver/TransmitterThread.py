#  .-------------------------------------------------------------------------.
#  |                                                                         |
#  |                  T R A N S M I T T E R  T H R E A D                     |
#  |                                                                         |
#  '-------------------------------------------------------------------------'

#  By: Fred Stakem 
#  Date: 8.16.12

# Libraries
import threading
import time

# Classes
from Message import Message

class TransmitterThread(threading.Thread):
    """This is a class thread that transmits mocap state information."""
    
    # Class constants
    
    # -----------------------------------------------------------------------
    #       Class Functions
    # -----------------------------------------------------------------------
    # None
    
    
    # -----------------------------------------------------------------------
    #       Instance Functions
    # -----------------------------------------------------------------------
    def __init__(self, client, source, addresses, start_time):
        self.start_time = start_time
        self.client = client
        self.source = source
        self.addresses = addresses
        threading.Thread.__init__(self)
        self.running = True
        
    def run(self):
        while self.running:
            current_time = time.time()
            delta_time = current_time - self.start_time
            next_event = self.source.getEvent(delta_time)
            
            if next_event != None:
                msg = Message(next_event)
                for address in self.addresses:
                    self.client.sendMsg(address['ip'], address['port'], msg.convertToJson())

        
