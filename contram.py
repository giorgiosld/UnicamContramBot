import requests
from extrapolate_data import *

def __scelta(msg):
    scelta = input(msg)
    stazione = bus_choice(scelta)
    return stazione

def __search(s, searchInfo):
    queryRicerca = {
        'PartenzaID': searchInfo[0],
        'flexdatalist-PartenzaID': searchInfo[1],
        'DestinazioneID': searchInfo[2],
        'flexdatalist-DestinazioneID': searchInfo[3],
        'DataPartenza': searchInfo[4],
        'DataRitorno': '',
        'NumeroAdulti': '0',
        'NumeroBambini': '0',
        'NumeroStudenti': '1',
        'NumeroPacchi': '0',
    }
    r = s.get('https://marcheroma.contram.it/home/Ricerca', params=queryRicerca)
    print("Url da inviare "+r.url)
    print("Risposta "+r.text)

def book():
    #quando setti stazione partenza fa richiesta a 
    #https://marcheroma.contram.it/api/fermata/arrivo/52
    #il che ritorna le stazioni di arrivo disponibili
    #dove 52 numero stazione partenza
    #poi fa richiesta a https://marcheroma.contram.it/api/fermata/partenza
    partenza = __scelta("Inserire la stazione di Partenza\n")
    arrivo = __scelta("Inserire la stazione di Arrivo\n")
    date = input("Inserire data di partenza (yyyy-mm-dd)\n")
    pID, p = extract_data(partenza)
    dID, d = extract_data(arrivo)
    s = requests.Session()
    searchInfo = [pID, p, dID, d, date]
    __search(s, searchInfo)

book()