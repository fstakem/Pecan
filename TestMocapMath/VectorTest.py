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
from Globals import *
from Utilities import *
from MocapMath import Vector

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
    
    @log_test(logger, globals.log_seperator)
    def testNegative(self):
        a = Vector(1.0, 1.0, 1.0)
        assert -a == Vector(-1.0, -1.0, -1.0), 'Incorrect vector value: %s' % (str(a))
        
        a = Vector(-1.0, -1.0, -1.0)
        assert -a == Vector(1.0, 1.0, 1.0), 'Incorrect vector value: %s' % (str(a))
        
    @log_test(logger, globals.log_seperator)   
    def testPositive(self):
        a = Vector(-1.0, -1.0, -1.0)
        assert +a == Vector(1.0, 1.0, 1.0), 'Incorrect vector value: %s' % (str(a))
        
    @log_test(logger, globals.log_seperator)
    def testAdd(self):
        pass
    
    @log_test(logger, globals.log_seperator)
    def testReflectiveAdd(self):
        pass
    
    @log_test(logger, globals.log_seperator)
    def testAugmentedAdd(self):
        pass
    
    @log_test(logger, globals.log_seperator)
    def testSubtract(self):
        pass
    
    @log_test(logger, globals.log_seperator)
    def testReflectiveSubtract(self):
        pass
    
    @log_test(logger, globals.log_seperator)
    def testAugmentedSubtract(self):
        pass
    
    @log_test(logger, globals.log_seperator)
    def testMultiply(self):
        pass
    
    @log_test(logger, globals.log_seperator)
    def testReflectiveMultiply(self):
        pass
    
    @log_test(logger, globals.log_seperator)
    def testAugmentedMultiply(self):
        pass
    
    @log_test(logger, globals.log_seperator)
    def testDivide(self):
        pass
    
    @log_test(logger, globals.log_seperator)
    def testReflectiveDivide(self):
        pass
    
    @log_test(logger, globals.log_seperator)
    def testAugmentedDivide(self):
        pass
    
    @log_test(logger, globals.log_seperator)
    def testEqual(self):
        pass
    
    @log_test(logger, globals.log_seperator)
    def testNotEqual(self):
        pass
    
    @log_test(logger, globals.log_seperator)
    def testAbsoluteValue(self):
        pass
    
    @log_test(logger, globals.log_seperator)
    def testGetItem(self):
        pass
    
    @log_test(logger, globals.log_seperator)
    def testSetItem(self):
        pass
    
    @log_test(logger, globals.log_seperator)
    def testCall(self):
        pass
    
    @log_test(logger, globals.log_seperator)
    def testString(self):
        pass
    
    @log_test(logger, globals.log_seperator)
    def testToString(self):
        pass
    
    @log_test(logger, globals.log_seperator)
    def testDistance(self):
        pass
    
    @log_test(logger, globals.log_seperator)
    def testMagnitude(self):
        pass
    
    @log_test(logger, globals.log_seperator)
    def testDot(self):
        pass
    
    @log_test(logger, globals.log_seperator)
    def testCross(self):
        pass
    
    @log_test(logger, globals.log_seperator)
    def testNormalize(self):
        pass  
    
if __name__=='__main__':
   unittest.main()
   
   
   