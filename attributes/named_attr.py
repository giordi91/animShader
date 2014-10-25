"""
This module implements an abstract attribute descriptor
"""
from storable_class import st_attribute
class NamedAttr(st_attribute.TypedAttr):
    """
    @brief This class implements an abstract attribute

    The attribute is a basic component added to the class,
    this attribute requires an attribute name which is the
    corresponding maya attribute on the node

    """
    def __init__(self, attribute_name, data_type):
        """
        Constructor
        @param attribute_name: str, the maya attribute we want to control
        @param data_type: str,list : the supported data for this attribute
        """
        ##The data type of the constructor
        self.data_type = data_type
        ##The Maya attribute hooked up to the descriptor
        self.attribute_name = attribute_name