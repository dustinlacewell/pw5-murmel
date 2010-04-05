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
__version__ = "$Revision: 113 $"
__date__ = "$Date: 2007-09-07 16:07:35 -0500 (Fri, 07 Sep 2007) $"
__license__ = "see readme.txt"
__copyright__ = "DR0ID (c) 2006-2007"
__url__ = "http://dr0id.ch.vu"
__email__ = "dr0id@bluewin.ch"

#Standard Imports
import math
import os
import random
##import pickle
##import cerealizer
import sys
#Third-Party Imports
import pygame
#Game Imports
import audio, track_config
import data
import eventsystem
import tilemap, tiles
import viewport
import ball
import engine
from states import *
#DEBUG UTILITY
DEBUG = True
def log_call(func):
    def wrapper(*x, **y):
        if DEBUG:
            print "Calling", func.__name__, "from", x[0]
            print "Args:", x, y
        return func(*x, **y)
    return wrapper

data_py = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.normpath(os.path.join(data_py, '..', 'data'))


sfxpath = os.path.normpath(os.path.join(data_dir, 'sfx'))
musicpath = os.path.normpath(os.path.join(data_dir, 'music'))
level_dir = musicpath = os.path.normpath(os.path.join(data_dir, 'levels'))

tracks = {'menu':[os.path.join(musicpath,filename) for filename in os.listdir(musicpath)
                          if filename.endswith('.ogg')],
          'randomtracks':[]}
