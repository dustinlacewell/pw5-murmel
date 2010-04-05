#!/usr/bin/env python
#
#
#
#
#

"""
#TODO: documentation!
"""

__author__ = "$Author: dr0iddr0id $"
__version__ = "$Revision: 152 $"
__date__ = "$Date: 2007-09-08 18:13:44 -0500 (Sat, 08 Sep 2007) $"
__license__ = "see readme.txt"
__copyright__ = "DR0ID (c) 2006-2007"
__url__ = "http://dr0id.ch.vu"
__email__ = "dr0id@bluewin.ch"

from data import load_image_rot
import collision
import math


class Tile(object):
    
    def __init__(self, image_name, pos, type=collision.QUAD_TYPE):
        super(Tile, self).__init__()
        self.images = []
        self.angle_deg = 0
        self.image_name = image_name
        self.images = load_image_rot(image_name) #cached loading
        self.rect = self.images[0][0].get_rect(center = pos)
        self.collision_type = type
            
    def get_collision_tile(self):
        if hasattr(self, 'collider'):
            return self.collider
        self.collider = collision.get_instance_of_type(self)
        self.collider.tile = self
        if self.angle_deg:
            vert, normals = self.collider.rotate(math.radians(self.angle_deg))
            self.collider.vertices = vert
            self.collider.normals = normals
        return self.collider
    
    def collision_response(self, tile, ctile, norm, other):
        pass
            
            
class NonCollidingTile(Tile):
    
    def __init__(self, image_name, pos):
        super(NonCollidingTile, self).__init__(image_name, pos)
        
    def get_collision_tile(self):
        return None
    
            
class PolygonTile(Tile):
    
    def __init__(self, image_name, pointlist, pos, angle_deg=0):
        super(PolygonTile, self).__init__(image_name, pos, type=collision.POLY_TYPE)
        self.pointlist = pointlist
        # find angle rounded to int
        self.angle_deg = int(round(angle_deg)%360)
        # shift images to match starting angle
        head = self.images[:self.angle_deg]
        del self.images[:self.angle_deg]
        self.images += head
        
        self.pointlist = pointlist
        self.size = self.images[0][0].get_size()
        
        
        



class Bar(PolygonTile):
    
    def __init__(self, image_name, pos, angle_deg=0):
        pointlist = [(0,0),(100,0),(100,-31),(0,-31)]
        super(Bar, self).__init__(image_name, pointlist, pos, angle_deg)
        
class Coin(Tile):
    
    def __init__(self, image_name, pos):
##        super(Coin, self).__init__(image_name, pos, collision.CIRCLE_TYPE)
        Tile.__init__(self,image_name, pos, collision.CIRCLE_TYPE)



class Circle(Tile):
    
    def __init__(self, image_name, pos):
        super(Circle, self).__init__(image_name, pos, collision.CIRCLE_TYPE)
        

##LeftHillHeigh
##RightHillHeigh
##LargeHill
##LeftHillLow
##RightHillLow
class LeftHillHeigh(PolygonTile):
    
    def __init__(self, image_name, pos, angle_deg=0):
        pointlist = [(0,0), (64,0), (64,-64), (0,-32)]
        super(LeftHillHeigh, self).__init__(image_name, pointlist, pos, angle_deg)


class RightHillHeigh(PolygonTile):
    
    def __init__(self, image_name, pos, angle_deg=0):
        pointlist = [(0,0), (64,0),(64,-32),(0,-64)]
        super(RightHillHeigh, self).__init__(image_name, pointlist, pos, angle_deg)

class LargeHill(PolygonTile):
    
    def __init__(self, image_name, pos, angle_deg=0):
        pointlist = [(0,0), (64,0), (64,-64)]
        super(LargeHill, self).__init__(image_name, pointlist, pos, angle_deg)

class LeftHillLow(PolygonTile):
    
    def __init__(self, image_name, pos, angle_deg=0):
        pointlist = [(0,0), (64,0), (64,-32)]
        super(LeftHillLow, self).__init__(image_name, pointlist, pos, angle_deg)

class RightHillLow(PolygonTile):
    
    def __init__(self, image_name, pos, angle_deg=0):
        pointlist = [(0,0), (64,0), (0,-32)]
        super(RightHillLow, self).__init__(image_name, pointlist, pos, angle_deg)
