from mymathutils import *

class sphere:
    """A sphere in tridimension space
    Has a color, radius, and center point"""
    def __init__(self, color, radius, center):
        self.color=float(color) #color (greyscale) is a number from 0 to 1 (0 white and 1 black)
        self.radius=float(radius)
        self.center=center #center is a /point/ as defined in mymathutils
        self.type = 'sphere' #temporarily adding a type in order to avoid a more generalized surface class; can removes this later on

class triangle:
    """A triangle in tridimension space
    Has a color and three corner points"""
    def __init__(self, color, p1, p2, p3):
        self.color=float(color)
        self.p1=p1
        self.p2=p2
        self.p3=p3
        self.type = 'triangle'

world = [] #List of all the objects that exist in the 'world'

(eye_x,eye_y,eye_z)=(0,0,200) # eye should be located on the positive z side of 3d space; x=0,y=0 are obvious choices

eye = point(eye_x,eye_y,eye_z) # eye is a /point/ where the sendrays originate from
fileoutput = 'C:/Users/Adam/Ray-Tracer/' # Directory where images will be saved; gonna keep them in the same place as the py files

def main(filename = 'img.pgm', res_factor = 1): # will run automatically when I execute this script
    """Should run automatically due to boilerplate code"""
    myraytest()
    destination = fileoutput + filename
    f = open(destination, 'w')
    f.write('P2 %d %d 255\n' % (res_factor*100, res_factor*100)) # Header contains 'P2', breadth, width, and max color value (255)
    increment = 1.0 / res_factor
    y = -50.0 # starts at -50, goes up by the increment until a total of res_factor*100 passes has been completed (same idea for x)
    while y <= 50 - increment:
        x = -50.0 # same idea as y
        while x <= 50 - increment:
            f.write(str(int(color_at(x, y)))) # color_at will return a double from 0.0 to 255.0 which will get converted into an int, then a string
            f.write('\n') # one pixel per line, left to right, then up to down, all below header
            x = x + increment
        y = y + increment
    f.close() # don't forget to close the file when done!

def color_at(x, y):
    """Finds the amount of light (color from white to black) at the corresponding x,y position of the translucent screen.  A vector is drawn
    from the eye to the x,y position.  Sendray() is called to send that vector further past the screen into the simulated world to see if it
    intersects with a surface.  Sendray returns an intensity between 0 and 1 which is scaled out of 255 in color_at()"""
    (uv_x,uv_y,uv_z) = unit_vector(x - eye.x, y - eye.y, 0 - eye.z) #uses the eye's position and the position of the x,y point to find a unit vector
    return round(sendray(eye, uv_x, uv_y, uv_z) * 255.0)

def sendray (pt, uv_x, uv_y, uv_z):
    """Calls first_hit to determine where the first intersection with a surface is (if no intersection, returns zero for black).  When there is an
    intersection lambert is called to determine what color gets reflected by the object."""
    (surface, intercept) = first_hit(pt, uv_x, uv_y, uv_z)
    if surface:
        return lambert(surface, intercept, uv_x, uv_y, uv_z)
    else:
        return 0.0

def first_hit (pt, uv_x, uv_y, uv_z):
    """Calls intersect for each surface in world; Choose the one that is the closest and returns it (or returns nothing if there is no intersection)"""
    (surface, hit, dist) = (None,None,None)
    for s in world:
        hit2 = intersect(s, pt, uv_x, uv_y, uv_z)
        if hit2:
            dist2 = distance(pt,hit2)
            if dist > dist2 or not dist:
                hit = hit2
                dist = dist2
                surface = s
    return (surface, hit)

def lambert (surface, intercept, uv_x, uv_y, uv_z):
    """Returns the proper color by taking the dot product of the sent ray and the normal of the surface"""
    if surface.type == 'sphere':
        (x_normal,y_normal,z_normal) = surface_normal(surface, intercept)
    if surface.type == 'triangle':
        blah = surface_normal(surface, intercept)
        (x_normal,y_normal,z_normal) = (blah.x,blah.y,blah.z)
    return max(0, x_normal*uv_x + y_normal*uv_y + z_normal*uv_z)

def create_sphere(x, y, z, r, c):
    """Appends the sphere to the world list, given the position (x,y,z), radius, and color"""
    mysphere = sphere(c, r, point(x,y,z))
    world.append(mysphere)
    return mysphere

def create_triangle(p1, p2, p3, c):
    """Appends the triangle to the world list, given the three corner points and the color"""
    mytriangle = triangle(c, p1, p2, p3)
    world.append(mytriangle)
    return mytriangle

