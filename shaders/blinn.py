"""
This module contains the declaration a blin attribute
"""
from maya import cmds

from animShader.shaders import lambert
from animShader.attributes import rgb_attr
from animShader.attributes import numeric_attr

class Blinn(lambert.Lambert):
    """
    This is an implementation of  the
    material Lambert
    """
    ##Constant defining the shader type
    SHADER_TYPE = "blinn"
    ##descriptor for the eccenticty attribute
    eccentricity = numeric_attr.NumericAttr("eccentricity")
    ##descriptor for the specular roll off
    specularRollOff = numeric_attr.NumericAttr("specularRollOff")
    ##descriptor for the reflectivity
    reflectivity = numeric_attr.NumericAttr("reflectivity")
    ##descriptor for the specular color
    specularColor = rgb_attr.RgbAttr("specularColor")
    ##descriptor for the reflected color
    reflectedColor = rgb_attr.RgbAttr("reflectedColor")

    def __init__(self, name=None, create_mode = 1):
        """
        The constructor
        @param name: str, the name we want to give to our shader
        """
        lambert.Lambert.__init__(self, name, create_mode)

def get_instance():
    """
    This function returns an instance
    of the class contained in this module
    """
    return Blinn()
