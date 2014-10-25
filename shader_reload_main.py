from animShader import env_config
from animShader.attributes import reload_attributes
from animShader.shader_utils import reload_shader_utils
from animShader.shaders import reload_shaders
from animShader.matcher import reload_matcher
from animShader.shader_look import reload_look
from animShader.light_setup import reload_light_setup

modules = [reload_attributes, reload_shader_utils,
            reload_matcher, reload_shaders,
            reload_look, reload_light_setup]


def reload_it():
    """
    This function reload the imported modules
    """
    reload(env_config)
    print "--> Init reload main"
    for sub_modules in modules:
        reload(sub_modules)
        print "-----> reloading ...",sub_modules

    for sub_modules in modules:
        sub_modules.reload_it()

    print "--> End reload main"


if __name__ == "__builtin__" :
    reload_it()