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
        VectorTest.logger.info( 'Operation: -%s' % (str(self.a)) )
        VectorTest.logger.info( 'Result: %s' % (str(-Vector(self.a))) )
        assert -self.a == self.c, 'Incorrect vector value: %s' % (str(-self.a))
        
        VectorTest.logger.info( 'Operation: -%s' % (str(self.a)) )
        VectorTest.logger.info( 'Result: %s' % (str(-Vector(self.d))) )
        assert -self.d == self.b, 'Incorrect vector value: %s' % (str(-self.d))
                
    @log_test(logger, globals.log_seperator)
    def testAdd(self):
        VectorTest.logger.info( 'Operation: %s + %s' % (str(self.a), str(self.b)) )
        z = self.a + self.b
        VectorTest.logger.info( 'Result: %s' % (str(z)) )
        assert z == self.e, 'Incorrect vector value: %s' % (str(z))
        
        VectorTest.logger.info( 'Operation: %s + %s' % (str(self.b), str(self.c)) )
        z = self.b + self.c
        VectorTest.logger.info( 'Result: %s' % (str(z)) )
        assert z == self.a, 'Incorrect vector value: %s' % (str(z))
        
        VectorTest.logger.info( 'Operation: %s + %s' % (str(self.c), str(self.d)) )
        z = self.c + self.d
        VectorTest.logger.info( 'Result: %s' % (str(z)) )
        assert z == self.f, 'Incorrect vector value: %s' % (str(z))
        
        self.assertRaises(AttributeError, Vector.__add__, self.a, 1)
        
    @log_test(logger, globals.log_seperator)
    def testReflectiveAdd(self):
        VectorTest.logger.info( 'Operation: %s + %s' % (str(self.a), str(self.b)) )
        z = self.a + self.b
        VectorTest.logger.info( 'Result: %s' % (str(z)) )
        assert z == self.e, 'Incorrect vector value: %s' % (str(z))
        
        VectorTest.logger.info( 'Operation: %s + %s' % (str(self.b), str(self.c)) )
        z = self.b + self.c
        VectorTest.logger.info( 'Result: %s' % (str(z)) )
        assert z == self.a, 'Incorrect vector value: %s' % (str(z))
        
        VectorTest.logger.info( 'Operation: %s + %s' % (str(self.c), str(self.d)) )
        z = self.c + self.d
        VectorTest.logger.info( 'Result: %s' % (str(z)) )
        assert z == self.f, 'Incorrect vector value: %s' % (str(z))
        
        self.assertRaises(AttributeError, Vector.__radd__, self.a, 1)
    
    @log_test(logger, globals.log_seperator)
    def testAugmentedAdd(self):
        VectorTest.logger.info( 'Operation: %s += %s' % (str(self.a), str(self.b)) )
        self.a += self.b
        VectorTest.logger.info( 'Result: %s' % (str(self.a)) )
        assert self.a == self.e, 'Incorrect vector value: %s' % (str(self.a))
        
        VectorTest.logger.info( 'Operation: %s += %s' % (str(self.b), str(self.c)) )
        self.b += self.c
        VectorTest.logger.info( 'Result: %s' % (str(self.b)) )
        assert self.b == Vector(1.0, 1.0, 1.0), 'Incorrect vector value: %s' % (str(self.b))
        
        VectorTest.logger.info( 'Operation: %s += %s' % (str(self.c), str(self.d)) )
        self.c += self.d
        VectorTest.logger.info( 'Result: %s' % (str(self.c)) )
        assert self.c == self.f, 'Incorrect vector value: %s' % (str(self.c))
        
        self.assertRaises(AttributeError, Vector.__iadd__, self.a, 1)
    
    @log_test(logger, globals.log_seperator)
    def testSubtract(self):
        VectorTest.logger.info( 'Operation: %s - %s' % (str(self.b), str(self.a)) )
        z = self.b - self.a
        VectorTest.logger.info( 'Result: %s' % (str(z)) )
        assert z == self.a, 'Incorrect vector value: %s' % (str(z))
        
        VectorTest.logger.info( 'Operation: %s - %s' % (str(self.c), str(self.b)) )
        z = self.c - self.b
        VectorTest.logger.info( 'Result: %s' % (str(z)) )
        assert z == self.f, 'Incorrect vector value: %s' % (str(z))
        
        VectorTest.logger.info( 'Operation: %s - %s' % (str(self.d), str(self.c)) )
        z = self.d - self.c
        VectorTest.logger.info( 'Result: %s' % (str(z)) )
        assert z == self.c, 'Incorrect vector value: %s' % (str(z))
        
        self.assertRaises(AttributeError, Vector.__sub__, self.a, 1)
    
    @log_test(logger, globals.log_seperator)
    def testReflectiveSubtract(self):
        VectorTest.logger.info( 'Operation: %s - %s' % (str(self.b), str(self.a)) )
        z = self.b - self.a
        VectorTest.logger.info( 'Result: %s' % (str(z)) )
        assert z == self.a, 'Incorrect vector value: %s' % (str(z))
        
        VectorTest.logger.info( 'Operation: %s - %s' % (str(self.c), str(self.b)) )
        z = self.c - self.b
        VectorTest.logger.info( 'Result: %s' % (str(z)) )
        assert z == self.f, 'Incorrect vector value: %s' % (str(z))
        
        VectorTest.logger.info( 'Operation: %s - %s' % (str(self.d), str(self.c)) )
        z = self.d - self.c
        VectorTest.logger.info( 'Result: %s' % (str(z)) )
        assert z == self.c, 'Incorrect vector value: %s' % (str(z))
        
        self.assertRaises(AttributeError, Vector.__rsub__, self.a, 1)
    
    @log_test(logger, globals.log_seperator)
    def testAugmentedSubtract(self):
        VectorTest.logger.info( 'Operation: %s -= %s' % (str(self.b), str(self.a)) )
        self.b -= self.a
        VectorTest.logger.info( 'Result: %s' % (str(self.b)) )
        assert self.b == self.a, 'Incorrect vector value: %s' % (str(self.b))
        
        VectorTest.logger.info( 'Operation: %s -= %s' % (str(self.d), str(self.a)) )
        self.d -= self.a
        VectorTest.logger.info( 'Result: %s' % (str(self.d)) )
        assert self.d == self.f, 'Incorrect vector value: %s' % (str(self.d))
        
        VectorTest.logger.info( 'Operation: %s -= %s' % (str(self.c), str(self.f)) )
        self.c -= self.f
        VectorTest.logger.info( 'Result: %s' % (str(self.c)) )
        assert self.c == Vector(2.0, 2.0, 2.0), 'Incorrect vector value: %s' % (str(self.c))
        
        self.assertRaises(AttributeError, Vector.__isub__, self.a, 1)
    
    @log_test(logger, globals.log_seperator)
    def testMultiply(self):
        y = 3.0
        VectorTest.logger.info( 'Operation: %s * %s' % (str(self.a), str(y)) )
        z = self.a * y
        VectorTest.logger.info( 'Result: %s' % (str(z)) )
        assert z == self.e, 'Incorrect vector value: %s' % (str(z))
        
        y = -3.0
        VectorTest.logger.info( 'Operation: %s * %s' % (str(self.a), str(y)) )
        z = self.a * y
        VectorTest.logger.info( 'Result: %s' % (str(z)) )
        assert z == self.f, 'Incorrect vector value: %s' % (str(z))
        
        y = 3.0
        VectorTest.logger.info( 'Operation: %s * %s' % (str(self.c), str(y)) )
        z = self.c * y
        VectorTest.logger.info( 'Result: %s' % (str(z)) )
        assert z == self.f, 'Incorrect vector value: %s' % (str(z))
        
        y = -3.0
        VectorTest.logger.info( 'Operation: %s * %s' % (str(self.c), str(y)) )
        z = self.c * y
        VectorTest.logger.info( 'Result: %s' % (str(z)) )
        assert z == self.e, 'Incorrect vector value: %s' % (str(z))
        
        self.assertRaises(TypeError, Vector.__mul__, self.a, self.b)
    
    @log_test(logger, globals.log_seperator)
    def testReflectiveMultiply(self):
        y = 3.0
        VectorTest.logger.info( 'Operation: %s * %s' % (str(y), str(self.a)) )
        z = y * self.a
        VectorTest.logger.info( 'Result: %s' % (str(z)) )
        assert z == self.e, 'Incorrect vector value: %s' % (str(z))
        
        y = -3.0
        VectorTest.logger.info( 'Operation: %s * %s' % (str(y), str(self.a)) )
        z = y * self.a
        VectorTest.logger.info( 'Result: %s' % (str(z)) )
        assert z == self.f, 'Incorrect vector value: %s' % (str(z))
        
        y = 3.0
        VectorTest.logger.info( 'Operation: %s * %s' % (str(y), str(self.c)) )
        z = y * self.c
        VectorTest.logger.info( 'Result: %s' % (str(z)) )
        assert z == self.f, 'Incorrect vector value: %s' % (str(z))
        
        y = -3.0
        VectorTest.logger.info( 'Operation: %s * %s' % (str(y), str(self.c)) )
        z = y * self.c
        VectorTest.logger.info( 'Result: %s' % (str(z)) )
        assert z == self.e, 'Incorrect vector value: %s' % (str(z))
        
        self.assertRaises(TypeError, Vector.__rmul__, self.a, self.b)
    
    @log_test(logger, globals.log_seperator)
    def testAugmentedMultiply(self):
        y = 3.0
        VectorTest.logger.info( 'Operation: %s *= %s' % (str(self.a), str(y)) )
        self.a *= y
        VectorTest.logger.info( 'Result: %s' % (str(self.a)) )
        assert self.a == self.e, 'Incorrect vector value: %s' % (str(self.a))
        
        self.a = Vector(1.0, 1.0, 1.0)
        y = -3.0
        VectorTest.logger.info( 'Operation: %s *= %s' % (str(self.a), str(y)) )
        self.a *= y
        VectorTest.logger.info( 'Result: %s' % (str(self.a)) )
        assert self.a == self.f, 'Incorrect vector value: %s' % (str(self.a))
        
        y = 3.0
        VectorTest.logger.info( 'Operation: %s *= %s' % (str(self.c), str(y)) )
        self.c *= y
        VectorTest.logger.info( 'Result: %s' % (str(self.c)) )
        assert self.c == self.f, 'Incorrect vector value: %s' % (str(self.c))
        
        self.c = Vector(-1.0, -1.0, -1.0)
        y = -3.0
        VectorTest.logger.info( 'Operation: %s *= %s' % (str(self.c), str(y)) )
        self.c *= y
        VectorTest.logger.info( 'Result: %s' % (str(self.c)) )
        assert self.c == self.e, 'Incorrect vector value: %s' % (str(self.c))
        
        self.assertRaises(TypeError, Vector.__imul__, self.a, self.b)
    
    @log_test(logger, globals.log_seperator)
    def testDivide(self):
        x = Vector(2.0, 2.0, 2.0)
        y = 0.5
        VectorTest.logger.info( 'Operation: %s / %s' % (str(self.a), str(y)) )
        z = self.a / y
        VectorTest.logger.info( 'Result: %s' % (str(z)) )
        assert z == x, 'Incorrect vector value: %s' % (str(z))
        
        w = Vector(-2.0, -2.0, -2.0)
        y = -0.5
        VectorTest.logger.info( 'Operation: %s / %s' % (str(self.a), str(y)) )
        z = self.a / y
        VectorTest.logger.info( 'Result: %s' % (str(z)) )
        assert z == w, 'Incorrect vector value: %s' % (str(z))
        
        y = 0.5
        VectorTest.logger.info( 'Operation: %s / %s' % (str(self.c), str(y)) )
        z = self.c / y
        VectorTest.logger.info( 'Result: %s' % (str(z)) )
        assert z == w, 'Incorrect vector value: %s' % (str(z))
        
        y = -0.5
        VectorTest.logger.info( 'Operation: %s / %s' % (str(self.c), str(y)) )
        z = self.c / y
        VectorTest.logger.info( 'Result: %s' % (str(z)) )
        assert z == x, 'Incorrect vector value: %s' % (str(z))
        
        self.assertRaises(TypeError, Vector.__div__, self.a, self.b)
        
    @log_test(logger, globals.log_seperator)
    def testAugmentedDivide(self):
        x = Vector(2.0, 2.0, 2.0)
        y = 0.5
        VectorTest.logger.info( 'Operation: %s /= %s' % (str(self.a), str(y)) )
        self.a /= y
        VectorTest.logger.info( 'Result: %s' % (str(self.a)) )
        assert self.a == x, 'Incorrect vector value: %s' % (str(self.a))
        
        self.a = Vector(1.0, 1.0, 1.0)
        w = Vector(-2.0, -2.0, -2.0)
        y = -0.5
        VectorTest.logger.info( 'Operation: %s /= %s' % (str(self.a), str(y)) )
        self.a /= y
        VectorTest.logger.info( 'Result: %s' % (str(self.a)) )
        assert self.a == w, 'Incorrect vector value: %s' % (str(self.a))
        
        y = 0.5
        VectorTest.logger.info( 'Operation: %s /= %s' % (str(self.c), str(y)) )
        self.c /= y
        VectorTest.logger.info( 'Result: %s' % (str(self.c)) )
        assert self.c == w, 'Incorrect vector value: %s' % (str(self.c))
        
        self.c = Vector(-1.0, -1.0, -1.0)
        y = -0.5
        VectorTest.logger.info( 'Operation: %s /= %s' % (str(self.c), str(y)) )
        self.c /= y
        VectorTest.logger.info( 'Result: %s' % (str(self.c)) )
        assert self.c == x, 'Incorrect vector value: %s' % (str(self.c))
        
        self.assertRaises(TypeError, Vector.__idiv__, self.a, self.b)
    
    @log_test(logger, globals.log_seperator)
    def testEqual(self):
        z = Vector(1.0, 1.0, 1.0)
        VectorTest.logger.info( 'Operation: %s = %s' % (str(self.a), str(z)) )
        assert self.a == z, 'Vector equality error.' 
        
        z = Vector(-1.0, -1.0, -1.0)
        VectorTest.logger.info( 'Operation: %s = %s' % (str(self.c), str(z)) )
        assert self.c == z, 'Vector equality error.' 
    
    @log_test(logger, globals.log_seperator)
    def testNotEqual(self):
        z = Vector(-1.0, -1.0, -1.0)
        VectorTest.logger.info( 'Operation: %s = %s' % (str(self.a), str(z)) )
        assert self.a != z, 'Vector inequality error.' 
        
        z = Vector(1.0, 1.0, 1.0)
        VectorTest.logger.info( 'Operation: %s = %s' % (str(self.c), str(z)) )
        assert self.c != z, 'Vector inequality error.' 
    
    @log_test(logger, globals.log_seperator)
    def testAbsoluteValue(self):
        # TODO
        z = Vector(1.0, 1.0, 1.0)
        VectorTest.logger.info( 'Operation: abs( %s )' % (str(self.a)) )
        assert abs(self.a) == z, 'Incorrect vector value: %s' % (str(self.a))
        
        VectorTest.logger.info( 'Operation: abs( %s )' % (str(self.c)) )
        assert abs(self.c) == z, 'Incorrect vector value: %s' % (str(self.c))
    
    @log_test(logger, globals.log_seperator)
    def testGetItem(self):
        VectorTest.logger.info( 'Operation: v[0] on %s' % (str(self.a)) )
        assert self.a[0] == self.a.x, 'Incorrect vector value: %s' % (str(self.a[0]))
        
        VectorTest.logger.info( 'Operation: v[1] on %s' % (str(self.a)) )
        assert self.a[1] == self.a.y, 'Incorrect vector value: %s' % (str(self.a[1]))
        
        VectorTest.logger.info( 'Operation: v[2] on %s' % (str(self.a)) )
        assert self.a[2] == self.a.z, 'Incorrect vector value: %s' % (str(self.a[2]))
        
        self.assertRaises(IndexError, Vector.__getitem__, self.a, 4)
    
    @log_test(logger, globals.log_seperator)
    def testSetItem(self):
        z = Vector()
        VectorTest.logger.info( 'Operation: v[0] = %s' % (str(self.a.x)) )
        z[0] = self.a.x
        assert z[0] == self.a.x, 'Incorrect vector value: %s' % (str(z[0]))
        
        VectorTest.logger.info( 'Operation: v[1] = %s' % (str(self.a.y)) )
        z[1] = self.a.y
        assert z[1] == self.a.y, 'Incorrect vector value: %s' % (str(z[1]))
        
        VectorTest.logger.info( 'Operation: v[2] = %s' % (str(self.a.z)) )
        z[2] = self.a.z
        assert z[2] == self.a.z, 'Incorrect vector value: %s' % (str(z[2]))
        
        self.assertRaises(IndexError, Vector.__setitem__, z, 4, 1.0)
    
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
   
   
   