"""
This module holds the definiton for a name attribute
"""

from maya import cmds

from attributes import shader_attr


class Name_attr(shader_attr.Attribute):
    """
    @brief attribute used to control maya node's name

    This class lets you implemente an attribute connected to the
    maya node's name, meaning if you change the value of attribute
    that will be reflected on the maya node's name
    """
    def __init__(self):
        """
        Constructor
        """
        shader_attr.Attribute.__init__(self, "name", ["str", "unicode"])

    def set_value(self, instance, value):
        """
        This function set the value on the maya shader
        """
        instance.internal_name = cmds.rename(instance.internal_name, value)

    def get_value(self, instance):
        """
        This function is automatically called by the getter
        function of the descriptor and gets the name from the
        maya node
        """

        #TO DO impelemtns it based on the MObject
        return instance.internal_name
