from header import *      
                
class Engine(object):

    def init_pygame(self, resolution, fs):
        #Pygame initialization
        pygame.init()
        #Font initialization
        self.font = pygame.font.Font(None, 14)
        #Screen resolution
        self.resolution = resolution
        #self.windowFlags = pygame.DOUBLEBUF | pygame.HWSURFACE
        self.windowFlags = 0x00
        if fs: self.windowFlags = self.windowFlags | pygame.FULLSCREEN
        pygame.mouse.set_visible(True)

    def __init__(self, state, fullscreen = False):
        self.init_pygame((800, 600), fs = fullscreen)
        self.evtsystem = eventsystem.EventSystem()
        self.audiosys = audio.AudioHandler(sounddir=track_config.sfxpath, musictracks = track_config.tracks)
        self.statestack = []
        self.firststate = state
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(500,30)

    def register_listeners(self):
        """
        Registers all event handlers for the topmost state.
        """
        global evtsys
        signalmatrix = self.statestack[-1].get_signal_matrix()
        for signal in signalmatrix:
            try:
                self.evtsystem.signals[signal].register(signalmatrix[signal])
            except KeyError:
                print r'Engine: couldn\'t find a "%s" signal for event registration.' % signal

    def unregister_listeners(self):
        """
        Unregisters all event handlers for the topmost state.
        """
        global evtsys
        signalmatrix = self.statestack[-1].get_signal_matrix()
        for signal in signalmatrix:
            try:
                self.evtsystem.signals[signal].unregister(signalmatrix[signal])
            except KeyError:
                print r'Engine: couldn\'t find a "%s" signal for event unregistration.' % signal
                
    def Push(self, state):
        """
        Enter a new State. (Automatic event registration and unregistration)
        """
        if len(self.statestack):
            self.unregister_listeners()
        self.statestack.append(state)
        self.register_listeners()
        self.statestack[-1].enter(self)
        
    def Pop(self, **args):
        """
        Leave current State. (Automatic event registration and unregistration)
        """
        if len(self.statestack):
            self.unregister_listeners()
            self.statestack[-1].leave()
            del self.statestack[-1]
        if len(self.statestack):
            self.register_listeners()
            return True
        return False
    
    def PopAll(self, **args):
        while len(self.statestack): self.Pop()

    def cleanup(self):
        pygame.quit()
        
    def run(self):
        self.screen = pygame.display.set_mode(self.resolution, self.windowFlags)
        state = self.firststate
        self.Push(state)
        
        #Now this is fucking power.
        #TODO: remove fps
        fps = 0
        start_time = pygame.time.get_ticks()
        #Queue music
        self.audiosys.queue_all_tracks('menu')
        #Wait till music starts
        while not self.audiosys.get_busy(): pass
        while len(self.statestack):
            self.clock.tick(60)
            self.evtsystem.update(0, 0, 0)
            pygame.display.flip()
            fps += 1
        end_time = pygame.time.get_ticks()
        print "average fps:", 1000./((end_time-start_time)/fps)
        self.cleanup()

    
if "__main__" == __name__:
    from states import *
##    from states import HugeRandomLevel
    app = Engine(SplashState())
##    app = Engine(HugeRandomLevel)
    app.run()