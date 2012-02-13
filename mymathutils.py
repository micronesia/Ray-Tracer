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

def distance (p1, p2):
    """Returns the distance between two points; uses the magnitude function"""
    return magnitude(p1.x-p2.x,p1.y-p2.y,p1.z-p2.z)

def minroot (a, b, c):
    """Returns the lesser of the two solutions to the quadratic formula given ax^2+bx+c=0"""
    if a==0:
        return float(-c)/float(b)
    else:
        discrim = sq(b)-4*a*c
        if discrim >=0:
            x1 = (-b+sqrt(discrim))/(2*a)
            x2 = (-b-sqrt(discrim))/(2*a)
            return min(x1,x2)
