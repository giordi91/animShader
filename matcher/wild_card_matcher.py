"""
This module implements a matcher based on a wild card
"""
from maya import cmds

from animShader.matcher import matcher
from storable_class import st_attribute

class WildCardMatcher(matcher.Matcher):
    """
    @brief This matcher is based on a wild card,
    bewhare this is not a regex parser but uses
    the list method of maya which allows the use
    of wild cards
    """
    ##descriptor holding the expression
    wild_card = st_attribute.GenericAttr()
    def __init__(self, wild_card=None):
        """
        This is the constructor
        @param wild_card : str, the wild card expression we want to use
        """
        ##the store wild car
        self.wild_card = wild_card

    def get_meshes(self):
        """
        This function finds the metching geometries
        and returns it
        """
        if self.wild_card:
            return cmds.ls(self.wild_card)
        return []


def get_instance():
    """
    This function returns an instance
    of the class contained in this module
    """
    return WildCardMatcher()
