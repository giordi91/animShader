"""
This module holds the declaration of a generic
numeric attribute
"""
from maya import cmds

from animShader.attributes import shape_attr


class NumericAttr(shape_attr.ShapeAttr):
    """
    @brief This class implements a numeric attribute

    This class lets you add to a class a numeric attribute which
    supports
    -# float
    -# int
    -# bool
    """
    def __init__(self , attribute_name):
        """
        Constructor
        @param attribute_name: str, the maya attribute we want to control
        """
        shape_attr.ShapeAttr.__init__(self,attribute_name, ["float", "int","bool"])
