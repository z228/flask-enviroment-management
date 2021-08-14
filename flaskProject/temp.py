import json

with open('properties.json', 'r', encoding='utf-8') as version:
    V = json.load(version)['version']
    for key in V.keys():
        V[key]= V[key][0]
    print(V)
