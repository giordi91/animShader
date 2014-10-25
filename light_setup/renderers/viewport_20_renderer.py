"""
This module holds a dummy class for the high quality renderer
"""

from animShader.light_setup.renderers import generic_viewport
from animShader.attributes import hardware_rendering_attr
from animShader.attributes import numeric_attr
 

class Viewport20Renderer(generic_viewport.GenericViewport):
    """
    This is a class used as a dummy for a high quality renderer.
    The reason why this class exists is to make the library
    uniform and let space for possible expansion in the future
    """

    ##attribute cvontrolling the on off of the ssao
    ssaoEnable = hardware_rendering_attr.HardwareRenderingAttr("ssaoEnable")
    ##attribute controling the amount of samples of the ssao
    ssaoSamples = hardware_rendering_attr.HardwareRenderingAttr("ssaoSamples")
    ##attribute controlling the on off of the motion blur
    motionBlurEnable = hardware_rendering_attr.HardwareRenderingAttr("motionBlurEnable")
    ##attribute controlling the number of samples for the motion blur
    motionBlurSampleCount = hardware_rendering_attr.HardwareRenderingAttr("motionBlurSampleCount")
    ##attribute controlling the multi sample on off
    multiSampleEnable = hardware_rendering_attr.HardwareRenderingAttr("multiSampleEnable")
    ##attribute controlling the number of sampels for multi samples
    multiSampleCount = hardware_rendering_attr.HardwareRenderingAttr("multiSampleCount")
    ##attribute controlling the on off of the gamma correcction
    gammaCorrectionEnable = hardware_rendering_attr.HardwareRenderingAttr("gammaCorrectionEnable")
    ##attribute ontrolling the amount of the gamma correction
    gammaValue = hardware_rendering_attr.HardwareRenderingAttr("gammaValue")
    
    def __init__(self):
        """
        This is the constructor
        """
        generic_viewport.GenericViewport.__init__(self)


def get_instance():
    """
    This function returns an instance of the renderer
    """
    return Viewport20Renderer()