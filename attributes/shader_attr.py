"""
This module implements an abstract attribute descriptor
"""

class Attribute(object):
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

    def __get__(self, instance, owner):
        """
        Getter function of the descriptor,
        a custom set_value function has been piped
        so can be overrided and lets implement
        custom behavior
        """
        return self.get_value(instance)
        #return self.data[instance]

    def __set__(self, instance, value):
        """
        Setter function of the descriptor,
        a custom set_value function has been piped
        so can be overrided and lets implement
        custom behavior
        """
        #check the data type if is corect
        if not self.check_data_type(value):
            return

        #call the custom set_value function
        self.set_value(instance, value)

    def set_value(self, instance, value):
        """
        This function need to be reimplemented
        to add custom behavior for setting the data
        in the descriptor
        """
        raise NotImplementedError()

    def get_value(self, instance):
        """
        This function need to be reimplemented
        to add custom behavior for fetching the data
        in the descriptor
        """
        raise NotImplementedError()

    def check_data_type(self, value):
        """
        This function checks that the input data is valid
        @param value: the value to test
        @return bool
        """
        #since the attribute supports multiple data type
        #we check if the data_type is a list
        if type(self.data_type).__name__ != "list":
            #If not a list we check normally the type
            if type(value).__name__ != self.data_type:
                raise ValueError("Attribute : expected {x} got {y}".format(
                    x=self.data_type, y=type(value).__name__))
            else:
                return 1
        else:
            #if it s a list we check if the type is in the accepted list
            if type(value).__name__ not in self.data_type:
                raise ValueError("Attribute : expected {x} got {y}".format(
                    x=self.data_type, y=type(value).__name__))

            else:
                return 1

