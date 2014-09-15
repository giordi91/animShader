"""
This module implements some env settings
used throught the whole programm
"""

import os
import inspect

ROOT_PATH = os.path.dirname(os.path.abspath( \
    inspect.getfile(inspect.currentframe())))

SHADER_PATH = ROOT_PATH + "/shaders"
ATTRIBUTE_PATH = ROOT_PATH +'/attributes'
MATCHER_PATH = ROOT_PATH +'/matcher'
LOOK_PATH = ROOT_PATH +'/look'
UITLS_PATH = ROOT_PATH +'/utils'


