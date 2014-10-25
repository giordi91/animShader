"""
This module holds the definition for a shape attribute
"""
from maya import cmds

from animShader.attributes import named_attr

class ShapeAttr(named_attr.NamedAttr):
    """
    @brief attribute for controlling the shape values
    This class is meant to be an attribute that controls a maya object attribute,
    the peculiarity is that in search for the attribute first on the shape of the node
    (if any) then on the transofrm
    """
    def __init__(self , attribute_name, data_type):
        """
        Constructor
        @param attribute_name: str, the maya attribute we want to control
        @param data_type: the type of data this attributes conroll
        """
        named_attr.NamedAttr.__init__(self,attribute_name,
                                    data_type)

    def __set__(self, instance, value):
        """
        This function need to be reimplemented
        to add custom behavior for setting the data
        in the descriptor
        """
        if not self.check_data_type(value):
            return

        name = self.get_node(instance)
        cmds.setAttr(name + "." + self.attribute_name,value)


    def __get__(self, instance, owner):
        """
        This function need to be reimplemented
        to add custom behavior for fetching the data
        in the descriptor
        """
        name = self.get_node(instance)
        return cmds.getAttr(name + "." + self.attribute_name)

    def get_node(self,instance):
        """
        This function returns the node node holding the attribute we need to set,
        precedence given to the shape
        @param instance: the instance of the class we use
        @return: str
        """

        name = instance.name
        shapes = cmds.listRelatives(name, shapes=1)

        if shapes :
            attrs = cmds.listAttr(shapes[0])
            if self.attribute_name in attrs:
                name = shapes[0]


        return name
