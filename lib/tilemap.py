#!/usr/bin/env python
#
#
#
#
#

"""
#TODO: documentation!
"""

__author__ = "$Author: dlacewell $"
__version__ = "$Revision: 98 $"
__date__ = "$Date: 2007-09-06 23:29:56 -0500 (Thu, 06 Sep 2007) $"
__license__ = "see readme.txt"
__copyright__ = "DR0ID (c) 2006-2007"
__url__ = "http://dr0id.ch.vu"
__email__ = "dr0id@bluewin.ch"


from tiles import *


class TileMap(object):
    
    
    
    def __init__(self):
        
        self.size = None
        self.tiles = []
        self.collision_tiles = []
        
        
    def get_at(self, world_rect):
        world_rect_colliderect = world_rect.colliderect
        return [tile for tile in self.tiles if world_rect_colliderect(tile.rect)]
    
    def get_colliders_at(self, rect):
        rect_colliderect = rect.colliderect
        return [tile for tile in self.collision_tiles if rect_colliderect(tile.crect)]
    
    def set_size(self, size, tile_size=(64,64), image_name='default.PNG'):
        self.size = size
        numx = size[0]/tile_size[0]
        numy = size[1]/tile_size[1]
        for x in range(numx+2):
            self.tiles.append(Tile(image_name, (x*tile_size[0]-tile_size[1]/2, -tile_size[1]/2)))
            self.tiles.append(Tile(image_name, (x*tile_size[0]-tile_size[1]/2, size[1]+tile_size[1]/2)))
        for y in range(numy):
            self.tiles.append(Tile(image_name, (-tile_size[0]/2, y*tile_size[1]+tile_size[1]/2)))
            self.tiles.append(Tile(image_name, (size[0]+tile_size[0]/2, y*tile_size[1]+tile_size[1]/2)))
        
        
