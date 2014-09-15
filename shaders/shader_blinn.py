"""
This module contains the declaration a blin attribute
"""
from maya import cmds

from shaders import shader_lambert
from attributes import shader_rgb_attr
from attributes import shader_numeric_attr
from attributes import shader_attr

class Blinn(shader_lambert.Lambert):
    """
    This is an implementation of  the
    material Lambert
    """
    ##Constant defining the attribute type
    SHADER_TYPE = "blinn"
    ##descriptor for the eccenticty attribute
    eccentricity = shader_numeric_attr.Numeric_attr("eccentricity")
    ##descriptor for the specular roll off
    specularRollOff = shader_numeric_attr.Numeric_attr("specularRollOff")
    ##descriptor for the reflectivity
    reflectivity = shader_numeric_attr.Numeric_attr("reflectivity")
    ##descriptor for the specular color
    specularColor = shader_rgb_attr.Rgb_attr("specularColor")
    ##descriptor for the reflected color
    reflectedColor = shader_rgb_attr.Rgb_attr("reflectedColor")

    def __init__(self, name=None):
        """
        The constructor
        @param name: str, the name we want to give to our shader
        """
        shader_lambert.Lambert.__init__(self, name)

def get_instance():
    """
    This function returns an instance
    of the class contained in this module
    """
    return Blinn()
