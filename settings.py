import os
import json

def get_settings():
    file_ = open(get_init_path() + "settings/settings","r")
    return json.loads(file_.read())

def get_init_path():
    path = os.getcwd()
    return path+"/"
    # if "C:" in path:
    #     username = (os.popen('echo whoami').read()).replace('\n','')
    #     return "C://Users//{}//pysticky/".format(username)
    # else:
    #     username = (os.popen('echo $USER').read()).replace('\n','')
    #     return "/home/{}/pysticky/".format(username)
    
def get_path():
    if get_settings()['path']:
        return get_settings()['path']#+"/notes"
    return get_init_path()#+"/notes"

def get_notes_path():
    return get_path()+"notes/"

def set_path(path):
    dict_ = get_settings()
    dict_["path"] = path
    file_ = open(get_init_path() + "settings/settings","w")
    file_.write(json.dumps(dict_))
    file_.close()
    # print(path)

def get_files():
    print(get_notes_path())
    return os.listdir(get_notes_path())

def set_transparency(transparency):
    dict_ = get_settings()
    dict_["transparency"] = transparency
    file_ = open(get_init_path() + "settings/settings","w")
    file_.write(json.dumps(dict_))
    file_.close()
    # return get_settings()["transparency"]

def get_transparency():
    #return 50
    return get_settings()["transparency"]

def get_background():
    #return "rgba(100,100,100,{})".format(get_transparency())
    return "rgba({},{})".format(get_settings()["background"],int((float(get_transparency())/100)*255))
    
def set_background(color):
    dict_ = get_settings()
    dict_["background"] = color
    file_ = open(get_init_path() + "settings/settings","w")
    file_.write(json.dumps(dict_))
    file_.close()

def get_text_color():
    #return "rgb(255,255,255)"
    return get_settings()["text_color"]

def set_text_color(color):
    dict_ = get_settings()
    dict_["text_color"] = color
    file_ = open(get_init_path() + "settings/settings","w")
    file_.write(json.dumps(dict_))
    file_.close()
