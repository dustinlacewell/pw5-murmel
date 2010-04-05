import importme
import pygame
from pygame.locals import *
import audio
import track_config

ah = audio.AudioHandler(sounddir='../data/sfx', musictracks = track_config.tracks)

pygame.init()
screen = pygame.display.set_mode((640,480))
quittime = False
"""


class Menu(object):
    def __init__(self):
        self.items = []
        self.current = 0
    def add_item(self, text):
        self.items.append(text)
        
    def select_next(self):
        if self.current < len(self.items):
            self.current += 1
    def select_prev(self):
        if self.current > 0:
            self.current -= 1

    def draw_menu(self, coords):
        for x,item in enumerate(self.items):
            temp = font.render(item, 0, (255,255,255))
            arect = temp.get_rect()
            arect.inflate_ip(20,20)
            if x == self.current:
                color = (0,0,255)
            else:
                color = (0,255,0)
            tempsurf = pygame.Surface((arect.width,arect.height))
            arect.move_ip(4,4)
            pygame.draw.rect(tempsurf, color, arect, 4)
            tempsurf.blit(temp,(6,6))
            screen.blit(tempsurf, coords)
            

menu = Menu()
for item in track_config.tracks.keys():
    menu.add_item(item)
"""

#queue up all the tracks in the 'menu' playlist
ah.queue_all_tracks('menu')

#draw a list of the sounds to the screen.

font = pygame.font.Font(None, 30)
w = 20
for x,item in enumerate(ah.get_sounds()):
    temp = font.render(item,0,(255,255,255))
    temp2 = font.render(str(x),0,(255,255,255))
    left = temp.get_width() / 2 - temp2.get_width() / 2
    top = temp.get_height() + 15
    screen.blit(temp, (w, 100))
    screen.blit(temp2, (w+left, 100+top))
    w += temp.get_width() + 15
    

keylist = [K_0,K_1,K_2,K_3,K_4,K_5]
while not quittime:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                raise SystemExit
            elif event.key in keylist:
                x = keylist.index(event.key)
                print "playing sound:"
                print ah.get_sounds()[x]
                ah.play_sound(ah.get_sounds()[x])
    #menu.draw_menu((100,100))
    pygame.display.update()
