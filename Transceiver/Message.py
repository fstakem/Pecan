#  .-------------------------------------------------------------------------.
#  |                                                                         |
#  |                               M E S S A G E                             |
#  |                                                                         |
#  '-------------------------------------------------------------------------'

#  By: Fred Stakem 
#  Date: 8.15.12

# Libraries
import json
import jsonpickle

# Classes

class Message(object):
    """This is a class that mocap state information is stored in before 
       being transmitted and after being received."""
    
    # Class constants
    json_indent = 4
    
    # -----------------------------------------------------------------------
    #       Class Functions
    # -----------------------------------------------------------------------
    # None
    
    
    # -----------------------------------------------------------------------
    #       Instance Functions
    # -----------------------------------------------------------------------
    def __init__(self, seq_number=-1, data=None):
        self.tx_time = None
        self.rx_time = None
        self.seq_number = seq_number
        self.data = data
        
    def convertToJson(self):
        output = [ self.seq_number, self.tx_time, self.rx_time, self.data ]
        return jsonpickle.encode( output )
    
    def getFromJson(self, msg):
        decoded_msg = jsonpickle.decode(msg)
        self.seq_number = decoded_msg[0]
        self.tx_time = decoded_msg[1]
        self.rx_time = decoded_msg[2]
        self.data = decoded_msg[3]
        
    def __str__(self):
        output = '\n- Packet Contents Start -\n'
        output += 'Sequence number: %s\n' % (str(self.seq_number))
        output += 'Transmitted time: %s\n' % (str(self.tx_time))
        output += 'Received time: %s\n' % (str(self.rx_time))
        output += 'Data:\n' + json.dumps(self.data, indent=Message.json_indent) + '\n'
        output += '- Packet Contents End -'
        
        return output
        
    def __eq__(self, msg):
        if msg != None and self.seq_number == msg.seq_number and self.data == msg.data:
            return True
        else:
            return False
        
        
        
        