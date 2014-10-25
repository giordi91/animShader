"""
This module holds a class definition for a viewport
manipulation class
"""
import inspect

from maya import cmds,mel,OpenMaya, OpenMayaUI

from storable_class import st_manager
from storable_class import st_finder

from animShader import env_config
from animShader.shader_utils import json_utils

class LightSet(st_manager.StorableManager):
    """
    This class lets you manage a light setup 
    and some viewport options
    """

    ##constant definig the available renderers
    RENDERERS = ["base_OpenGL_Renderer",
            "hwRender_OpenGL_Renderer",
            "vp2Renderer"]

    ##constant mapping the class names to their proper renderer names
    RENDERERS_SHORTCUT = {
                            'DefaultRenderer':          RENDERERS[0],
                            'HighQualityRenderer':      RENDERERS[1],
                            'Viewport20Renderer':       RENDERERS[2],

                        }
    ##constant mapping the renderers to their class names
    MAYA_RENDERER_TO_CLASS = {

                                RENDERERS[0] : "DefaultRenderer",
                                RENDERERS[1] : "HighQualityRenderer",
                                RENDERERS[2] : "Viewport20Renderer",
                            }

    ##folders to exclude in the finder
    __folders_to_eclude = []    
    ##files to exclude in the finders
    __files_to_exclude = [  "__init__.py", 
                            "light.py", 
                            "generic_renderer.py"]
    ##constant defining the renderer path
    RENDERERS_PATH = env_config.RENDERERS_PATH
    ##constant defining the lights path
    LIGHTS_PATH = env_config.LIGHTS_PATH

    def __init__(self):
        """
        This is the constructor
        """
        st_manager.StorableManager.__init__(self)


        #setup and config renderer finder
        ##finder in charge to find the renderers
        self.renderer_finder = st_finder.Finder()
        self.renderer_finder.path = self.RENDERERS_PATH
        self.renderer_finder.files_to_exclude = self.__files_to_exclude
        self.renderer_finder.folders_to_eclude = self.__folders_to_eclude

        #setup and config lights finder
        ##finder in charge to find the lights
        self.light_finder = st_finder.Finder()
        self.light_finder.path = self.LIGHTS_PATH
        self.light_finder.files_to_exclude = self.__files_to_exclude
        self.light_finder.folders_to_eclude = self.__folders_to_eclude

        ##forcing the lights and renderers to populate
        self.available_renderers
        self.available_lights

        ##list holding all the lights added
        self.lights = []
        ##privet variable holding the renderer used
        self.__renderer  = None


    @property
    def available_renderers(self):
        """
        Getter property for populating available renderers
        @return list[str]
        """

        return self.renderer_finder.available_files

    @property
    def available_lights(self):
        """
        Getter property for populating available lights
        @return list[str]
        """
        return self.light_finder.available_files

    @property
    def renderer_name(self):
        """
        This function returns the renderer name
        @return str
        """
        curr = OpenMayaUI.M3dView.active3dView()
        return curr.rendererString()

    @property
    def renderer(self):
        """
        Property used to access the renderer
        """
        return self.__renderer



    @renderer.setter
    def renderer(self, value):
        """
        Setter property for the renderer
        @param value: the value needed to be set
        """
        
        #lets check if our value is an istance of a renderer
        #class or a string value
    
        if inspect.isclass(type(value)) == True \
            and type(value).__name__ != "str" \
            and type(value).__name__ != "int":
            self.__set_renderer_by_str(value.__class__.__name__)
            self.__renderer = value

        else:
            if value in self.RENDERERS_SHORTCUT:
                self.__renderer = self.get_renderer_instance(value)
                self.__set_renderer_by_str(value)




    def __set_renderer_by_str(self, value):
        """
        This function sets the active rendere from it s string name
        @param value: str, the name of the rendere
        """
        currPanel = cmds.getPanel(withFocus = 1)
        panelType = cmds.getPanel(to = currPanel)

        if value in self.RENDERERS_SHORTCUT:
            #create the mel command to eval
            cmd = 'setRendererInModelPanel \"{r}\" {cp};'.format(
                r = self.RENDERERS_SHORTCUT[value] , 
                cp = currPanel)
            
            #make sure we have a model panel active
            if (panelType == "modelPanel"):
                mel.eval(cmd)
            else :
                OpenMaya.MGlobal.displayError("In order to set stuff" +
                " on the viewport we need an acive viewport")

        else :
            #print the error
            strSupp = [str(k) for k in self.RENDERERS_SHORTCUT.keys()]
            supp = "\n-" +"\n- ".join(strSupp)
            OpenMaya.MGlobal.displayError("You did not provide a valid " + 
                "renderer name, supported renderer names are :" + 
                " \n {r}".format(r = supp) + 
                " \n got {v}".format(v= type(value).__name__))        

    def get_data(self):
        """
        This function returns all the data of the look ready
        to be saved
        @return list
        """
        to_return = {}
        lightsData = []

        for light in self.lights:
            
            lightsData.append(light.get_data())

        if self.renderer :
            to_return["renderer"] = self.renderer.get_data()
        else :
            to_return["renderer"] = None
        to_return["lights"] = lightsData

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
        self.lights = []


        if data["renderer"]:
            ren = self.get_renderer_instance(data["renderer"]["type"])
            if not ren:
                    raise ValueError("Look::SetData: Could not create the renderer instance")
            ren.set_data(data["renderer"])
            self.renderer = ren

        for light_data in data["lights"]:

            light = self.get_light_instance(light_data["type"])
            if not light:
                    raise ValueError("Look::SetData: Could not create a light instance")
            light.set_data(light_data)
            self.lights.append(light)



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


    def get_light_instance(self, name):
        """
        This function retunrs and instance of a shader
        from its name
        @param name: str, the name of the light we need to return
        """
        if not name in self.light_finder.modules_dict :
            return

        return self.light_finder.modules_dict[name].get_instance()


    def get_renderer_instance(self, name):
        """
        This function retunrs and instance of a matcher
        from its name
        @param name: str, the name of the renderer we need to return
        """

        if not name in self.renderer_finder.modules_dict :
            return
            
        return self.renderer_finder.modules_dict[name].get_instance()
