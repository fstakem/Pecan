#  .-------------------------------------------------------------------------.
#  |                                                                         |
#  |                   A M C  I M P O R T E R  T E S T                       |
#  |                                                                         |
#  '-------------------------------------------------------------------------'

#  By: Fred Stakem 
#  Date: 7.17.12

# Libraries
import logging
import unittest

# Classes

class AmcImporterTest(unittest.TestCase):
       
    # Setup logging
    logger = logging.getLogger('AmcImporterTest')
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