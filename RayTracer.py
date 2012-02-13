from mymathutils import *

class sphere:
    """A sphere in tridimension space
    Has a color, radius, and center point"""
    def __init__(self, color, radius, center):
        self.color=float(color) #color (greyscale) is a number from 0 to 1 (0 white and 1 black)
        self.radius=float(radius)
        self.center=center #center is a /point/ as defined in mymathutils
        self.type = 'sphere' #temporarily adding a type in order to avoid a more generalized surface class; can removes this later on

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
    (x_normal,y_normal,z_normal) = normal(surface, intercept)
    return max(0, x_normal*uv_x + y_normal*uv_y + z_normal*uv_z)

def create_sphere(x, y, z, r, c):
    """Appends the sphere to the world list, given the position (x,y,z), radius, and color"""
    mysphere = sphere(c, r, point(x,y,z))
    world.append(mysphere)
    return mysphere

def intersect (surface, pt, uv_x, uv_y, uv_z):
    """Determines and calls the proper intersect function for the type of surface that is passed in"""
    if surface.type == 'sphere':
        return sphere_intersect(surface, pt, uv_x, uv_y, uv_z)

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

def normal (surface, pt):
    """Determines and calls the proper normal function for the type of surface that is bassed in"""
    if surface.type == 'sphere':
        return sphere_normal(surface,pt)

def sphere_normal(surface, pt):
    c = surface.center
    (vect_x,vect_y,vect_z)=(c.x-pt.x,c.y-pt.y,c.z-pt.z)
    return unit_vector(vect_x,vect_y,vect_z)

def myraytest ():
    world = []
    create_sphere(0,0,-1200,200,.8)

if __name__ == '__main__': #boilerplate code to run main if I execute this script
    main(res_factor=6)
