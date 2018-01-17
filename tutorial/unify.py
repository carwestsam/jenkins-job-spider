import os
import json

rootDir = './jobs'
jobs = os.listdir(rootDir)

data = {}

def extract_dir (dir):
    if os.path.isdir(dir):
        print ("is dir", dir)
        obj = {}
        for subdir in os.listdir(dir):
            value = extract_dir(dir + '/' + subdir)
            if subdir.endswith('.json'):
                obj[subdir[:-5]] = value
            else :
                obj[subdir] = value
        return obj

    elif os.path.isfile(dir):
        print ("is file", dir)
        with open(dir, 'r') as f:
            return json.loads("".join(f.readlines()).replace('\n', ''))
    else:
        print ("is others", dir)

with open('data.json', 'wb') as f:
    f.write(json.dumps(extract_dir('./jobs'), indent=2).encode('utf-8'))
