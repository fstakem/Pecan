#  .-------------------------------------------------------------------------.
#  |                                                                         |
#  |                               M E S S A G E                             |
#  |                                                                         |
#  '-------------------------------------------------------------------------'

#  By: Fred Stakem 
#  Date: 8.15.12

# Libraries
#import jsonpickle

# Classes

class Message(object):
    """This is a class that mocap state information is stored in before 
       being transmitted and after being received."""
    
    # Class constants
    
    # -----------------------------------------------------------------------
    #       Class Functions
    # -----------------------------------------------------------------------
    # None
    
    
    # -----------------------------------------------------------------------
    #       Instance Functions
    # -----------------------------------------------------------------------
    def __init__(self, data):
        self.data = data
        
    def convertToJson(self):
        return self.data
    
    def getFromJson(self, msg):
        self.data = msg
        
    def __eq__(self, msg):
        if msg != None and self.data == msg.data:
            return True
        else:
            return False