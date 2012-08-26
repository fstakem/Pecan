#  .-------------------------------------------------------------------------.
#  |                                                                         |
#  |                          T R A N S M I T T E R                          |
#  |                                                                         |
#  '-------------------------------------------------------------------------'

#  By: Fred Stakem 
#  Date: 8.11.12

# Libraries
import threading
import time

# Classes
from Message import Message

class Transmitter(threading.Thread):
    """This is a class that transmits mocap state information."""
    
    # Class constants
    
    # -----------------------------------------------------------------------
    #       Class Functions
    # -----------------------------------------------------------------------
    # None
    
    
    # -----------------------------------------------------------------------
    #       Instance Functions
    # -----------------------------------------------------------------------
    def __init__(self, client, tx_alg, remote_hosts, time_step_sec=.001):
        self.client = client
        self.tx_alg = tx_alg
        self.remote_hosts = remote_hosts
        self.playback_time = 0
        self.time_step_sec = time_step_sec
        self.running = False
        threading.Thread.__init__(self)
        
    def start(self): 
        self.running = True
        threading.Thread.start(self)
           
    def stop(self):
        self.running = False
        
    def run(self):
        initial_playback_time = self.playback_time
        start_time = time.time()
        while self.running:
            current_time = time.time()
            delta_time = current_time - start_time
            self.playback_time = initial_playback_time + delta_time
            next_message = self.source.getNextMessage(self.playback_time)
            
            if next_message != None:
                for host in self.remote_hosts:
                    self.client.sendMsg(host['ip'], host['port'], next_message)
                    
            time.sleep(self.time_step_sec)
            
    
    
    
    