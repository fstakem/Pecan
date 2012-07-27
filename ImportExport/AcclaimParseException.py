#  .-------------------------------------------------------------------------.
#  |                                                                         |
#  |             A C C L A I M  P A R S E  E X C E P T I O N                 |
#  |                                                                         |
#  '-------------------------------------------------------------------------'

#  By: Fred Stakem 
#  Date: 7.21.12

# Libraries
import sys

# Classes

class AcclaimParseException(Exception):
    """This is a class for custom Acclaim parsing exceptions."""
    
    def __init__(self, *args):
        Exception.__init__(self, *args)
        self.wrapped_exc = sys.exc_info( )