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
__version__ = "$Revision: 118 $"
__date__ = "$Date: 2007-09-07 18:48:24 -0500 (Fri, 07 Sep 2007) $"
__license__ = "see readme.txt"
__copyright__ = "DR0ID (c) 2006-2007"
__url__ = "http://dr0id.ch.vu"
__email__ = "dr0id@bluewin.ch"

import pygame
import math
from math import cos
from math import sin
from math import hypot
from math import atan2
import data
##def rotate_around_point(vector, point, rad_angle):
##    radius = hypot(vector[0], vector[1])
##    return point[0] + radius * cos(rad_angle), \
##           point[1] + radius * sin(rad_angle)
##
##def rotate_point(point, rad_angle):
##    radius = hypot(point[0], point[1])
##    return radius * cos(rad_angle), radius * sin(rad_angle)

    

class ViewPort(object):
    
    def __init__(self, surface, screen_rect, world, world_rect, bg = None):
        """
        surface: surf to draw on
        screen_rect: rect on screen to drawon
        world: tilemap 
        world_rect: initial position and size to draw 
        """
        super(ViewPort, self).__init__()
        
        self.surface = surface.subsurface(screen_rect)
        self.screen_rect = screen_rect
        self.half_view_x = screen_rect.centerx
        self.half_view_y = screen_rect.centery
        if bg:
            self.bgd = data.load_image(bg)[0]
        else:
            self.bgd = pygame.Surface(screen_rect.size)
            self.bgd.fill((0,0,0))
        
        self.world = world
        
        diagonal = hypot(world_rect.width, world_rect.height)+2
        r = pygame.Rect((0,0), (diagonal, diagonal))
        r.center = world_rect.center
        self.world_rect = r
        
        self._wsurf = pygame.Surface(self.world_rect.size)
    
    def draw(self):
        wx, wy = self.world_rect.center
        half_view_x = self.half_view_x
        half_view_y = self.half_view_y
        
        surface_blit = self.surface.blit
        surface_blit(self.bgd, (0, 0))
        
        for spr in self.world.get_at(self.world_rect):
            sprx, spry = spr.rect.center
            rx = (sprx - wx) + half_view_x
            ry = (spry - wy) + half_view_y
            if spr.angle_deg:
                image, rect = spr.images[0 + spr.angle_deg]
            else:
                image, rect = spr.images[0]
            surface_blit(image, rect.move(rx, ry))
    
    def get_at(self, screen_rect):
        sx, sy = screen_rect.center
        wx, wy = self.world_rect.center
        wpx = sx - self.half_view_x + wx
        wpy = sy - self.half_view_y + wy
        print "view.get_at", screen_rect, wpx, wpy
        screen_rect.center = (wpx, wpy)
        return self.world.get_at(screen_rect)
    
            
class RotatableView(ViewPort):

    def __init__(self, surface, screen_rect, world, world_rect, bg = None):
        super(RotatableView, self).__init__(surface, screen_rect, world, world_rect, bg)
        
        self.angle = 0
        
    def draw_rot(self, ang):
        angle = ang
        deg_angle = int(round(math.degrees(angle)))%360
        
        wx, wy = self.world_rect.center
        half_view_x = self.half_view_x
        half_view_y = self.half_view_y
        
        surface_blit = self.surface.blit
        surface_blit(self.bgd, (0,0))
        
        for spr in self.world.get_at(self.world_rect):                
            sprx, spry = spr.rect.center
            rx = (sprx - wx)
            ry = (spry - wy)
            radius = hypot(rx, ry)
            spr_angle = atan2(ry, rx)
            rrx = radius * cos(angle + spr_angle) + half_view_x
            rry = radius * sin(angle + spr_angle) + half_view_y
            image, rect = spr.images[deg_angle] # rect center has to be at (0,0)
            surface_blit(image, rect.move(rrx, rry))
   
