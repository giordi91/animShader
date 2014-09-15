from matcher import shader_matcher
from matcher import shader_set_matcher
from matcher import shader_wild_card_matcher

modules = [shader_matcher, shader_set_matcher, shader_wild_card_matcher]



def reload_it():
    """
    This function reload the imported modules
    """
    print "---> Init reload matcher"
    for sub_modules in modules:
        reload(sub_modules)
        print "-----> reloading ...",sub_modules

    print "---> End reload matcher"
