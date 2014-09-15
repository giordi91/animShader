from shader_utils import json_utils
from shader_utils import node_utils

modules = [json_utils, node_utils]


def reload_it():
    """
    This function reload the imported modules
    """
    print "--> Init reload shader_utils"
    for sub_modules in modules:
        reload(sub_modules)
        print "-----> reloading ...",sub_modules

    print "--> End reload shader_utils"