from animShader.light_setup.renderers import generic_viewport
from animShader.light_setup.renderers import default_renderer
from animShader.light_setup.renderers import high_quality_renderer
from animShader.light_setup.renderers import viewport_20_renderer

##mopdules to reload
modules = [
            generic_viewport,
            default_renderer,
            high_quality_renderer,
            viewport_20_renderer
          ]


def reload_it():
    """
    This function reload the imported modules
    """
    print "---> Init reload renderers"
    for sub_modules in modules:
        reload(sub_modules)
        print "-----> reloading ...",sub_modules

    print "---> End reload renderers"