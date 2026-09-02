import json

config_path = 'config/options.json'

def readoptions() -> list:
    filedata = open(config_path, 'r')
    arr = json.loads(filedata.read())

    return arr