def intersect (surface, pt, uv_x, uv_y, uv_z):
    """Determines and calls the proper intersect function for the type of surface that is passed in"""
    if surface.type == 'sphere':
        return sphere_intersect(surface, pt, uv_x, uv_y, uv_z)
    if surface.type == 'triangle':
        return triangle_intersect(surface, pt, uv_x, uv_y, uv_z)

def sphere_intersect (sphere, pt, uv_x, uv_y, uv_z):
    """Given the sphere and the sent ray, determines and returns the point of intersection (if any), favoring the closer intersection"""
    c = sphere.center
    n = minroot(sq(uv_x) + sq(uv_y) + sq (uv_z),
                2.0 * ((pt.x - c.x) * uv_x +
                       (pt.y - c.y) * uv_y +
                       (pt.z - c.z) * uv_z),
                sq(pt.x - c.x) + sq(pt.y - c.y) +
                sq(pt.z - c.z) - sq(sphere.radius))
    if n:
        return point(pt.x + uv_x * n, pt.y + uv_y * n, pt.z + uv_z * n)

def triangle_intersect (triangle, pt, uv_x, uv_y, uv_z):
    """Given the triangle and the sent ray, determines and returns the point of intersection (if any)"""
    dist2plane = dist_to_plane(triangle_normal(triangle),triangle.p1,pt) #Using the triangle's p1 as the point on the plane
    sentray = point(dist2plane*uv_x,dist2plane*uv_y,dist2plane*uv_z) #multiplies unit vector times distance to plane to get a vector
    plane_intercept = point(eye.x+sentray.x,eye.y+sentray.y,eye.z+sentray.z) #point where sent ray intersects triangle's plane
    #Now it is necessary to determine if the point is within the triangle or not
    if inside_triangle(triangle, plane_intercept, sentray):
        return plane_intercept

def inside_triangle(triangle, pt4, sentray):
    """Returns true if the point is within the triangle (pt4 should already be on the same plane)"""
    if triangle_test(triangle.p1,triangle.p2,triangle.p3,pt4,sentray):
        if triangle_test(triangle.p2,triangle.p3,triangle.p1,pt4,sentray):
            if triangle_test(triangle.p3,triangle.p1,triangle.p2,pt4,sentray):
                return True

def triangle_test(p1,p2,p3,p4,sentray):
    p12 = point(p2.x-p1.x,p2.y-p1.y,p2.z-p1.z)
    p13 = point(p3.x-p1.x,p3.y-p1.y,p3.z-p1.z)
    normal = determ(p12,p13)
    if dotprod(sentray,normal) > 0:
        normal.x = -normal.x
        normal.y = -normal.y
        normal.z = -normal.z
    p12perp = determ(p12,normal)
    p12perp_length = magnitude(p12perp.x,p12perp.y,p12perp.z)
    p12perp = point(p12perp.x/p12perp_length,p12perp.y/p12perp_length,p12perp.z/p12perp_length)
    a = distance(p1,p2)
    b = distance(p2,p3)
    c = distance(p3,p1)
    s = (a+b+c)/2 #setup for Heron math
    altitude = (2/a)*sqrt(s*(s-a)*(s-b)*(s-c))
    altitude_vector = point(altitude*p12perp.x,altitude*p12perp.y,altitude*p12perp.z)
    foot = point((p3.x-altitude_vector.x)/2,(p3.y-altitude_vector.y)/2,(p3.z-altitude_vector.z)/2)
    footp3 = point(p3.x-foot.x,p3.y-foot.y,p3.z-foot.z)
    footp4 = point(p4.x-foot.x,p4.y-foot.y,p4.z-foot.z)
    if dotprod(footp3,footp4) > 0:
        return True    

def surface_normal (surface, pt):
    """Determines and calls the proper normal function for the type of surface that is bassed in"""
    if surface.type == 'sphere':
        return sphere_normal(surface,pt)
    if surface.type == 'triangle':
        return triangle_normal(surface)

def sphere_normal(surface, pt):
    c = surface.center
    (vect_x,vect_y,vect_z)=(c.x-pt.x,c.y-pt.y,c.z-pt.z)
    return unit_vector(vect_x,vect_y,vect_z)

def triangle_normal(surface):
    mynormal = normal(surface.p1, surface.p2, surface.p3)
    return point(mynormal.x,mynormal.y,mynormal.z)

def myraytest ():
    world = []
    create_triangle(point(-25,-25,100),point(-25,25,100),point(25,0,100),0.8)

if __name__ == '__main__': #boilerplate code to run main if I execute this script
    main(res_factor=4)
