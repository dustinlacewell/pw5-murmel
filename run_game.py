#! /usr/bin/env python

import sys
import os


try:
    __file__
except NameError:
    pass
else:
    libdir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'lib'))
    sys.path.insert(0, libdir)
import header
from states import *
##    from states import HugeRandomLevel
app = engine.Engine(SplashState(), fullscreen=True)
##    app = Engine(HugeRandomLevel)
app.run()
