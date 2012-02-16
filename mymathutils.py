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

def determ (p1, p2):
    """Returns p1 x p2 where p1 and p2 are points being used as vectors"""
    i = p1.y*p2.z-p2.y*p1.z
    j = p1.z*p2.x-p2.z*p1.x
    k = p1.x*p2.y-p2.x*p1.y
    return point(i, j, k)

def normal (p1, p2, p3):
    """Returns a unit vector of the normal of a triangle"""
    p12 = point(p2.x-p1.x,p2.y-p1.y,p2.z-p1.z)
    p13 = point(p3.x-p1.x,p3.y-p1.y,p3.z-p1.z)
    normal_vector = determ(p12,p13)
    normal_size = magnitude(normal_vector.x, normal_vector.y, normal_vector.z)
    return point(normal_vector.x/normal_size, normal_vector.y/normal_size, normal_vector.z/normal_size)

def dotprod (p1, p2):
    """Returns the dot product of p1 and p2 (points)"""
    return p1.x*p2.x+p1.y*p2.y+p1.z*p2.z

def dist_to_plane (normal_vector, point_on_plane, p4):
    """Returns the distance between a point 'called point' and a plane represented by the point 'point_on_plane' and unit normal vector 'normal'"""
    point_to_plane = point(point_on_plane.x-p4.x, point_on_plane.y-p4.y, point_on_plane.z-p4.z)
    return abs(dotprod(normal_vector, point_to_plane))
