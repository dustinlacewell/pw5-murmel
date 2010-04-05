'''Simple data loader module.

Loads data files from the "data" directory shipped with a game.

Enhancing this to handle caching etc. is left as an exercise for the reader.
'''

import os

data_py = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.normpath(os.path.join(data_py, '..', 'data/art'))
##data_dir = 'data'

##def filepath(filename):
##    '''Determine the path to a file in the data directory.
##    '''
##    return os.path.join(data_dir, filename)
##
##def load(filename, mode='rb'):
##    '''Open a file in the data directory.
##
##    "mode" is passed as the second arg to open().
##    '''
##    return open(os.path.join(data_dir, filename), mode)

from pygame.image import load
from pygame.transform import rotozoom
from pygame.transform import scale
from pygame import RLEACCEL
from pygame.transform import rotate

rotcache = {} # {name:[]}
cache = {}
def load_image(name, colorkey=(255,0,255)):
    """
    name: it will look it up in data/name (if you want to look for 
    data/tiles/name then you have to pass in tiles/name for name
    """
    global cache
    if name in cache:
        return cache[name]
    image = load(os.path.join(data_dir, name))
    if image.get_alpha():
        image = image.convert_alpha()
    else:
        image = image.convert()
        image.set_colorkey(colorkey, RLEACCEL)
    rect = image.get_rect(center=(0,0))
    sub = cache.setdefault(name, (image, rect))
    return cache[name]
    
def load_image_rot(name, angle=0):
    """
    name: it will look it up in data/name (if you want to look for 
    data/tiles/name then you have to pass in tiles/name for name
    """
    global rotcache
    if name in cache:
        return list(cache[name])
    image = load(os.path.join(os.path.normpath(data_dir), name))
    rect = image.get_rect(center=(0,0))
    sub = []
    sub.append((image.convert_alpha(), rect))
    for angle in range(1, 360):
        rot_image = rotozoom(image, -angle, 1)
        rot_image = rot_image.convert_alpha()
        rect = rot_image.get_rect(center=(0,0))
        sub.append((rot_image, rect))
    cache[name] = sub
    return list(cache[name])
    
def load_ball_images():
    
    colors = []
    for i in range(1,21,1):
        name = '%s%02d.%s'%('ball',i,'png')
        colors.append(load_image(os.path.join('ball',name)))
    breaking = []
    for i in range(1,51,1):
        name = '%s%02d.%s'%('ball_break',i,'png')
        breaking.append(load_image(os.path.join('ball', name)))
    return colors, breaking
        
