#  .-------------------------------------------------------------------------.
#  |                                                                         |
#  |                             V E C T O R                                 |
#  |                                                                         |
#  '-------------------------------------------------------------------------'

#  By: Fred Stakem 
#  Date: 7.9.12

# Libraries
from math import *

# Classes

class Vector(object):
    """This is a three dimensional vector class. All basic 3D vector
       operations are included in this class."""
    
    # -----------------------------------------------------------------------
    #       Class Functions
    # -----------------------------------------------------------------------
    # None
    
    
    # -----------------------------------------------------------------------
    #       Instance Functions
    # -----------------------------------------------------------------------
    def __init__(self, *args):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        
        if len(args) == 1:
            if isinstance(args[0], Vector):
                self.x = args[0].x
                self.y = args[0].y
                self.z = args[0].z
            elif isinstance(args[0], (list, tuple)) and len(args[0]) == 3:
                self.x = args[0][0]
                self.y = args[0][1]
                self.z = args[0][2]
        elif len(args) == 3:
            self.x = args[0]
            self.y = args[1]
            self.z = args[2]
                
    def __neg__(self):
        self.x = -self.x
        self.y = -self.y
        self.z = -self.z
        return self
    
    def __pos__(self):
        self.x = +self.x
        self.y = +self.y
        self.z = +self.z
        return self
            
    def __add__(self, vector):
        return Vector(self.x + vector.x,
                      self.y + vector.y,
                      self.z + vector.z)
        
    def __radd__(self, vector):
        return self.__add__(vector)
    
    def __iadd__(self, vector):
        return self.__add__(vector)
        
    def __sub__(self, vector):
        return Vector(self.x - vector.x,
                      self.y - vector.y,
                      self.z - vector.z)
        
    def __rsub__(self, vector):
        return Vector(vector.x - self.x, 
                      vector.y - self.y,
                      vector.z - self.z)
    
    def __isub__(self, vector):
        return self.__sub__(vector)
        
    def __mul__(self, scalar):
        return Vector(self.x * scalar,
                      self.y * scalar,
                      self.z * scalar)
        
    def __rmul__(self, scalar):
        self.__mul__(scalar)
    
    def __imul__(self, scalar):
        self.__mul__(scalar)
        
    def __div__(self, scalar):
        self.__mul__(1.0 / scalar)
        
    def __rdiv__(self, scalar):
        self.__div__(scalar)
    
    def __idiv__(self, scalar):
        self.__div__(scalar)
    
    def __eq__(self, vector):
        if self.x == vector.x and self.y == vector.y and self.z == vector.z:
            return True
        else:
            return False
    
    def __ne__(self, vector):
        if self.x != vector.x or self.y != vector.y or self.z != vector.z:
            return True
        else:
            return False
    
    def __abs__(self):
        return self.__pos__()
    
    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        elif index == 2:
            return self.z
        else:
            raise IndexError('Vector index out of range')
    
    def __setitem__(self, index, value):
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        elif index == 2:
            self.z = value
        else:
            raise IndexError('Vector index out of range')
    
    def __call__(self, *args):
        if len(args) == 1:
            if isinstance(args[0], Vector):
                self.x = args[0].x
                self.y = args[0].y
                self.z = args[0].z
            elif isinstance(args[0], (list, tuple)) and len(args[0]) == 3:
                self.x = args[0][0]
                self.y = args[0][1]
                self.z = args[0][2]
            else:
                raise ValueError('Vector must take a list or Vector if only one argument passed in.')
        elif len(args) == 3:
            self.x = args[0]
            self.y = args[1]
            self.z = args[2]
        else:
            raise ValueError('Vector only takes either 1 or 3 arguments.')
    
    def __str__(self):
        return '(' + str( self.x ) + ", " + str( self.y ) + ", " + str( self.z ) + ')'
    
    def toString(self, start_token, delimiter, end_token):
        return start_token + str( self.x ) + delimiter + str( self.y ) + delimiter + str( self.z ) + end_token 
        
    def distance(self, vector):
        distance = ( vector.x - self.x )**2 + \
                   ( vector.y - self.y )**2 + \
                   ( vector.z - self.z )**2
        return sqrt(distance)
        
    def magnitude(self):
        distance = self.x**2 + self.y**2 + self.z**2
        return sqrt(distance)
    
    def dot(self, vector):
        return self.x * vector.x + self.y * vector.y + self.z * vector.z
    
    def cross(self, vector):
        x = self.y * vector.z - vector.y * self.z
        y = self.z * vector.x - vector.z * self.x
        z = self.x * vector.y - vector.x * self.y
        return Vector(x, y, z)
      
    def normalize(self):
        return Vector(self.x, self.y, self.z) / self.magnitude()
    