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
__version__ = "$Revision: 30 $"
__date__ = "$Date: 2007-09-05 03:17:47 -0500 (Wed, 05 Sep 2007) $"
__license__ = "see readme.txt"
__copyright__ = "DR0ID (c) 2006-2007"
__url__ = "http://dr0id.ch.vu"
__email__ = "dr0id@bluewin.ch"

import importme
import pygame
import sys
import math

def main():
    pygame.display.init()
    screen = pygame.display.set_mode((800,600))
    bgd = pygame.Surface(screen.get_size()).convert()
    bgd.fill((0,0,0))
    
    angle = 0
    dangle = 0
    
    fixed_vecx = 0
    fixed_vecy = 0
    fixed_angle = 0
    
    current_vec_x = 0
    current_vec_y = 0
    current_angle = 0
    
    centerx = 400
    centery = 300
    
    # init stuff
    image = pygame.Surface((800, 600))
    image.fill((255,0,0))
    image.set_colorkey((255,0,255))
    rect = image.get_rect(center=(centerx, centery))
    spinning = False
    dirty = 0
    
    looping = True
    while looping:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               looping = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    looping = False 
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                fixed_vecx = mx-centerx
                fixed_vecy = my-centery
                fixed_angle = math.atan2(fixed_vecy, fixed_vecx)
                spinning = True
            elif event.type == pygame.MOUSEBUTTONUP:
                angle += dangle
                angle %= (2*math.pi)
                dangle = 0
                spinning = False
            elif event.type == pygame.MOUSEMOTION:
                if spinning:
                    mx, my = event.pos
                    current_vec_x = mx-centerx
                    current_vec_y = my-centery
                    current_angle = math.atan2(current_vec_y, current_vec_x)
                    dangle = fixed_angle-current_angle
                    dirty = 1
        rotated_image = pygame.transform.rotate(image, math.degrees(angle+dangle))
        rect = rotated_image.get_rect(center=(centerx, centery))
        screen.blit(rotated_image, rect)
        pygame.draw.line(screen, (255,255,255), (centerx,centery), (centerx+fixed_vecx, centery+fixed_vecy))
        pygame.draw.line(screen, (0,0,255), (centerx,centery), (centerx+current_vec_x, centery+current_vec_y))
        dirty = 0
        # clear screen
        pygame.display.flip()
        screen.blit(bgd, (0,0))
        
    # loop end
    pygame.quit()
                    
if __name__== '__main__':
    main()