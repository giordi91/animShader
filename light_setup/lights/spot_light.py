"""
This module holds the implementation of a 
spot light
"""

from animShader.light_setup.lights import light
from animShader.attributes import numeric_attr
from animShader.attributes import float3_attr

class SpotLight(light.Light):
    """
    @brief SpotLight class
    """

    ##constant defining the light type
    LIGHT_TYPE = "spotLight"

    #light
    ##attribute for the depth map shadow
    useDepthMapShadows = numeric_attr.NumericAttr("useDepthMapShadows")
    ##attribute for the depth map resolution
    dmapResolution = numeric_attr.NumericAttr("dmapResolution")
    ##atribute controlling the cone angle of the light
    coneAngle = numeric_attr.NumericAttr("coneAngle")
    ##attribute controlling the penumbra angle of the light
    penumbraAngle = numeric_attr.NumericAttr("penumbraAngle")
    ##attribute used to controll the dropOff
    dropoff = numeric_attr.NumericAttr("dropoff")


def get_instance():
    """
    This function returns an instance of the light
    """
    return SpotLight()