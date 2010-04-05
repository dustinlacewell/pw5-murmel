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

import cerealizer

class Level(object):
    """
    Container object to be pickled and loaded.
    tile = (name, pos, type, pointlist, angle)
    """
    def __init__(self):
        self.size = (576, 576)
        self.bg = None
        self.tiles = []
        self.ball = None
        
cerealizer.register(Level)
