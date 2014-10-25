"""
This module holds a basic version of a generic viewport
used as a base for all other viewports
"""
from maya import cmds, OpenMaya

from animShader.attributes import named_attr
from storable_class import st_class


class DisplaystyleAttr(named_attr.NamedAttr):
    """
    This class implement displaystyle_attr used to sett stuff
    like wireframes , shaded etc for the viewport
    """

    ##constand defining what values are accepted by 
    ##this attribute
    SUPPORTED_ATTRS = ["wireframe",
                        "points",
                        "boundingBox",
                        "smoothShaded",
                        "flatShaded"
                        ]
                           
    
    def __init__(self):
        """
        Constructor
        """
        named_attr.NamedAttr.__init__(self,"displayAppearance", ["str","unicode"])

    def __set__(self, instance, value):
        """
        This function set the value on the displayAppearance of the 
        modelpanel
        """
        #usual data check
        if not self.check_data_type(value):
            return

        #get the modelpanel
        model = get_model()
        if not model:
            return

        #check if the value we want to set is actually
        #supported
        if not value in self.SUPPORTED_ATTRS:
            types = ""
            for t in self.SUPPORTED_ATTRS:
                types += "- "
                types += t
                types += " \n"
            OpenMaya.MGlobal.displayWarning("value \"{v}\" ".format(v = value) + \
                    "is not supported \nsupported types : \n" + types)
            return

        #if everything goes well lets sett the value
        cmds.modelEditor(model, displayAppearance=value, e=1)

    def __get__(self, instance):
        """
        This function is automatically called by the getter
        function of the descriptor returns the value of
        the attr
        """
        # return cmds.getAttr(instance.name + "." + self.attribute_name)
         
        model = get_model()
        if not model:
            return

        return cmds.modelEditor( model , q =1 ,displayAppearance=1)


class ModelEditorAttr(named_attr.NamedAttr):
    """
    @brief attribute for modeleditor keys

    This class implement model editor attribute to work
    with the modelEditor command, this attribute can support
    all the bool-argument of the maya command cmds.modeleditor
    For now only a small subset of those attribute has been 
    tested and supported
    Accepted values for this attribute are BOOL only means
    True or False only
    """

    ##constand defining what attribute we can control
    SUPPORTED_ATTRS = ["shadows",
                        "wireframeOnShaded",
                        "displayLights",
                        "displayTextures",
                        ]
            
    def __init__(self,attribute_name):
        """
        Constructor
        @param attribute_name: str, the "attribute" we want to control
        """
        named_attr.NamedAttr.__init__(self,attribute_name, ["bool","str","unicode"])
        
        if not attribute_name in self.SUPPORTED_ATTRS:
            types = ""
            for t in self.SUPPORTED_ATTRS:
                types += "- "
                types += t
                types += " \n"
            OpenMaya.MGlobal.displayError("Model_editor_attr: attribute " \
                                        +attribute_name + " not supported \n" \
                                        + "supported types : \n" + types)
            return



    def __set__(self, instance, value):
        """
        This function set the value on the maya modeleditor
        """
        if not self.check_data_type(value):
            return

        model = get_model()
        if not model:
            return

        data_dict = {self.attribute_name : value}
        cmds.modelEditor( model , e =1 , **data_dict)

    def __get__(self, instance):
        """
        This function is automatically called by the getter
        function of the descriptor returns the value of
        the attr
        """
        # return cmds.getAttr(instance.name + "." + self.attribute_name)
         
        model = get_model()
        if not model:
            return
        data_dict = {self.attribute_name : 1}
        return cmds.modelEditor( model , q =1 , **data_dict)

def get_model():
    """
    This function returns the currently active modelPanel
    @return str
    """
    currPanel = cmds.getPanel(withFocus = 1)
    panelType = cmds.getPanel(to = currPanel)
    if (panelType == "modelPanel"): 
        return currPanel
    else :
        OpenMaya.MGlobal.displayWarning("Could not find an active \
            viewport, plase select one and re-run")
    
class GenericViewport(st_class.StorableClass):
    """
    @brief basic viewport implementation

    This class is used as a base for all the different viewport renderer 
    we want to support, it implements basic controls like wireframeOnShaded,
    displayTextures etc
    """
    ##the dysplay style attribute
    displayStyle = DisplaystyleAttr()
    ##attribute controlling wireframe on shaded
    wireframeOnShaded = ModelEditorAttr("wireframeOnShaded")
    ##attribute controlling the shadows on off
    shadows = ModelEditorAttr("shadows")
    ##attribute controlling the display lights
    displayLights = ModelEditorAttr("displayLights")
    ##attribibute controlling the display of the textures
    displayTextures = ModelEditorAttr("displayTextures")

