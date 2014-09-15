"""
This module holds the definition for a generic descriptor
"""
import weakref


class Generic_attr(object):
    """
    @brief Implements a generic descriptor to be sublclassed
    if needed.
    The use of this descriptor is for dinamically find the
    attributes added to the class
    """
    def __init__(self):
        """
        Constructor
        """
        ##the internal dict holding all the data
        self.data = weakref.WeakKeyDictionary()

    def __get__(self, instance, owner):
        """
        Getter function
        @param instance: class, the instance we need the data of
        @param owner the type class
        """
        return self.data[instance]

    def __set__(self, instance, value):
        """
        Setter function
        @param instance: class, the instance we need the data of
        @param value : the value we need to store
        """
        self.data[instance] = value



