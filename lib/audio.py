from header import *


class AudioHandler(object):
    """ takes care of playing sound effects."""
    valid_exts = ['.ogg','.wav']
    def __init__(self, sounddir=None, musictracks=None):
        """ if sounddir is overridden, the dictionary mapping
        will be of the form {"filename_without_extension" : sound object}"""
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        self.sounds = {}
        if sounddir:
            for filename in os.listdir(sounddir):
                name, ext = os.path.splitext(filename)
                if ext in AudioHandler.valid_exts:
                    self.add_sound(os.path.join(sounddir, filename))
                    
        self.tracks = musictracks
                
    #def __getitem__(self, itemname):
    #    """ shortcut to return sound object contained in self.sounds[itemname]
    #    """
    #    return self.sounds[itemname]
        
    def play_sound(self, soundname):
        """raises KeyError if soundname is nonexistant."""
        temp = self.sounds[soundname]
        temp.play()
        
    def get_sounds(self):
        return self.sounds.keys()

    def add_sound(self, fullpath, name=None):
        """will load the sound, setting name to filename (minus extension)
           if an appropriate name is not provided."""
        if not name:
            filename = os.path.split(fullpath)[-1]
            name = os.path.splitext(filename)[0]
        self.sounds[name] = pygame.mixer.Sound(fullpath)

    def queue_all_tracks(self, name):
        try:
            random.shuffle(self.tracks[name])
            print "loading track:" +self.tracks[name][0]
            pygame.mixer.music.load(self.tracks[name][0])
            pygame.mixer.music.play()
            for item in self.tracks[name][1:]:
                pygame.mixer.music.queue(item)
                
        except IndexError:
            """if you have no tracks, or name doesn't exist in tracklist,
            we just won't play music."""
            pass
    
    def get_busy(self):
        return pygame.mixer.music.get_busy()
