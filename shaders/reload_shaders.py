from shaders import shader
from shaders import shader_lambert
from shaders import shader_blinn
modules = [shader, shader_lambert, shader_blinn]


def reload_it():
    """
    This function reload the imported modules
    """
    print "--> Init reload shaders"

    for sub_modules in modules:
        reload(sub_modules)
        print "-----> reloading ...",sub_modules

    print "--> End reload main"