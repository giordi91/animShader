"""
This module holds a dummy class for the high quality renderer
"""
from animShader.light_setup.renderers import generic_viewport

class HighQualityRenderer(generic_viewport.GenericViewport):
    """
    This is a class used as a dummy for a high quality renderer.
    The reason why this class exists is to make the library
    uniform and let space for possible expansion in the future
    """
    def __init__(self):
        """
        This is the constructor
        """
        generic_viewport.GenericViewport.__init__(self)


def get_instance():
    """
    This function returns an instance of the renderer
    """
    return HighQualityRenderer()