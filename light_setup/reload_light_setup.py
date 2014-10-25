from animShader.light_setup import light_set
from animShader.light_setup.renderers import reload_renderer
from animShader.light_setup.lights import reload_lights

##modules to reload
modules = [light_set,reload_renderer, reload_lights]
##module to kick recursive reload
toKick = [reload_renderer, reload_lights]


def reload_it():
    """
    This function reload the imported modules
    """
    print "---> Init reload light_setup"
    for sub_modules in modules:
        reload(sub_modules)
        print "-----> reloading ...",sub_modules

    for subKick in toKick:
        subKick.reload_it()
    print "---> End reload light_setup"