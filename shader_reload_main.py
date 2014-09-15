import env_config
from attributes import reload_attributes
from shader_utils import reload_shader_utils
from shaders import reload_shaders
from matcher import reload_matcher
from shader_look import reload_look

modules = [reload_attributes, reload_shader_utils,
            reload_matcher, reload_shaders,
            reload_look]


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
