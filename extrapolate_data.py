import json

def bus_choice(scelta):
    f = open("fermate.json")
    fermate = json.load(f)
    searched = None
    for fermata in fermate:
        for k, v in fermata.items():
            if scelta == v:
                searched = fermata
    f.close()
    return searched

def extract_data(stazione):
    return stazione.get('fermataID'), stazione.get('nome')
    
station = bus_choice("Pedaso")
extract_data(station)