#  .-------------------------------------------------------------------------.
#  |                                                                         |
#  |                     R E C E I V E R  T H R E A D                        |
#  |                                                                         |
#  '-------------------------------------------------------------------------'

#  By: Fred Stakem 
#  Date: 8.16.12

# Libraries
import threading
import time

# Classes
from Message import Message

class ReceiverThread(threading.Thread):
    """This is a class thread that receives mocap state information."""
    
    # Class constants
    
    # -----------------------------------------------------------------------
    #       Class Functions
    # -----------------------------------------------------------------------
    # None
    
    
    # -----------------------------------------------------------------------
    #       Instance Functions
    # -----------------------------------------------------------------------
    def __init__(self, start_time):
        self.start_time = start_time
        threading.Thread.__init__(self)
        self.running = True
        
    def run(self):
        while self.running:
            current_time = time.time()
            delta_time = current_time - self.start_time
            

        
