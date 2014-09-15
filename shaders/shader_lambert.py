"""
This module contains the declaration of an abstract shader class
"""
from maya import cmds

from shaders import shader
from attributes import shader_rgb_attr
from attributes import shader_numeric_attr

class Lambert(shader.Shader):
    """
    This is an implementation of  the
    material Lambert
    """
    ##Constant defining the attribute type
    SHADER_TYPE = "lambert"
    ##descriptor for the color attribute
    color = shader_rgb_attr.Rgb_attr("color")
    ##descriptor for the transparency attribute
    transparency = shader_rgb_attr.Rgb_attr("transparency")
    ##descriptor for the ambientColor attribute
    ambientColor = shader_rgb_attr.Rgb_attr("ambientColor")
    ##descriptor for the incandescence attribute
    incandescence = shader_rgb_attr.Rgb_attr("incandescence")
    ##descriptor for the diffuse attribute
    diffuse = shader_numeric_attr.Numeric_attr("diffuse")
    ##descriptor for the translucence attribute
    translucence = shader_numeric_attr.Numeric_attr("translucence")


    
    def __init__(self, name=None):
        """
        The constructor
        #@param name: str, the name we want to give to our shader
        """
        shader.Shader.__init__(self, name)


def get_instance():
    """
    This function returns an instance
    of the class contained in this module
    """
    return Lambert()
