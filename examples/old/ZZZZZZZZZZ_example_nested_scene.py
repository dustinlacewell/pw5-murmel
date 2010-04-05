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

import pygame
##from view import View
from entity import Entity
from viewmanager import ViewManager
from eventsystem import EventSystem
##from eventsystem import Signal
from gametime import GameTime
##from simulation import Simulation

current_scene = None
scenes = [] # current_scene[-1] is the current running scene

class Task(object):
    
    def update(self, gdt, gt, rt):
        pass

class TaskRunner(object):
    """
    Class TaskRunner
    """
    
    def __init__(self):
        """
        
        """
        super(TaskRunner, self).__init__()
        # Attributes:
        self._state_stack = None  # ([State]) 
        
        
        self.running = True
        self._tasks = [] # [(prio, instance)]
        self._task_updates = []
        
        self.return_data = None
        
        self.gametime = GameTime()
        

    def _set_denied(self, val):
        raise "task attribute is read only!"
        
    def add_task(self, task, prio, attr_name=None):
        """
        A task is an instance that must have a method called update(gdt, gt, rt).
        They will we run in priority order, smaller prio is excecuted first.
        If two tasks have same prio then it depends on the order you add them.
        If attr_name already exists then it is overridden.
        """
        task_ = (prio, task, attr_name)
        self._tasks.append(task_)
        self._tasks.sort()
        self._task_updates = [task_[1].update for task_ in self._tasks]
        if attr_name:
            setattr(TaskRunner, attr_name, property(lambda self: task, TaskRunner._set_denied))
            
    def remove_task(self, task=None, attr_name=None):
        """
        
        """
        if task:
            idxes =[idx for idx, tas in enumerate(self._tasks) if tas[1]==task]
            dx = 0
            for idx in idxes:
                deltask = self._tasks.pop(idx-dx)
                self._task_updates.pop(idx-dx)
                dx += 1
                if deltask[2]:
                    delattr(TaskRunner, deltask[2])
        elif attr_name:
            self.remove_task(getattr(self, attr_name, None))
        else:
            # TODO: make it a log entry
            import warnings
            warnings.warn("Scene.remove_task: either task or attr_name must be given!")
        
    def init(self, *args, **kwargs):
        """
        To be overridden.
        Called automatically by run() method.
        """
        print "init scene", self, id(self)
        pass
        
        
    def quitting(self):
        """
        To be overridden.
        Called when main loop is left.
        """
        print "quitting scene", self, id(self)
        pass
        
    def run(self, *args, **kwargs):
        """
        The args and kwargs are passe to the init() method.
        """
        global current_scene
        global scenes
        current_scene = self
        scenes.append(self)
        self.init(*args, **kwargs)
        while self.running:
            gdt, gt, rt = self.gametime.update()
            [update(gdt, gt, rt) for update in self._task_updates]
        self.quitting()
        scenes.pop()
        if len(scenes):
            current_scene = scenes[-1]
        else:
            current_scene = None
        return self.return_data



