"""
This module implements a matcher based on a set
"""
from maya import cmds

from matcher import shader_matcher
from attributes import shader_generic_attr


class Set_matcher(shader_matcher.Matcher):
    """
    @brief This matcher is based on a set content
    """
    ##descriptor holding the set_name
    set_name = shader_generic_attr.Generic_attr()

    def __init__(self, set_name=None):
        """
        The constructor
        @param set_name : str, the set we want to work on
        """
        ##the stored name of the set
        self.set_name = set_name

    def get_meshes(self):
        """
        This function finds the metching geometries
        and returns it
        """

        if self.set_name:
            return cmds.sets(self.set_name, q=True)
        return []

def get_instance():
    """
    This function returns an instance
    of the class contained in this module
    """
    return Set_matcher()
