from animShader.light_setup.lights import light
from animShader.light_setup.lights import spot_light
from animShader.light_setup.lights import directional_light
from animShader.light_setup.lights import point_light

##modules to be reloaded
modules = [light, spot_light, directional_light, point_light]




def reload_it():
    """
    This function reload the imported modules
    """
    print "---> Init reload lights"
    for sub_modules in modules:
        reload(sub_modules)
        print "-----> reloading ...",sub_modules

    print "---> End reload lights"