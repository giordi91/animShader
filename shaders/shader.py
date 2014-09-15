"""
This module contains the declaration of an abstract shader class
"""
import inspect

from maya import cmds

from attributes import shader_name_attr
from shader_utils import json_utils
from shader_utils import node_utils
from attributes import shader_attr

class Shader(object):
    """
    This is an abstract implementation of  the
    material class
    """
    ##constant identifying the abstract type
    ABSTRACT_TAG = "__ABSTRACT__"
    ##Constant used for the shader type
    SHADER_TYPE = ABSTRACT_TAG
    ##descriptor for interact with the name of the maya node
    name = shader_name_attr.Name_attr()
    def __init__(self, name=None):
        """
        The constructor
        @param name: str, the name we want to give to our shader
        """
        ##Attribute that holds the internalname of the shader, do not use.
        self.internal_name = name

        self.create()

    #TO DO : implement naming based on MObject

    @property
    def supported_attrs(self):
        """
        This attribute returns the supported attribute for
        the given shader
        """
        return self.get_attrs()

    @property
    def shader_set(self):
        """
        This attributes holds the set associated with the shader
        """

        if not self.internal_name:
            return

        node = node_utils.has_connected_node_type(self.internal_name, \
                                                    "outColor",       \
                                                    "shadingEngine",  \
                                                    0)

        if not node:
            node = cmds.sets(renderable=True, \
                noSurfaceShader=True, empty=1, \
                n=self.internal_name +"SG")
            cmds.connectAttr(self.internal_name + ".outColor",
                             node + '.surfaceShader')
        return node

    def create(self):
        """
        This abstract function is used to create the shader itself
        """
        if self.SHADER_TYPE == self.ABSTRACT_TAG:
            raise ValueError("Please set the SHADER_TYPE in the \
                class, cannot be " + self.ABSTRACT_TAG)
        res = cmds.shadingNode(self.SHADER_TYPE, asShader=1)
        if self.name:
            self.name = cmds.rename(res, self.name)
        else:
            self.name = res

    def get_data(self):
        """
        This fucntions gather all the attribute values of the shader
        and returns it as a dict
        @return dict
        """
        #Find the attribute of the shader
        attrs_to_save = self.get_attrs()
        #Build the dict
        to_return = dict((name, getattr(self, name)) for name in attrs_to_save)
        to_return["type"] = self.__class__.__name__
        return to_return
    def save(self, path=None):
        """
        This function save all the data of a shader and saves it out
        @param path : str, where to save the shader
        """ 
        to_save = self.get_data()
        json_utils.save(to_save, path)

    def set_data(self, data):
        """
        This function sets all the values in the shader class
        @param data: dict, the dict previously generate from a
                     get_data() call
        """
        attrs_to_load = self.get_attrs()
        for name in attrs_to_load:
            setattr(self, name, data[name])

    def load(self, path=None):
        """
        This functions loads all the data in the shader
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
        @param cls: the class instance to work on
        """

        results = [a
                       for b in inspect.getmro(cls)[::-1]
                       for a, v in vars(b).items()
                       if issubclass(type(v), shader_attr.Attribute)]
        return results
