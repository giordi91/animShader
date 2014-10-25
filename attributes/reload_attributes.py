from animShader.attributes import named_attr
from animShader.attributes import shape_attr
from animShader.attributes import float3_attr
from animShader.attributes import numeric_attr
from animShader.attributes import rgb_attr
from animShader.attributes import string_attr
from animShader.attributes import bump2D_attr
from animShader.attributes import name_attr
from animShader.attributes import hardware_rendering_attr

modules = [named_attr, shape_attr,float3_attr, numeric_attr,
            rgb_attr, string_attr,
            bump2D_attr,name_attr, hardware_rendering_attr]



def reload_it():
    """
    This function reload the imported modules
    """
    print "---> Init reload attributes"
    for sub_modules in modules:
        reload(sub_modules)
        print "-----> reloading ...",sub_modules

    print "---> End reload attributes"
