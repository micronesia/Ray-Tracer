from math import sqrt

class point:
    """A point in 3D space"""
    def __init__(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

def sq (x):
    """Returns the square of its argument"""
    return x*x

def magnitude(x, y, z):
    """Returns the length of a vector with components x, y, z"""
    return sqrt(sq(x)+sq(y)+sq(z))

def unit_vector (x, y, z):
    """Returns the <x>, <y>, and <z> components of a unit vector with components x, y, and z"""
    vector_magnitude = magnitude(x, y, z)
    return x/vector_magnitude, y/vector_magnitude, z/vector_magnitude
