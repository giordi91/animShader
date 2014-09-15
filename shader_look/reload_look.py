from shader_look import look

modules = [look]


def reload_it():
    """
    This function reload the imported modules
    """
    print "---> Init reload look"
    for sub_modules in modules:
        reload(sub_modules)
        print "-----> reloading ...",sub_modules

    print "---> End reload look"