from animShader.matcher import matcher
from animShader.matcher import set_matcher
from animShader.matcher import wild_card_matcher

modules = [matcher, set_matcher, wild_card_matcher]



def reload_it():
    """
    This function reload the imported modules
    """
    print "---> Init reload matcher"
    for sub_modules in modules:
        reload(sub_modules)
        print "-----> reloading ...",sub_modules

    print "---> End reload matcher"
