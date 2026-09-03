import json

config_path = 'config/options.json'

def fetchoptions() -> list:
    filedata = open(config_path, 'r')
    arr = json.loads(filedata.read())

    return arr