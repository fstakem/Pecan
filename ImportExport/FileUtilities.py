#  .-------------------------------------------------------------------------.
#  |                                                                         |
#  |                       F I L E  U T I L I T I E S                        |
#  |                                                                         |
#  '-------------------------------------------------------------------------'

#  By: Fred Stakem 
#  Date: 7.13.12

# Libraries
import logging

# Classes

# Setup logging
logger = logging.getLogger('FileUtilities')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s %(asctime)s %(name)s Line: %(lineno)d |  %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

# Functions
def readLinesFromFile(file_name):
    f = open(file_name, "r")
    lines = f.readlines()
    f.close()
    
    return lines