"""
This module implements a matcher based on a set
"""
from maya import cmds

from animShader.matcher import matcher
from storable_class import st_attribute


class SetMatcher(matcher.Matcher):
    """
    @brief This matcher is based on a set content
    """
    ##descriptor holding the set_name
    set_name = st_attribute.GenericAttr()

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
    return SetMatcher()
