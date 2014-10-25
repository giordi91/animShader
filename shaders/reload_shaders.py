from animShader.shaders import shader
from animShader.shaders import lambert
from animShader.shaders import blinn
modules = [shader, lambert, blinn]


def reload_it():
    """
    This function reload the imported modules
    """
    print "--> Init reload shaders"

    for sub_modules in modules:
        reload(sub_modules)
        print "-----> reloading ...",sub_modules

    print "--> End reload main"