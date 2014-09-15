"""
This module implements holds the declaration of
a float3 attribute
"""
from maya import cmds

from attributes import shader_attr

class Float3_attr(shader_attr.Attribute):
    """
    @brief This attibute implements a float3 attribute
    A float3 attribute is basically a [x, y, z] value.
    and the input value has to be a list of len 3
    """
    def __init__(self, attribute_name):
        """
        Constructor
        @param attribute_name: str, the maya attribute we want to control
        """
        shader_attr.Attribute.__init__(self, attribute_name, "list")

    def set_value(self, instance, value):
        """
        This function set the value on the maya shader
        """
        #check data
        if not self.check_data_type(value):
            return
        #set the value
        cmds.setAttr(instance.name + "." + self.attribute_name, \
             value[0],value[1],value[2] )

    def get_value(self, instance):
        """
        This function get the value on the maya shader
        """
        #get the value
        return list(cmds.getAttr(instance.name + "." + self.attribute_name)[0])

    def check_data_type(self, value):
        """
        This function checks that the input data is valid
        @param value: the value to test
        @return bool
        """
        #check the regular data if is a list
        if not shader_attr.Attribute.check_data_type(self, value):
            return 0
        #then lets check if the list has correct len
        if len(value) != 3:
            raise ValueError("Attribute : excpected list of len 3")
        else:
            return 1
