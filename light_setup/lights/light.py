"""
This module holds the most basic definition of light
and all the type of lights should inherit from 
this one
"""
from maya import cmds

from storable_class import st_class
from animShader.attributes import name_attr
from animShader.attributes import numeric_attr
from animShader.attributes import float3_attr
from animShader.attributes import rgb_attr



class Light(st_class.StorableClass):
    """
    This is a basic class for the lights, implements the common attributes
    shared among all the classes
    """
    ##constant identifying the abstract type
    ABSTRACT_TAG = "__ABSTRACT__"
    ##Constant used for the shader type
    LIGHT_TYPE = ABSTRACT_TAG
    ##descriptor for interact with the name of the maya node
    name = name_attr.NameAttr()
    ##attribute for the shape name of the light
    shape_name = name_attr.NameShapeAttr()
    ##attribute controlling the translateX
    translateX = numeric_attr.NumericAttr("translateX")
    ##attribute controlling the translateY
    translateY = numeric_attr.NumericAttr("translateY")
    ##attribute controlling the translateZ
    translateZ = numeric_attr.NumericAttr("translateZ")
    ##attribute controlling the translate
    translate  = float3_attr.Float3Attr("translate")
    ##attribute controlling the rotateX
    rotateX = numeric_attr.NumericAttr("rotateX")
    ##attribute controlling the rotateY
    rotateY = numeric_attr.NumericAttr("rotateY")
    ##attribute controlling the rotateZ
    rotateZ = numeric_attr.NumericAttr("rotateZ")
    ##attribute controlling the rotate
    rotate  = float3_attr.Float3Attr("rotate")
    ##attribute controlling the scaleX
    scaleX = numeric_attr.NumericAttr("scaleX")
    ##attribute controlling the scaleY
    scaleY = numeric_attr.NumericAttr("scaleY")
    ##attribute controlling the scaleZ
    scaleZ = numeric_attr.NumericAttr("scaleZ")
    ##attribute controlling the scale
    scale  = float3_attr.Float3Attr("scale")
    ##attribute controlling the visibility of the light
    visibility = numeric_attr.NumericAttr("visibility")


    #light
    ##attribute controlling the color of the light
    color = rgb_attr.RgbAttr("color")
    ##attribute controlling the intenisty of the light
    intensity = numeric_attr.NumericAttr("intensity")

    ##constant holding the light set
    LIGHT_SET = "defaultLightSet"
    
    def __init__(self, name=None, create_mode = 1):
        """
        The constructor
        @param name: str, the name we want to give to our light
        @param create_mode: bool , whether or not we should create the light at init time or not
        """
        st_class.StorableClass.__init__(self)
        ##Attribute that holds the internalname of the light, do not use.
        self.internal_name = name
        ##attribute holding the internal name of the shape light do not use it.
        self.internal_shape_name = None
        ##attribute holding the value for which we should create the light at init time or not
        self.create_mode = create_mode
        self.create()


    def create(self):
        """
        This abstract function is used to create the shader itself
        """

        if self.create_mode == 0 and self.internal_name != None:
            if not cmds.objExists(self.internal_name):
                OpenMaya.MGlobal.displayError("Light::create: you are trying to init \
                                the class with a not existing node")
                return
            return

        if self.LIGHT_TYPE == self.ABSTRACT_TAG:
            raise ValueError("Please set the LIGHT_TYPE in the \
                class, cannot be " + self.ABSTRACT_TAG)
        res = cmds.createNode(self.LIGHT_TYPE)
        par = cmds.listRelatives(res, parent =1)[0]
        if self.name:
            self.name = cmds.rename(par, self.name)
            # self.shape_name = cmds.rename(res, self.internal_name + "Shape")
        else:
            self.internal_name = par

        self.internal_shape_name = cmds.listRelatives( \
                    self.internal_name, shapes = 1)[0]

        #lets  connect the light to the light set
        indexes = cmds.getAttr(self.LIGHT_SET + '.dagSetMembers',mi = 1)
        idx = 0
        connected = 0
        if not indexes:
            cmds.connectAttr(self.internal_name + '.instObjGroups[0]',
                        self.LIGHT_SET + '.dagSetMembers[0]')
            return

        for i in indexes:
            if i != idx:
                cmds.connectAttr(self.internal_name + '.instObjGroups[0]',
                    self.LIGHT_SET + '.dagSetMembers[{idx}]'.format(idx = idx))
                connected = 1
                break
            idx += 1

        if connected == 0:
            cmds.connectAttr(self.internal_name + '.instObjGroups[0]',
                        self.LIGHT_SET + '.dagSetMembers[{idx}]'.format(idx = indexes[-1]+1))
