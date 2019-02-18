import json
from var import cliente, jsonFile

data = json.load(open(jsonFile))

for cnj in list(data):
    if cnj != 'meta':
        if data[cnj] == 'INDISPONIVEL':
            del data[cnj]

database = json.load(open('files.json'))
database[cliente] = {}
database[cliente] = data

with open('files.json', 'w') as f:
    json.dump(database, f, indent=2)
