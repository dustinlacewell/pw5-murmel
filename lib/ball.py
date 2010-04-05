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
__version__ = "$Revision: 140 $"
__date__ = "$Date: 2007-09-08 11:11:53 -0500 (Sat, 08 Sep 2007) $"
__license__ = "see readme.txt"
__copyright__ = "DR0ID (c) 2006-2007"
__url__ = "http://dr0id.ch.vu"
__email__ = "dr0id@bluewin.ch"

import pygame
import collision
import data
import math
import tiles
from math import cos
from math import sin
from math import hypot
from math import pi
from math import sqrt
from math import degrees
from math import atan2

class Ball(tiles.Tile):
    
    def __init__(self, image_name, pos):
        super(Ball, self).__init__(image_name, pos)
        self.collision_type = collision.CIRCLE_TYPE
        self.old_pos = pos
        self.vx = 0
        self.vy = 0
        self.gravity = 0.03
##        self.onGround = False
        self.debug = False
        self.debug_normals = []
        self.bounciness = 0.3
        self.friction = 0.1
        self.hit_threshold = 0.6725
        
        self.speed_sq = 0
        self.maxspeed = 1.5**2
        self.minspeed = 0.01**2
        
        self.images, self.anim_breaking_imgs = data.load_ball_images()
        self.anim_angle = 0
        self.image = self.images[0][0]
        self.rect = self.image.get_rect(center = self.rect.center)
        self.counter = 0
        self.state = 0

    def get_collision_tile(self):
        coll_tile = super(Ball, self).get_collision_tile()
        self.collider = coll_tile
        self.crect = coll_tile.crect
        self.rect = coll_tile.rect
        print "collision ball builded"
        return coll_tile

    def update(self, angle, dt=20):
        # get direction of gravity
        angle -= pi/2
        gvecx = cos(-angle)
        gvecy = sin(-angle)
        # normal state
        if self.state == 0:
            # for debug
            if self.debug:
                self.debug_normals = []
            else:
                # udpate velocity
                self.vx += gvecx*self.gravity
                self.vy += gvecy*self.gravity
                #Terminal Velocity
                self.speed_sq = self.vx**2+self.vy**2
                if self.speed_sq < self.minspeed:
                    self.vx = 0
                    self.vy = 0
                if self.speed_sq > self.maxspeed:
                    speed = sqrt(self.speed_sq)
                    maxspeed = sqrt(self.maxspeed)
                    self.vx = self.vx/speed * maxspeed
                    self.vy = self.vy/speed * maxspeed
                    self.speed_sq = self.vx**2+self.vy**2
                # update position
                self.rect.x += self.vx*dt
                self.rect.y += self.vy*dt
            # update image
            self.image = self.images[min(int(self.speed_sq/self.maxspeed*100)/5, 19)][0]
            
            # udpate collision rect
            self.crect.center = self.rect.center
            
            # collision detection
            # TODO: implement sweeping?
            for coll_tile in self.world.get_colliders_at(self.rect):
                if self.crect.colliderect(coll_tile.crect):
                    col, norm = collision.collision_function_map[(self.collider.type, coll_tile.type)](self.collider, coll_tile)
                    if col:
                        if self.debug:
                            print norm, coll_tile
                            self.debug_normals.append(norm)

                        self.collision_response(norm, coll_tile)
                        coll_tile.collision_response((-norm[0], -norm[1]), self)
            # save old position
            self.old_pos = self.rect.center
        # playing break animation
        elif self.state==1: 
            self.counter += 1
            icounter = self.counter
            if icounter >= 50:
                self.exit()
            else:
                self.image = pygame.transform.rotozoom(self.anim_breaking_imgs[icounter][0], degrees(-self.anim_angle-angle), 1)
                self.rect = self.image.get_rect(center= self.rect.center)
            

    def collision_response(self, norm, other):
##        print "colliding with", other, other.tile
        
        if isinstance(other.tile, tiles.Coin):
            return
        self.rect.move_ip((norm[0]*1.0, norm[1]*1.0))
        h = hypot(*norm)
        if h:
            norm = (norm[0]/h, norm[1]/h)
        
            dot = self.vx*norm[0] + self.vy*norm[1]
            
            self.vx = self.vx - (((1+self.bounciness) * dot) * norm[0])
            self.vy = self.vy - (((1+self.bounciness) * dot) * norm[1])
            
            tangx = -norm[1]
            tangy = norm[0]
            
            
            friction = (self.speed_sq/self.maxspeed)**2
            
            self.vx = self.vx - (((friction) * dot) * tangx)
            self.vy = self.vy - (((friction) * dot) * tangy)
            
            if abs(dot*dot) >= self.hit_threshold * self.maxspeed:
                self.break_ball(norm)
            
    def break_ball(self, norm):
        self.state = 1
        self.counter = 0
        self.anim_angle = atan2(-norm[1], -norm[0])
        
    def exit(self):
        pass