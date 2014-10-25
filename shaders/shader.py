"""
This module contains the declaration of an abstract shader class
"""
import inspect

from maya import cmds

from animShader.attributes import name_attr
from animShader.shader_utils import json_utils
from animShader.shader_utils import node_utils

from storable_class import st_class
from storable_class import st_attribute

class Shader(st_class.StorableClass):
    """
    This is an abstract implementation of  the
    material class
    """
    ##constant identifying the abstract type
    ABSTRACT_TAG = "__ABSTRACT__"
    ##Constant used for the shader type
    SHADER_TYPE = ABSTRACT_TAG
    ##descriptor for interact with the name of the maya node
    name = name_attr.NameAttr()
    def __init__(self, name=None, create_mode = 1):
        """
        The constructor
        @param name: str, the name we want to give to our shader
        @param create_mode: bool, wheter or not to create the shader at init time
        """
        st_class.StorableClass.__init__(self)

        ##Attribute that holds the internalname of the shader, do not use.
        self.internal_name = name
        ##whether or not to create the shader at init time
        self.create_mode = create_mode
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
        if self.create_mode == 0 and self.internal_name != None:
            if not cmds.objExists(self.internal_name):
                OpenMaya.MGlobal.displayError("Shader::create: you are trying to init \
                                the class with a not existing node")
                return
            return

        if self.SHADER_TYPE == self.ABSTRACT_TAG:
            raise ValueError("Please set the SHADER_TYPE in the \
                class, cannot be " + self.ABSTRACT_TAG)
        res = cmds.shadingNode(self.SHADER_TYPE, asShader=1)
        if self.name:
            self.name = cmds.rename(res, self.name)
        else:
            self.name = res