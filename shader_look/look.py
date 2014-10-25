"""
This module holds the declaration of a model look
"""
import os
import imp

from maya import cmds
from animShader.shader_utils import json_utils
from animShader import env_config

from storable_class import st_manager
from storable_class import st_finder

class Look(st_manager.StorableManager):
    """
    @brief shader and assignment manager

    This class is in charge to collect all the shaders and the matchers
    used for the assigments.
    You can add sub_look to the class, a sub_look is a combination
    of a metcher list and a shader

    @code
    from matcher import shader_wild_card_matcher
    from matcher import shader_set_matcher
    from shaders import shader_blinn,shader_lambert
    from shader_look import look

    s= shader_blinn.Blinn()
    wm = shader_wild_card_matcher.Wild_card_matcher([
                                                    "*Rim*",
                                                    "*Tire*"
                                                    ])

    wm2 = shader_set_matcher.Set_matcher("dnRenderGeo")

    l = look.Look()
    l.add_sublook([wm2,wm],s)
    l.apply_look()

    @endcode
    """
    __folders_to_eclude = []
    __files_to_exclude = ["__init__.py", "shader.py", "shader_matcher.py"]
    ##constant defining the shader path
    SHADER_PATH = env_config.SHADER_PATH
    ##constand defining the matcher path
    MATCHER_PATH = env_config.MATCHER_PATH

    def __init__(self):
        """
        This is the constructor
        """
        st_manager.StorableManager.__init__(self)

        ##list holding the internal data (sub looks)
        self.data = []

        #setup and config matchers finder
        ##this is the finder used for the matchers
        self.matchers_finder = st_finder.Finder()
        self.matchers_finder.path = self.MATCHER_PATH
        self.matchers_finder.files_to_exclude = self.__files_to_exclude
        self.matchers_finder.folders_to_eclude = self.__folders_to_eclude

        #setup and config matchers finder
        ##this is the finder used for the shaders
        self.shader_finder = st_finder.Finder()
        self.shader_finder.path = self.SHADER_PATH
        self.shader_finder.files_to_exclude = self.__files_to_exclude
        self.shader_finder.folders_to_eclude = self.__folders_to_eclude

        ##forcing the shaders and matchers to populate
        self.available_shaders
        self.available_matchers

    @property
    def available_shaders(self):
        """
        Getter property for populating available shaders
        @return list[str]
        """

        return self.shader_finder.available_files

    @property
    def available_matchers(self):
        """
        Getter property for populating available matchers
        @return list[str]
        """
        return self.matchers_finder.available_files

    def add_sublook(self, matchers, shader):
        """
        This fucntion add a sublook to the final look
        @param matchers: list , the matchers we want to use for
                         the association
        @param shader:  Shader , the shader class to use on the geometries
        """
        self.data.append((matchers, shader))

    def apply_look(self):
        """
        This function loops the sublook and applies them
        """

        for sub_look in self.data:
            #first get all the meshes
            meshes = self.__get_meshes_from_matchers(sub_look[0])
            self.__apply_shader(meshes, sub_look[1])

    def __apply_shader(self, geos, shader):
        """
        This function applies the shader on
        the given meshes
        """

        if not geos:
            return

        for geo in geos:
            cmds.sets(geo, fe=shader.shader_set)

    def __get_meshes_from_matchers(self, matchers):
        """
        This function evaluets the matchers and returns
        the resulting mesh list
        @param matchers: list, matchers array
        @return list
        """

        meshes = []
        for i, matcher in enumerate(matchers):

            if i == 0:
                meshes = matcher.get_meshes()
            else:
                temp = matcher.get_meshes()
                meshes = [mesh for mesh in temp if mesh in meshes]

        return meshes

    def get_data(self):
        """
        This function returns all the data of the look ready
        to be saved
        @return list
        """
        to_return = []
        for matchers, shader in self.data:
            matchers_data = []
            for matcher in matchers:
                matchers_data.append(matcher.get_data())

            to_return.append((matchers_data, shader.get_data()))

        return to_return


    def save(self, path=None):
        """
        This function gets all the data of a look and saves it out
        @param path: str, where to save the shader
        """
        to_save = self.get_data()
        json_utils.save(to_save, path)


    def set_data(self, data):
        """
        This function sets all the values in the shader class
        @param data: dict, the dict previously generate from a
                     get_data() call
        """
        self.data = []

        for sub_look in data:
            loaded_matchers = []
            for matcher in sub_look[0]:

                sub_matcher = self.get_matcher_instance(matcher["type"])
                if not sub_matcher:
                    raise ValueError("Look::SetData: Could not create a matcher instance")
                sub_matcher.set_data(matcher)
                loaded_matchers.append(sub_matcher)
            shader = self.get_shader_instance(sub_look[1]["type"])
            if not shader:
                    raise ValueError("Look::SetData: Could not create a shader instance")
            shader.set_data(sub_look[1])

            self.add_sublook(loaded_matchers, shader)

        self.apply_look()

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


    def get_shader_instance(self, name):
        """
        This function retunrs and instance of a shader
        from its name
        """
        if not name in self.shader_finder.modules_dict :
            return

        return self.shader_finder.modules_dict[name].get_instance()


    def get_matcher_instance(self, name):
        """
        This function retunrs and instance of a matcher
        from its name
        """
        if not name in self.matchers_finder.modules_dict :
            return
            
        return self.matchers_finder.modules_dict[name].get_instance()


