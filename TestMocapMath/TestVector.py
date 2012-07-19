#  .-------------------------------------------------------------------------.
#  |                                                                         |
#  |                        V E C T O R  T E S T                             |
#  |                                                                         |
#  '-------------------------------------------------------------------------'

#  By: Fred Stakem 
#  Date: 7.17.12

# Libraries
import logging
import unittest

# Classes

class VectorTest(unittest.TestCase):
       
    # Setup logging
    logger = logging.getLogger('VectorTest')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s %(asctime)s %(name)s Line: %(lineno)d |  %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def testXXX(self):
        pass
    
if __name__=='__main__':
   unittest.main()