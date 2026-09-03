import json

config_path = 'config/options.json'

def collect_options() -> list:
    filedata = open(config_path, 'r')
    arr = json.loads(filedata.read())

    return arr