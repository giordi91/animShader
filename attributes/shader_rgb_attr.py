"""
This module holds the declaration of an rgb attribute
"""

from maya import cmds

from attributes import shader_attr
from shader_utils import node_utils

class Rgb_attr(shader_attr.Attribute):
    """
    @brief implements a color attribute for both flaot 3 and textures

    This class lets you control the value with a flaot 3 value
    and an input texure, the texure require extra care for implementing
    nodes and stuff
    """
    def __init__(self, attribute_name):
        """
        Constructor
        @param attribute_name: str, the maya attribute we want to control
        """
        shader_attr.Attribute.__init__(self, attribute_name, \
                                    ["str", "unicode", "list"])

        ##The created place2D node
        self.place2D_node = None
        ##The created file node
        self.file_node = None

    def set_value(self, instance, value):
        """
        This function set the value on the maya shader,
        this attr needs to handle both list and texture
        @param instance : class, the instance we need to work on
        @param value : str, float3 the value we want to set must 
                    be an rgb like [0,1,0] or a path to a texture
        """
        #check the input data
        if not self.check_data_type(value):
            return

        #lets first handle the simple case the float3 attribute
        if type(value).__name__ == "list":
            if self.file_node:
                cmds.delete(self.file_node)
                self.file_node = None
                self.place2D_node = None

            #set the value
            cmds.setAttr(instance.name + "." + self.attribute_name, \
                 value[0], value[1], value[2])
            return

        #now lets handle the more complex case of a path
        self.ensure_texture_nodes(instance)
        #set the path on the file node
        cmds.setAttr(self.file_node + '.fileTextureName', value, type="string")

    def get_value(self, instance):
        """
        This function is automatically called by the getter
        function of the descriptor and gets the name of the
        texture or the value of the color used
        @param instance: class, the instance we need to work on
        """
        if self.file_node:
            return str(cmds.getAttr(self.file_node + '.fileTextureName'))
        else:
            return list(cmds.getAttr(instance.name +'.' + self.attribute_name )[0])

    def ensure_texture_nodes(self, instance):
        """
        This fucntion makes sure all the needed nodes
        are in place for loading a texture
        @param instance: class, the instance we need to work on
        """
        #check if a file node is connected
        file_res = node_utils.has_connected_node_type(instance.name, \
                                                self.attribute_name, \
                                                "file")

        #if not we create it
        if not file_res:
            #creates the node
            file_res = cmds.createNode("file", name=instance.name + "_FILE")
            #lets connect it to the color attribute
            cmds.connectAttr(file_res + ".outColor",
                            instance.name +'.' + self.attribute_name)

        #check if the texture placement node is there
        place_tex_res = node_utils.has_connected_node_type(file_res, \
                                                "coverage",          \
                                                "place2dTexture")
        #if not lets create the node
        if not place_tex_res:
            #crate the node
            place_tex_res = cmds.createNode("place2dTexture",\
                name=instance.name + "_2DPlace")

            #connect all the attrbiutes
            for attr in ["coverage", "translateFrame", "rotateFrame",\
                                'mirrorU', "mirrorV", "stagger", \
                                 "wrapU", "wrapV", "repeatUV", \
                                 "offset", "rotateUV", "noiseUV", \
                                 "vertexUvOne", "vertexUvTwo", \
                                 "vertexUvThree", "vertexCameraOne"]:
                cmds.connectAttr(place_tex_res + "." + attr, \
                                file_res + "." + attr)


            cmds.connectAttr(place_tex_res + ".outUV", \
                                file_res + ".uv")

            cmds.connectAttr(place_tex_res + ".outUvFilterSize", \
                                file_res + ".uvFilterSize")
        #store the found node for later used
        self.place2D_node = place_tex_res
        self.file_node = file_res





