"""
This module holds the implementaion for a string attribute
"""
from maya import cmds

from animShader.attributes import shape_attr


class StringAttr(shape_attr.ShapeAttr):
    """
    @brief Class that controls a string attribute
    """
    def __init__(self, attribute_name):
        """
        Constructor
        @param attribute_name: str, the maya attribute we want to control
        """
        shape_attr.ShapeAttr.__init__(self, attribute_name, "str")

    def __set__(self, instance, value):
        """
        This function set the value on the maya shader
        """

        name = self.get_node(instance)
        cmds.setAttr(name + "." + self.attribute_name, \
            value, type="string")

    def __get__(self, instance, owner):
        """
        This function is automatically called by the getter
        function of the descriptor and returns the attribute value
        """
        name = self.get_node(instance)
        return cmds.getAttr(name + "." + self.attribute_name)
