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


from viewport import ViewPort
from tilemap import TileMap
from tilemap import Tile
from eventsystem import EventSystem

import pygame


running = True
def quitting():
    global running
    running = False

def main():
    pygame.init()
    screen = pygame.display.set_mode((800,600))
    # set up world
    world = TileMap((10, 10), (32,32))
    # adding tiles
    name1 = 'test_tile1.PNG'
    name2 = 'test_tile2.PNG'
    for x in range(-64, 1280, 32):
        for y in range(0, 1280, 32):
            world.tiles.append(Tile(name1, (x,y)))
            name1, name2 = name2, name1
        name1, name2 = name2, name1
    # setting up eventsytem
    evtsys = EventSystem()
##    evtsys._blocking = True
    # setting up viewport
    view = ViewPort(screen, pygame.Rect(0,0,800,600), world, pygame.Rect(0,0,800,600))
    evtsys.signals['mousemotion'].register(view.handle_mousemotion)
    evtsys.signals['mousebuttondown'].register(view.handle_mousedown)
    evtsys.signals['mousebuttonup'].register(view.handle_mouseup)
    evtsys.signals['keydown'].register(view.handle_keydown)
    # connecting quit event
    evtsys.signals['quit'].register(quitting)
    
##    for tile in world.tiles:
##        screen.blit(tile.images[0][0], tile.rect)
##    pygame.display.flip()
    # main loop
    global running
    clock = pygame.time.Clock()
    fps = []
    while running:
        clock.tick()
        evtsys.update(0,0,0)
        view.drawrot()
        fps.append(clock.get_fps())
    print "average fps:", sum(fps)/len(fps)
    print "min fps:", min(fps)
    print "max fps:", max(fps)
    
    
    
if __name__=='__main__':
    main()