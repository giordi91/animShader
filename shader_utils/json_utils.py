"""
This module holds some utilities to work on json files
"""

import json

from maya import cmds

#@todo : replace maya dialog with qt dialog

def save(stuff_to_save=None, path=None):

    '''
    This procedure saves given data in a json file
    @param[in] stuff_to_save : this is the data you want to save,
    be sure it s json serializable
    @param path : where you want to save the file

    '''
    if not path:
        path = cmds.fileDialog2(fileMode=0, dialogStyle=1)[0]

    to_be_saved = json.dumps(stuff_to_save, sort_keys=True, \
                    ensure_ascii=True, indent=2)
    opened_file = open(path, 'w')
    opened_file .write(to_be_saved)
    opened_file .close()

    print "------> file correctly saved here : ", path


def load(path=None):

    '''
    This procedure loads and returns the content of a json file
    @param path:  what file you want to load
    @return : the content of the file
    '''
    if not path:
        path = cmds.fileDialog2(fileMode=1, dialogStyle=1)[0]

    opened_file = open(path)
    data_file = json.load(opened_file)
    opened_file.close()

    return data_file

        