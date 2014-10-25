"""
This module holds the declaration of an hardware rendering
attribute
"""
from maya import cmds

from animShader.attributes import numeric_attr


class HardwareRenderingAttr(numeric_attr.NumericAttr):
    """
    @brief This class implements an hardware rendering attribute

    This class lets you add to a class an hardware rendering attribute
    which is an attributre on the node hardwareRenderingGlobals,
    used for viewport 2.0
    -# float
    -# int
    -# bool
    """
    def __init__(self , attribute_name):
        """
        Constructor
        @param attribute_name: str, the maya attribute we want to control
        """
        numeric_attr.NumericAttr.__init__(self,attribute_name)

    def __set__(self, instance, value):
        """
        This function set the value on the maya shader
        """
        if not self.check_data_type(value):
            return
        cmds.setAttr(self.__get_node_name() + 
                "." + self.attribute_name,value)

    def __get__(self, instance, owner):
        """
        This function is automatically called by the getter
        function of the descriptor returns the value of
        the attr
        """
        return cmds.getAttr(self.__get_node_name() + 
                "." + self.attribute_name)

    def __get_node_name(sefl):
        """
        This function is in charge to find the hardwareRenderingGlobals,
         node, if not found it will create one
        """

        if not cmds.objExists("hardwareRenderingGlobals"):

            cmds.createNode("hardwareRenderingGlobals" , 
                n = "hardwareRenderingGlobals")

        return "hardwareRenderingGlobals"