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
__version__ = "$Revision: 13 $"
__date__ = "$Date: 2007-09-03 13:37:50 -0500 (Mon, 03 Sep 2007) $"
__license__ = "see readme.txt"
__copyright__ = "DR0ID (c) 2006-2007"
__url__ = "http://dr0id.ch.vu"
__email__ = "dr0id@bluewin.ch"

from pygame.event import get as get_events
from pygame.event import wait as wait_for_event
from pygame.event import set_grab
from pygame.constants import QUIT, ACTIVEEVENT, KEYDOWN, KEYUP, MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN, JOYAXISMOTION, JOYBALLMOTION, JOYHATMOTION, JOYBUTTONUP, JOYBUTTONDOWN, VIDEORESIZE, VIDEOEXPOSE, USEREVENT
from pygame.time import get_ticks


class Signal(object):
    
    def __init__(self):
        self._listeners = []
        
    def register(self, listener, prio=None):
        if listener in self._listeners:
            self.unregister(listener)
        if prio and prio < len(self._listeners):
            self._listeners.insert(prio, listener)
        else:
            self._listeners.append(listener)
        
    def unregister(self, listener):
        if listener in self._listeners:
            self._listeners.remove(listener)
            
    def emit(self, *args, **kwargs):
        [listener(*args, **kwargs) for listener in self._listeners]



class EventSystem(object):
    """Class Eventsystem
    """
    def __init__(self):
        super(EventSystem, self).__init__()
        
        # internal data
        self.signals = {}
        self._mousedown_pos = {}
        self._last_click_time = {}
        
        # configurable attributes
        self._click_error = 2 # abs(oldpos-newpos)<= error [pixels]
        self._doubleclick_delay = 200 # time between two clicks [milliseconds]
        
        self._blocking = False
        self._only_last_mousemotion = True
        
        self._wheel_block = True
        self._wheel_button_up = 4
        self._wheel_button_down = 5
        
        # Signal handlers
        #   pygame events
        self.signals['quit'] = Signal()
        self.signals['activeevent'] = Signal()
        self.signals['keydown'] = Signal()
        self.signals['keyup'] = Signal()
        self.signals['mousemotion'] = Signal()
        self.signals['mousebuttondown'] = Signal()
        self.signals['mousebuttonup'] = Signal()
        self.signals['joyaxismotion'] = Signal()
        self.signals['joyballmotion'] = Signal()
        self.signals['joyhatmotion'] = Signal()
        self.signals['joybuttonup'] = Signal()
        self.signals['joybuttondown'] = Signal()
        self.signals['videoresize'] = Signal()
        self.signals['videoexpose'] = Signal()
        self.signals['userevent'] = Signal()
        #   other events
        self.signals['click'] = Signal()
        self.signals['doubleclick'] = Signal()
        self.signals['wheelup'] = Signal()
        self.signals['wheeldown'] = Signal()
        self.signals['render'] = Signal()
        
    def update(self, gdt, gt, rt):
        events = []
        last_mousemotion = None
        
        if self._blocking:
            events = [wait_for_event()]
        else:
            events = get_events()
        
        for event in events:
            
            if event.type == MOUSEMOTION:
            #Emit signature: (pos, rel, buttons, only_last)
                if self._only_last_mousemotion:
                    last_mousemotion = event
                else:
                    self.signals['mousemotion'].emit(event.pos, event.rel, event.buttons, self._only_last_mousemotion)
                
            elif event.type == MOUSEBUTTONUP:
            #Emit signature: (pos, button)
                if not self._wheel_block or event.button not in [self._wheel_button_down, self._wheel_button_up]:
                    self.signals['mousebuttonup'].emit(event.pos, event.button)
                # detect click event
                ex, ey = event.pos
                mx, my = self._mousedown_pos.get(event.button, (-1,-1)) # if up is first
                if (mx > -1 and abs(ex-mx) <= self._click_error and abs(ey-my) <= self._click_error) or not self._wheel_block:
                    # detect double click
                    now = get_ticks()
                    if now - self._last_click_time.get(event.button, 0) < self._doubleclick_delay:
                        self.signals['doubleclick'].emit(event.pos, event.button)
                    else:
                        self.signals['click'].emit(self._mousedown_pos[event.button], event.button)
                        self._last_click_time[event.button] = now
                    
            elif event.type == MOUSEBUTTONDOWN:
            #Emit signature: (pos, button)
                button = event.button
                if not self._wheel_block or button not in [self._wheel_button_down, self._wheel_button_up]:
                    self.signals['mousebuttondown'].emit(event.pos, event.button)
                    # position for click event, see mousebuttonup
                    self._mousedown_pos[event.button] = event.pos
                if button == self._wheel_button_down:
                    self.signals['wheeldown'].emit(event.pos)
                elif button == self._wheel_button_up:
                    self.signals['wheelup'].emit(event.pos)
                    
            elif event.type == KEYDOWN:
            #Emit Signature: (unicode, key, mod)
                self.signals['keydown'].emit(event.unicode, event.key, event.mod)
                
            elif event.type == KEYUP:
            #Emit Signature (key, mod)
                self.signals['keyup'].emit(event.key, event.mod)
                
            elif event.type == JOYAXISMOTION:
            #Emit Signiture: (joy, axis, value)
                self.signals['joyaxismotion'].emit(event.joy, event.axis, event.value)
                
            elif event.type == JOYBALLMOTION:
            #Emit Signature: (joy, ball, rel)
                self.signals['joyballmotion'].emit(event.joy, event.ball, event.rel)
                
            elif event.type == JOYHATMOTION:
            #Emit Signature: (joy, hat, value)
                self.signals['joyhatmotion'].emit(event.joy, event.hat, event.value)
                
            elif event.type == JOYBUTTONUP:
            #Emit Signature: (joy, button)
                self.signals['joybuttonup'].emit(event.joy, event.button)
                
            elif event.type == JOYBUTTONDOWN:
            #Emit Signature: (joy, button)
                self.signals['joybuttondown'].emit(event.joy, event.button)
                
            elif event.type == VIDEORESIZE:
            #Emit Signature: (size, w, h)
                self.signals['videoresize'].emit(event.size, event.w, event.h)
                
            elif event.type == VIDEOEXPOSE:
                self.signals['videoexpose'].emit()
                
            elif event.type == USEREVENT:
                self.signals['userevent'].emit()
                
            elif event.type == QUIT:
                self.signals['quit'].emit()
                
            elif event.type == ACTIVEEVENT:
            #Emit Signature: (gain, state)
                self.signals['activeevent'].emit(event.gain, event.state)
                
        if last_mousemotion:
        #Emit Signature: (pos, rel, only_last)
            event = last_mousemotion
            self.signals['mousemotion'].emit(event.pos, event.rel, event.buttons, self._only_last_mousemotion)
            self._last_mousemotion = None
        
        self.signals['render'].emit()



##    QUIT	     none
##    ACTIVEEVENT	     gain, state
##    KEYDOWN	     unicode, key, mod
##    KEYUP	     key, mod
##    MOUSEMOTION	     pos, rel, buttons
##    MOUSEBUTTONUP    pos, button
##    MOUSEBUTTONDOWN  pos, button
##    JOYAXISMOTION    joy, axis, value
##    JOYBALLMOTION    joy, ball, rel
##    JOYHATMOTION     joy, hat, value
##    JOYBUTTONUP      joy, button
##    JOYBUTTONDOWN    joy, button
##    VIDEORESIZE      size, w, h
##    VIDEOEXPOSE      none
##    USEREVENT        code

