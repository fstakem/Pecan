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
        self.a = Vector(1.0, 1.0, 1.0)
        self.b = Vector(2.0, 2.0, 2.0)
        self.c = Vector(-1.0, -1.0, -1.0)
        self.d = Vector(-2.0, -2.0, -2.0)
        self.e = Vector(3.0, 3.0, 3.0)
        self.f = Vector(-3.0, -3.0, -3.0)
    
    def tearDown(self):
        pass
    
    @log_test(logger, globals.log_seperator)
    def testNegative(self):
        VectorTest.logger.info( 'Taking the negative value of: %s' % (str(self.a)) )
        VectorTest.logger.info( 'Result: %s' % (str(-Vector(self.a))) )
        assert -self.a == self.c, 'Incorrect vector value: %s' % (str(-self.a))
        
        VectorTest.logger.info( 'Taking the negative value of: %s' % (str(self.d)) )
        VectorTest.logger.info( 'Result: %s' % (str(-Vector(self.d))) )
        assert -self.d == self.b, 'Incorrect vector value: %s' % (str(-self.d))
                
    @log_test(logger, globals.log_seperator)
    def testAdd(self):
        VectorTest.logger.info( 'Adding %s to %s.' % (str(self.a), str(self.b)) )
        z = self.a + self.b
        VectorTest.logger.info( 'Result: %s' % (str(z)) )
        assert z == self.e, 'Incorrect vector value: %s' % (str(z))
        
        VectorTest.logger.info( 'Adding %s to %s.' % (str(self.b), str(self.c)) )
        z = self.b + self.c
        VectorTest.logger.info( 'Result: %s' % (str(z)) )
        assert z == self.a, 'Incorrect vector value: %s' % (str(z))
        
        VectorTest.logger.info( 'Adding %s to %s.' % (str(self.c), str(self.d)) )
        z = self.c + self.d
        VectorTest.logger.info( 'Result: %s' % (str(z)) )
        assert z == self.f, 'Incorrect vector value: %s' % (str(z))
        
        self.assertRaises(AttributeError, Vector.__add__, self.a, 1)
        
    @log_test(logger, globals.log_seperator)
    def testReflectiveAdd(self):
        VectorTest.logger.info( 'Adding %s to %s.' % (str(self.a), str(self.b)) )
        z = self.a + self.b
        VectorTest.logger.info( 'Result: %s' % (str(z)) )
        assert z == self.e, 'Incorrect vector value: %s' % (str(z))
        
        VectorTest.logger.info( 'Adding %s to %s.' % (str(self.b), str(self.c)) )
        z = self.b + self.c
        VectorTest.logger.info( 'Result: %s' % (str(z)) )
        assert z == self.a, 'Incorrect vector value: %s' % (str(z))
        
        VectorTest.logger.info( 'Adding %s to %s.' % (str(self.c), str(self.d)) )
        z = self.c + self.d
        VectorTest.logger.info( 'Result: %s' % (str(z)) )
        assert z == self.f, 'Incorrect vector value: %s' % (str(z))
        
        self.assertRaises(AttributeError, Vector.__radd__, self.a, 1)
    
    @log_test(logger, globals.log_seperator)
    def testAugmentedAdd(self):
        VectorTest.logger.info( 'Adding %s to %s.' % (str(self.a), str(self.b)) )
        self.a += self.b
        VectorTest.logger.info( 'Result: %s' % (str(self.a)) )
        assert self.a == self.e, 'Incorrect vector value: %s' % (str(self.a))
        
        VectorTest.logger.info( 'Adding %s to %s.' % (str(self.b), str(self.c)) )
        self.b += self.c
        VectorTest.logger.info( 'Result: %s' % (str(self.b)) )
        assert self.b == Vector(1.0, 1.0, 1.0), 'Incorrect vector value: %s' % (str(self.b))
        
        VectorTest.logger.info( 'Adding %s to %s.' % (str(self.c), str(self.d)) )
        self.c += self.d
        VectorTest.logger.info( 'Result: %s' % (str(self.c)) )
        assert self.c == self.f, 'Incorrect vector value: %s' % (str(self.c))
        
        self.assertRaises(AttributeError, Vector.__iadd__, self.a, 1)
    
    @log_test(logger, globals.log_seperator)
    def testSubtract(self):
        VectorTest.logger.info( 'Subtracting %s from %s.' % (str(self.a), str(self.b)) )
        z = self.b - self.a
        VectorTest.logger.info( 'Result: %s' % (str(z)) )
        assert z == self.a, 'Incorrect vector value: %s' % (str(z))
        
        VectorTest.logger.info( 'Subtracting %s from %s.' % (str(self.b), str(self.c)) )
        z = self.c - self.b
        VectorTest.logger.info( 'Result: %s' % (str(z)) )
        assert z == self.f, 'Incorrect vector value: %s' % (str(z))
        
        VectorTest.logger.info( 'Subtracting %s from %s.' % (str(self.c), str(self.d)) )
        z = self.d - self.c
        VectorTest.logger.info( 'Result: %s' % (str(z)) )
        assert z == self.c, 'Incorrect vector value: %s' % (str(z))
        
        self.assertRaises(AttributeError, Vector.__sub__, self.a, 1)
    
    @log_test(logger, globals.log_seperator)
    def testReflectiveSubtract(self):
        VectorTest.logger.info( 'Subtracting %s from %s.' % (str(self.a), str(self.b)) )
        z = self.b - self.a
        VectorTest.logger.info( 'Result: %s' % (str(z)) )
        assert z == self.a, 'Incorrect vector value: %s' % (str(z))
        
        VectorTest.logger.info( 'Subtracting %s from %s.' % (str(self.b), str(self.c)) )
        z = self.c - self.b
        VectorTest.logger.info( 'Result: %s' % (str(z)) )
        assert z == self.f, 'Incorrect vector value: %s' % (str(z))
        
        VectorTest.logger.info( 'Subtracting %s from %s.' % (str(self.c), str(self.d)) )
        z = self.d - self.c
        VectorTest.logger.info( 'Result: %s' % (str(z)) )
        assert z == self.c, 'Incorrect vector value: %s' % (str(z))
        
        self.assertRaises(AttributeError, Vector.__rsub__, self.a, 1)
    
    @log_test(logger, globals.log_seperator)
    def testAugmentedSubtract(self):
        VectorTest.logger.info( 'Subtracting %s from %s.' % (str(self.a), str(self.b)) )
        self.b -= self.a
        VectorTest.logger.info( 'Result: %s' % (str(self.b)) )
        assert self.b == self.a, 'Incorrect vector value: %s' % (str(self.b))
        
        VectorTest.logger.info( 'Subtracting %s from %s.' % (str(self.a), str(self.d)) )
        self.d -= self.a
        VectorTest.logger.info( 'Result: %s' % (str(self.d)) )
        assert self.d == self.f, 'Incorrect vector value: %s' % (str(self.d))
        
        VectorTest.logger.info( 'Subtracting %s from %s.' % (str(self.c), str(self.f)) )
        self.c -= self.f
        VectorTest.logger.info( 'Result: %s' % (str(self.c)) )
        assert self.c == Vector(2.0, 2.0, 2.0), 'Incorrect vector value: %s' % (str(self.c))
        
        self.assertRaises(AttributeError, Vector.__isub__, self.a, 1)
    
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
   
   
   