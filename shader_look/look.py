"""
This module holds the declaration of a model look
"""
import os
import imp

from maya import cmds
from shader_utils import json_utils
import env_config

class Look(object):
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
    __foldersToExclude = []
    __filesToExclude = ["__init__.py", "shader.py", "shader_matcher.py"]

    def __init__(self):
        """
        This is the constructor
        """

        ##Internal data holding all the sublooks
        self.data = []
        ##all the available shaders
        self.__shaders = []
        ##all the available matchers
        self.__matchers = []
        ##mapping of the shaders name to its full path
        self.__shaders_dict = {}
        ##mapping of the matchers to their full pats
        self.__matchers_dict = {}

        ##forcing the shaders and matchers to populate
        self.available_shaders
        self.available_matchers

    @property
    def available_shaders(self):
        """
        Getter property for populating available shaders
        @return list[str]
        """
        self.__shaders_dict = {}
        self.__shaders = []
        self.__check_path(env_config.SHADER_PATH, \
                            self.__shaders,        \
                            self.__shaders_dict)

        return self.__shaders

    @property
    def available_matchers(self):
        """
        Getter property for populating available matchers
        @return list[str]
        """

        self.__matchers_dict = {}
        self.__matchers = []

        #kick the recursion
        self.__check_path(env_config.MATCHER_PATH, \
                            self.__matchers,       \
                            self.__matchers_dict)

        return self.__matchers

    def __check_path(self, path, accumulation_list, accumulation_dict):
        """
        This procedure checks a path for the py files and kicks the recursions
        @param path: str , the path we want to scan
        @param accumulation_list: empty list , in this list we
                                  accumulate the founded moudules
        @param accumulation_dict: empty dict , the dict we use to map the data
        """

        res = os.listdir(path)
        to_return = []
        for sub_res in res:
            if sub_res not in self.__foldersToExclude and \
            os.path.isdir(path + sub_res) == 1:
                self.__check_path(path  + sub_res + "/", \
                    accumulation_list, \
                    accumulation_dict)


            if sub_res.find("py") != -1 and sub_res.find(".pyc") == -1 \
            and sub_res not in self.__filesToExclude:
                if sub_res.find("reload") == -1:
                    to_return.append(sub_res)
                    accumulation_dict[sub_res] = path +"/" + sub_res
        accumulation_list += to_return

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
                sub_matcher = self.get_matcher_instance(matcher["type"])[0]
                sub_matcher.set_data(matcher)
                loaded_matchers.append(sub_matcher)
            shader = self.get_shader_instance(sub_look[1]["type"])[0]
            shader.set_data(sub_look[1])

            self.add_sublook(loaded_matchers, shader)

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

    def __get_module_from_string(self, name, dict_mapper):
        """
        This procedure makes an istance of a module from its name
        @param moduleName: str ,the name of the module
        @return: module instance
        """
        module_name = dict_mapper[self.__fix_name(name)]
        module_name = imp.load_source(self.__fix_name(name, 0), \
                    module_name)
        return module_name

    def __fix_name(self, name, add_extension=1):
        """
        This procedure converts the given module name in a way that is suitable
        for the instancing
        @param moduleName: str ,the name of the module
        @param addExtension: bool , whether or not to add the ".py" at the end
        @return: str
        """

        val = "shader_" +name[0].lower() + name[1:]
        if add_extension == 1:
            val += ".py"

        return val

    def __get_instance_from_str(self, name, dict_mapper):
        """
        This procedure returns a class instance from the given string
        @param moduleName: str ,the name of the module
        """

        module = self.__get_module_from_string(name, dict_mapper)
        instance = module.get_instance()
        return instance, module

    def get_shader_instance(self, name):
        """
        This function retunrs and instance of a shader
        from its name
        """

        return self.__get_instance_from_str(name, self.__shaders_dict)


    def get_matcher_instance(self, name):
        """
        This function retunrs and instance of a matcher
        from its name
        """

        return self.__get_instance_from_str(name, self.__matchers_dict)
