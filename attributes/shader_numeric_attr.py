"""
This module holds the declaration of a generic
numeric attribute
"""
from maya import cmds

from attributes import shader_attr


class Numeric_attr(shader_attr.Attribute):
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
        shader_attr.Attribute.__init__(self,attribute_name, ["float", "int","bool"])

    def set_value(self, instance, value):
        """
        This function set the value on the maya shader
        """
        if not self.check_data_type(value):
            return
        cmds.setAttr(instance.name + "." + self.attribute_name,value)

    def get_value(self, instance):
        """
        This function is automatically called by the getter
        function of the descriptor returns the value of
        the attr
        """
        return cmds.getAttr(instance.name + "." + self.attribute_name)