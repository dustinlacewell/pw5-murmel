
"""the only thing this file needs to have defined is a variable called
tracks, that is a dictionary whose keys are names for track collections
such as 'menu', and whose values are lists of track locations."""
import os

data_py = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.normpath(os.path.join(data_py, '..', 'data'))


sfxpath = os.path.normpath(os.path.join(data_dir, 'sfx'))
musicpath = os.path.normpath(os.path.join(data_dir, 'music'))

tracks = {'menu':[os.path.join(musicpath,filename) for filename in os.listdir(musicpath)
                          if filename.endswith('.ogg')],
          'randomtracks':[]}
