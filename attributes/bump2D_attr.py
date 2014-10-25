"""
This module holds the definition of a bump attribute
which needs to be handled a bit differently because
other then file and text placement node needs the bump node
"""

from maya import cmds

from animShader.attributes import named_attr
from animShader.shader_utils import node_utils


class Bump2DAttr(named_attr.NamedAttr):
    """
    @brief implements a color attribute for bump attribute

    This class lets you control the value with a flaot 3 value
    and an input texure, the texure require extra care for implementing
    nodes and stuff
    """
    def __init__(self):
        """
        Constructor
        """
        named_attr.NamedAttr.__init__(self, "normalCamera", \
                                    ["str", "unicode"])

    def __set__(self, instance, value):
        """
        This function set the value on the maya shader,
        this attr needs to handle both list and texture
        @param instance : class, the instance we need to work on
        @param value : str, float3 the value we want to set must 
                    be an rgb like [0,1,0] or a path to a texture
        """
        #check the input data
        if not value:
            return

        if not self.check_data_type(value):
            return


        #now lets handle the more complex case of a path
        file_node,placement ,bump = self.ensure_texture_nodes(instance)
        #set the path on the file node
        cmds.setAttr(file_node + '.fileTextureName', value, type="string")

    def __get__(self, instance, owner):
        """
        This function is automatically called by the getter
        function of the descriptor and gets the name of the
        texture or the value of the color used
        @param instance: class, the instance we need to work on
        @param owner: the type of the instance
        """
        bump_res = node_utils.has_connected_node_type(instance.name, \
                                                self.attribute_name, \
                                                "bump2d")
        if bump_res:

            file_res = node_utils.has_connected_node_type(bump_res, \
                                                "bumpValue", \
                                                "file")

            if file_res:
                return str(cmds.getAttr(file_res + '.fileTextureName'))
        else:
            return None

    def ensure_texture_nodes(self, instance):
        """
        This fucntion makes sure all the needed nodes
        are in place for loading a texture
        @param instance: class, the instance we need to work on
        """
        #check if a file node is connected
        bump_res = node_utils.has_connected_node_type(instance.name, \
                                                self.attribute_name, \
                                                "bump2d")

        if not bump_res:
            #creates the node
            bump_res = cmds.createNode("bump2d", name=instance.name + "_BUMP")
            #lets connect it to the color attribute
            cmds.connectAttr(bump_res + ".outNormal",
                            instance.name +'.' + self.attribute_name)


        file_res = node_utils.has_connected_node_type(bump_res, \
                                                "bumpValue", \
                                                "file")

        #if not we create it
        if not file_res:
            #creates the node
            file_res = cmds.createNode("file", name=instance.name + "_FILE")
            #lets connect it to the color attribute
            cmds.connectAttr(file_res + ".outAlpha",
                            bump_res +'.bumpValue')


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


        return file_res,place_tex_res, bump_res



