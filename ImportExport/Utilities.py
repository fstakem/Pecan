#  .-------------------------------------------------------------------------.
#  |                                                                         |
#  |                           U T I L I T I E S                             |
#  |                                                                         |
#  '-------------------------------------------------------------------------'

#  By: Fred Stakem 
#  Date: 7.20.12

# Libraries
import logging

# Setup logging
logger = logging.getLogger('Utilities')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s %(asctime)s %(name)s Line: %(lineno)d |  %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

# Functions
def readLinesFromFile(filename):
    f = open(filename, "r")
    lines = f.readlines()
    f.close()
    
    return lines