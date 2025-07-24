import json

def write(data, files):
    with open(files, "w") as f:
        json.dump(data, f)

def read(files):
    with open(files, "r") as f:
        return json.load(f)
    