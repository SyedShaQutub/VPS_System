import mathutils
import math



class Point(object):
    def __init__(self, x=0.0,y=0.0,z=0.0):
        self.x = float(x)
	    self.y = float(y)
        self.z = float(z)
	
    def __repr__(self):
        coord = (self.x,self.y,self.z)
	return coord
	
    def __str__(self):
	point_str = "(%f,%f,%f)" % (self.x, self.y, self.z)
	return point_str