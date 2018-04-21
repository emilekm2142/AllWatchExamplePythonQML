import os,base64

import re

def save_image_from_base64(base:str,name:str,extension:str,application:str):
    data = re.sub(r'.*,', '', base)
    path = get_image_path(application)
    print(path)
    fh = open(path, "wb")
   # fh = open(os.path.abspath(path), "wb")
    image = base64.b64decode(data)
    fh.write(image)
    fh.close()
    return path


def get_image_path(application_name: str) -> str:
    path = "Resources/Images/" + application_name + "_" + str(len([os.listdir('./Resources/Images/')]))+".jpg"
    return os.path.abspath(path)

def get_image_name(name:str,extension:str):
    return name+"."+extension
def add_protocol(path):
    return 'file:///'+path
