
"""the only thing this file needs to have defined is a variable called
tracks, that is a dictionary whose keys are names for track collections
such as 'menu', and whose values are lists of track locations."""
import os

tracks = {'menu':['../data/music/'+filename for filename in os.listdir('../data/music')
                          if filename.endswith('.ogg')],
          'randomtracks':['music/song01.ogg','music/song04.ogg']}
