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
__version__ = "$Revision: 110 $"
__date__ = "$Date: 2007-09-07 14:30:37 -0500 (Fri, 07 Sep 2007) $"
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

##def rotate_around_point(vector, point, rad_angle):
##    radius = hypot(vector[0], vector[1])
##    return point[0] + radius * cos(rad_angle), \
##           point[1] + radius * sin(rad_angle)
##
##def rotate_point(point, rad_angle):
##    radius = hypot(point[0], point[1])
##    return radius * cos(rad_angle), radius * sin(rad_angle)
    

class ViewPort(object):
    
    def __init__(self, surface, screen_rect, world, world_rect):
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
        self.bgd = pygame.Surface(screen_rect.size)
        self.bgd.fill((0,0,0))
        
        self.world = world
        
        diagonal = hypot(world_rect.width, world_rect.height)+2
        r = pygame.Rect((0,0), (diagonal, diagonal))
        r.center = world_rect.center
        self.world_rect = r
        
        self.angle = 0
        self.delta_angle = 0
        self.x = (1,0)
        self.y = (0,1)
        
        self.spinning = False
        self.fixed_angle = 0
        print "ViewPort init:"
        print "screenrect:", self.screen_rect
        print "world_rect:", self.world_rect
        self._wsurf = pygame.Surface(self.world_rect.size)
        
        
    def draw(self):
        wx, wy = self.world_rect.center
        angle = self.angle+self.delta_angle
        half_view_x = self.half_view_x
        half_view_y = self.half_view_y
        deg_angle = int(round(math.degrees(angle)))%360
        surface_blit = self.surface.blit
        surface_blit(self.bgd, (0,0))
        for spr in self.world.get_at(self.world_rect):
            sprx, spry = spr.rect.center
            rx = sprx - wx
            ry = spry - wy
            radius = hypot(rx, ry)
            spr_angle = atan2(ry, rx)
            rrx = radius * cos(angle + spr_angle) + half_view_x
            rry = radius * sin(angle + spr_angle) + half_view_y
            image, rect = spr.images[deg_angle] # rect center has to be at (0,0)
            surface_blit(image, rect.move(rrx, rry))

        pygame.display.flip()
        
    def draw2(self):
        wx, wy = self.world_rect.center
        angle = self.angle+self.delta_angle
        deg_angle = int(round(math.degrees(angle)))%360
        surface_blit = self.surface.blit
        surface_blit(self.bgd, (0,0))

        radius = hypot(wx, wy)
        origin_angle = atan2(wy, wx)
        originx = self.half_view_x-radius * cos(angle+origin_angle)
        originy = self.half_view_y-radius * sin(angle+origin_angle)
        radius = hypot(1, 0)
        unitx_x = radius * cos(angle)
        unitx_y = radius * sin(angle)
        for spr in self.world.get_at(self.world_rect):
            sprx, spry = spr.rect.center
            image, rect = spr.images[deg_angle]
            surface_blit(image, rect.move(originx+sprx*unitx_x-spry*unitx_y, originy+spry*unitx_x+sprx*unitx_y))
        pygame.display.flip()
        
        
    def draw3(self):
        wx, wy = self.world_rect.center
        angle = self.angle+self.delta_angle
##        deg_angle = int(round(math.degrees(angle)))%360
        surface_blit = self._wsurf.blit
        surface_blit(self.bgd, (0,0))
        
        
####        radius = hypot(wx, wy)
##        origin_angle = atan2(wy, wx)
##        originx = self.half_view_x-radius * cos(angle+origin_angle)
##        originy = self.half_view_y-radius * sin(angle+origin_angle)
##        radius = hypot(1, 0)
##        unitx_x = radius * cos(angle)
##        unitx_y = radius * sin(angle)
        for spr in self.world.get_at(self.world_rect):
            surface_blit(spr.images[0][0], spr.rect)
        img = pygame.transform.rotate(self._wsurf, math.degrees(-angle))
        r = img.get_rect(center=self.world_rect.center)
        self.surface.blit(img, r)
##            sprx, spry = spr.rect.center
##            image, rect = spr.images[deg_angle]
##            surface_blit(image, rect.move(originx+sprx*unitx_x-spry*unitx_y, originy+spry*unitx_x+sprx*unitx_y))
        pygame.display.flip()
        
        
    def handle_mousedown(self, pos, button):
        mx, my = pos
        self.fixed_angle = math.atan2(my-self.half_view_y, mx-self.half_view_x)
        self.spinning = True
        
    def handle_mousemotion(self, pos, rel, buttons, only_last):
        if self.spinning:
            mx, my = pos
            current_angle = math.atan2(my-self.half_view_y, mx-self.half_view_x)
            self.delta_angle = current_angle - self.fixed_angle
        
    def handle_mouseup(self, pos, button):
        self.angle += self.delta_angle
        self.angle %= (2*math.pi)
        self.delta_angle = 0
        self.spinning = False
        
    def handle_keydown(self, unicode, key, mod):
        if key == pygame.K_a:
            self.world_rect.move_ip(5, 0)
        elif key == pygame.K_d:
            self.world_rect.move_ip(-5, 0)
        elif key == pygame.K_s:
            self.world_rect.move_ip(0, -5)
        elif key == pygame.K_w:
            self.world_rect.move_ip(0, 5)