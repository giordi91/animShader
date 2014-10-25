"""
This module holds the definiton for a name attribute
"""

from maya import cmds

from animShader.attributes import named_attr


class NameAttr(named_attr.NamedAttr):
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
        named_attr.NamedAttr.__init__(self, "name", ["str", "unicode"])

    def __set__(self, instance, value):
        """
        This function set the value on the maya object
        @param instance: class, the instance we need to work on
        @param value: the value we want to set
        """
        if not self.check_data_type(value):
            return

        instance.internal_name = cmds.rename(instance.internal_name, value)

    def __get__(self, instance, owner):
        """
        This function is automatically called by the getter
        function of the descriptor and gets the name from the
        maya node
        @param instance: class, the instance we need to work on
        @param owner: the type of the instance
        """
        #TO DO impelemtns it based on the MObject
        return instance.internal_name


class NameShapeAttr(NameAttr):
    """
    @brief attribute that controls the shape name

    This class lets you control the shape name of the object
    compared to the regular transform name
    """
    def __init__(self):
        """
        This is the Constructor
        """
        NameAttr.__init__(self)

    def __set__(self, instance, value):
        """
        This function set the value on the maya shape object
        @param instance: class, the instance we need to work on
        @param value: the value we want to set
        """
        if not self.check_data_type(value):
            return

        shape = cmds.listRelatives ( instance.internal_name,
                                    shapes = 1)
        if not shape:
            return
        else :
            shape = shape[0]
        instance.internal_shape_name = cmds.rename(
                                    shape, 
                                    value)
    def __get__(self, instance,owner):
        """
        This function is automatically called by the getter
        function of the descriptor and gets the name from the
        maya node
        @param instance: class, the instance we need to work on
        @param owner: the type of the instance
        """
        #TO DO impelemtns it based on the MObject
        shape = cmds.listRelatives ( instance.internal_name,
                                    shapes = 1)
        if shape:
            return shape[0]
