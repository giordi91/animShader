"""
This module holds all utilities functions for interactiong with nodes
"""

from maya import cmds

def has_connected_node_type(node, attribute, node_type, source=1):
    """
    This functions check if at the given attribute there is a
    connected node of the given type
    @return: 0 or the corresponding node
    """
    if source == 1:
        nodes = cmds.listConnections(node +'.' +attribute, source=1)
    else:
        nodes = cmds.listConnections(node +'.' +attribute, destination=1)
    if not nodes:
        return 0

    for sub_node in nodes:
        n_type = cmds.nodeType(sub_node)
        if n_type == node_type:
            return sub_node

    return 0
