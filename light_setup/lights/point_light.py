"""
This module holds the implementation of a 
point light
"""

from animShader.light_setup.lights import light
from animShader.attributes import numeric_attr
from animShader.attributes import float3_attr

class PointLight(light.Light):
    """
    @brief SpotLight class
    """

    ##constant defining the light type
    LIGHT_TYPE = "PointLight"

    #light
    ##attribute for the depth map shadow
    useDepthMapShadows = numeric_attr.NumericAttr("useDepthMapShadows")
    ##attribute for the depth map resolution
    dmapResolution = numeric_attr.NumericAttr("dmapResolution")
    
def get_instance():
    """
    This function returns an instance of the light
    """
    return PointLight()