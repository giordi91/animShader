from attributes import shader_attr
from attributes import shader_float3_attr
from attributes import shader_numeric_attr
from attributes import shader_rgb_attr
from attributes import shader_string_attr
from attributes import shader_generic_attr
from attributes import shader_name_attr

modules = [shader_attr, shader_float3_attr, shader_numeric_attr,
            shader_rgb_attr, shader_string_attr,shader_generic_attr,
            shader_name_attr]



def reload_it():
    """
    This function reload the imported modules
    """
    print "---> Init reload attributes"
    for sub_modules in modules:
        reload(sub_modules)
        print "-----> reloading ...",sub_modules

    print "---> End reload attributes"
