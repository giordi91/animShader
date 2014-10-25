"""
This module holds the implementation of a 
DirectionalLight 
"""

from animShader.light_setup.lights import light
from animShader.attributes import numeric_attr
from animShader.attributes import float3_attr

class DirectionalLight(light.Light):
    """
    @brief DirectionalLight class
    """
    ##constant defining the type of the light
    LIGHT_TYPE = "directionalLight"

    #light
    ##attribute for the depth map shadow
    useDepthMapShadows = numeric_attr.NumericAttr("useDepthMapShadows")
    ##attribute for the depth map resolution
    dmapResolution = numeric_attr.NumericAttr("dmapResolution")
    
def get_instance():
    """
    This function returns an instance of the light
    """
    return DirectionalLight()