import json
FILE='incidencias.json'

def load_data():
    try:
        return json.load(open(FILE))
    except:
        return []

def save_data(data):
    json.dump(data, open(FILE,'w'), indent=4)
