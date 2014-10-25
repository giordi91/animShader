"""
This module contains the declaration of an abstract shader class
"""
from maya import cmds

from animShader.shaders import shader
from animShader.attributes import rgb_attr
from animShader.attributes import numeric_attr
from animShader.attributes import bump2D_attr

class Lambert(shader.Shader):
    """
    This is an implementation of  the
    material Lambert
    """
    ##Constant defining the shader type
    SHADER_TYPE = "lambert"
    ##descriptor for the color attribute
    color = rgb_attr.RgbAttr("color")
    ##descriptor for the transparency attribute
    transparency = rgb_attr.RgbAttr("transparency")
    ##descriptor for the ambientColor attribute
    ambientColor = rgb_attr.RgbAttr("ambientColor")
    ##descriptor for the incandescence attribute
    incandescence = rgb_attr.RgbAttr("incandescence")
    ##descriptor for the diffuse attribute
    diffuse = numeric_attr.NumericAttr("diffuse")
    ##descriptor for the translucence attribute
    translucence = numeric_attr.NumericAttr("translucence")
    ##descriptor for the bump
    bump = bump2D_attr.Bump2DAttr()

    def __init__(self, name=None, create_mode = 1):
        """
        The constructor
        #@param name: str, the name we want to give to our shader
        """
        shader.Shader.__init__(self, name, create_mode)


def get_instance():
    """
    This function returns an instance
    of the class contained in this module
    """
    return Lambert()
