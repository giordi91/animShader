"""
This module holds an abstract definition of a matcher
"""
import inspect

from attributes import shader_generic_attr
from shader_utils import json_utils

class Matcher(object):
    """
    @brief This class is an abstract implementation of a matcher

    A matcher is a class in charge to find all the possible mathcing
    meshes needed by the shader, the way in which a mesh is picked or
    not is defined by the matcher itself
    """

    def get_meshes(self):
        """
        This function is the one in charge for
        finding the wanted meshes to associate
        with the matcher
        """

        raise NotImplementedError()

    def get_data(self):
        """
        This fucntions gather all the attribute values of the matcher
        and returns it as a dict
        @return dict
        """
        #Find the attribute of the matcher
        attrs_to_save = self.get_attrs()
        #Build the dict
        to_return = dict((name, getattr(self, name)) for name in attrs_to_save)
        to_return["type"] = self.__class__.__name__
        return to_return

    def save(self, path=None):
        """
        This function save all the data of a matcher and saves it out
        @param path: str, where to save the matcher
        """
        to_save = self.get_data()
        json_utils.save(to_save, path)

    def set_data(self, data):
        """
        This function sets all the values in the matcher class
        @param data: dict, the dict previously generate from a
                     get_data() call
        """
        attrs_to_load = self.get_attrs()
        for name in attrs_to_load:
            setattr(self, name, data[name])

    def load(self, path=None):
        """
        This functions loads all the data in the matcher
        from a json file
        @param path: str, the location of the file to read, if not
                     provided a popup dialog browser will show up
        """
        #read the data from file
        data = json_utils.load(path)
        #set the data in the class
        self.set_data(data)

    @classmethod
    def get_attrs(cls):
        """
        This function is used to scan the class and find all the
        shader_attr in the class, returns a dictonary where
        the key is the name of the attribute and the value
        is the instance of that attribute
        """
        #build the dict
        results = [a
                       for b in inspect.getmro(cls)[::-1]
                       for a, v in vars(b).items()
                       if issubclass(type(v), shader_generic_attr.Generic_attr)]
        return results
