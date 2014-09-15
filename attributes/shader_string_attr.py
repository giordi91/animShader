"""
This module holds the implementaion for a string attribute
"""
from maya import cmds

from attributes import shader_attr


class String_attr(shader_attr.Attribute):
    """
    @brief Class that controls a string attribute
    """
    def __init__(self, attribute_name):
        """
        Constructor
        @param attribute_name: str, the maya attribute we want to control
        """
        shader_attr.Attribute.__init__(self, attribute_name, "str")

    def set_value(self, instance, value):
        """
        This function set the value on the maya shader
        """
        cmds.setAttr(instance.name + "." + self.attribute_name, \
            value, type="string")

    def get_value(self, instance):
        """
        This function is automatically called by the getter
        function of the descriptor and returns the attribute value
        """
        return cmds.getAttr(instance.name + "." + self.attribute_name)
