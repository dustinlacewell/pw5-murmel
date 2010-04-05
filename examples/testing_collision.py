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
__version__ = "$Revision: 57 $"
__date__ = "$Date: 2007-09-05 20:16:47 -0500 (Wed, 05 Sep 2007) $"
__license__ = "see readme.txt"
__copyright__ = "DR0ID (c) 2006-2007"
__url__ = "http://dr0id.ch.vu"
__email__ = "dr0id@bluewin.ch"

import importme
import pygame
from eventsystem import EventSystem
import collision
import math



class Ball(collision.CCircle):
    
    def __init__(self, radius, pos):
        super(Ball, self).__init__(radius, pos)
        self.dragging = False
        self.image = pygame.Surface((2*radius,)*2).convert()
        self.image.set_colorkey((0,0,0))
        self.image.fill((0,0,0))
        pygame.draw.circle(self.image, (255,0,0), (radius, radius), radius)
        self.vx = 0
        self.vy = 0
        self.gravity = 1
        self.onGround = False
        self.bounciness = 0.9
        
    
    
    def mousedown(self, pos, button):
        self.dragging = True
        self.vx = self.vy = 0
        self.rect.center = pos
        
    def mouseup(self, pos, button):
        self.dragging = False
        
    def mousemotion(self, pos, rel, buttons, only_last):
        if self.dragging:
            self.rect.center = pos
            
    def update(self):
        # ball update
        if not self.dragging:
            self.rect.x += self.vx
            if not self.onGround:
                self.vy += self.gravity
            self.rect.y += self.vy
        else:
            self.vy = 0
            self.onGround = False
        self.crect.center = self.rect.center
        # collision detection
        for square in self.tiles:
            if self.crect.colliderect(square.crect):
                pygame.draw.rect(self.screen, (255,255,0), self.crect, 1)
                pygame.draw.rect(self.screen, (0,255,0), square.crect, 1)
                pygame.draw.rect(self.screen, (0,0,255), square.rect, 1)
                col, norm = collision.collision_function_map[(self.type, square.type)](self, square)
                if col:
                    self.collision_response(norm)
                    square.collision_response((-norm[0], -norm[1]))
##                    self.onGround = True
                    cx, cy = self.rect.center
                    pygame.draw.line(self.screen, (255,255,255), (cx, cy), (cx+100*norm[0], cy+100*norm[1]))
            else:
                self.onGround = False

    def collision_response(self, norm, other = None):
##        self.velocity = self.velocity - (((1 + bounciness) * self.velocity.dot(normal)) * normal)
        self.rect.move_ip((norm[0]*1., norm[1]*1.))
##        self.crect.move_ip((norm[0]*1., norm[1]*1.))
##        self.crect.center = self.rect.center
        if math.hypot(*norm):
            norm = (norm[0]/math.hypot(*norm), norm[1]/math.hypot(*norm))
        
            dot = self.vx*norm[0] + self.vy*norm[1]
            
            self.vx = self.vx - (((1+self.bounciness) * dot) *norm[0])
            self.vy = self.vy - (((1+self.bounciness) * dot) *norm[1])
        else:
            self.onGround = True

class Square(collision.CSquare):
    
    def __init__(self, size, pos):
        super(Square, self).__init__(size, pos)
        self.image = pygame.Surface(size).convert()
        self.image.fill((0,255,0))
        
class Poly(collision.CPoly):
    
    def __init__(self, pointlist, pos, rotation=0, size = (1, 1)):
        # only convex polygons are possible
        super(Poly, self).__init__(pointlist, pos, rotation, size)
        self.image = pygame.Surface(self.rect.size).convert()
        self.image.fill((0,0,0))
        self.image.set_colorkey((0,0,0))
        # move points about half rect so all points are on surface
        vert, normal = self.rotate(0, (self.rect.width/2, self.rect.height/2))
        pygame.draw.polygon(self.image, (255,0,0), vert)
        

running = True
def quitting():
    global running
    running = False

def main():
    pygame.init()
    screen = pygame.display.set_mode((800,600))
    bgd = pygame.Surface((800,600)).convert()
    bgd.fill((0,0,0))
    
    evtsys = EventSystem()
    evtsys.signals['quit'].register(quitting)
    
    ball = Ball(20, (100, 115))
    evtsys.signals['mousemotion'].register(ball.mousemotion)
    evtsys.signals['mousebuttondown'].register(ball.mousedown)
    evtsys.signals['mousebuttonup'].register(ball.mouseup)
    
    tiles = []
    tiles.append(Square((300, 100), (550, 300)))
    
    tiles.append(Square((900, 100), (400, 550)))
    # wrong, concave not possible
##    tiles.append(Poly([(0,0), (300,0), (300,-100), (200,-50), (100, -50), (0,-100) ], (200, 300)))
    
    tiles.append(Poly([(0,0), (100,0), (100, -400)], (720, 450)))
    tiles.append(Poly([(0,0), (100,0), (100, -400)], (200, 250)))
    tiles.append(Poly([(0,0), (100,0), (0, -400)], (70, 450)))
    tiles.append(Poly([(0,0), (0,400), (100, 0)], (70, 150)))
    tiles.append(Poly([(0,0), (100,400), (100, 0)], (720, 150) ))
    tiles.append(Poly([(0,0), (40,-40), (40, -80), (0,-160), (-40, -160), (-80, -120), (-80, -60), (-40, 0)], (350, 150) ))
    
    ball.tiles = tiles
    ball.screen = screen
    fps = []
    clock = pygame.time.Clock()
    global running
    while running:
        clock.tick(100)
        fps.append(clock.get_fps())
        print fps[-1]
        evtsys.update(0,0,0)
        screen.blit(bgd, (0,0))
        # dawing tiles
        for tile in tiles:
            screen.blit(tile.image, tile.rect)
            tile.crect.center = tile.rect.center
            # drawing normals
            cx, cy = tile.rect.center
            for nx, ny in tile.normals:
                pygame.draw.line(screen, (0,(ny*nx*255)%255,255), (cx, cy), (cx+50*nx, cy+50*ny))
        # update ball
        ball.update()
        screen.blit(ball.image, ball.rect)
        # update screen
        pygame.display.flip()

    print "average fps:", sum(fps)/len(fps)
    print "max fps", max(fps)
    print "mmin fps", min(fps)


if __name__=='__main__':
    main()