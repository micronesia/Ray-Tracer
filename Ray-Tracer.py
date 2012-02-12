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








if __name__ == '__main__': #boilerplate code to run main if I execute this script
    main()
