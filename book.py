import requests

from extrapolate_data import *

def prenota():
    s = requests.Session()
    queryRicerca = {'PartenzaID': '24',
            'flexdatalist-PartenzaID':'Camerino Terminal',
            'DestinazioneID': '41',
            'flexdatalist-DestinazioneID':'Civitanova Marche F.S',
            'DataPartenza': '2022-11-04',
            'DataRitorno': '',
            'NumeroAdulti': '0',
            'NumeroBambini': '0',
            'NumeroStudenti': '1',
            'NumeroPacchi': '0',
    }
    r = s.get('https://marcheroma.contram.it/home/Ricerca', params=queryRicerca)
    print("Url da inviare "+r.url)
    print("Risposta "+r.text)
    dataPrenota = { 'CorsaID': '20980',
                'TrattaID': '421',
                'DataPartenza': '28/10/2022 00:00:00',
                'DataRitorno': '',
                'PartenzaID': '24',
                'DestinazioneID': '41',
                'NumeroAdulti': '0',
                'NumeroBambini': '0',
                'NumeroStudenti': '1',
                'NumeroPacchi': '0',
    }
    r = s.post('https://marcheroma.contram.it/home/Prenota', data=dataPrenota)
    print('Risposta: '+r.text)
    #richiesta get '/home/RitornaCarrello'
    r = s.get('https://marcheroma.contram.it/home/RitornaCarrello')
    print('Risposta ritorna carrello '+ r.text)
    #richiesta post mandando ind unicam nome cognome ind mail numero
    dataAcquista = { 'EmailAcquirente': 'giorgiosaldana99@gmail.com',
                'Nominativi[0].CorsaID': '20980',
                'Nominativi[0].TrattaID': '421',
                'Nominativi[0].Tipo': '3',
                'Nominativi[0].Nome': 'Giorgio',
                'Nominativi[0].Cognome': 'Saldana',
                'Nominativi[0].Email': 'giorgiosaldana99@gmail.com',
                'Nominativi[0].Telefono': '3315887863',
    }
    r = s.post('https://marcheroma.contram.it/home/RitornaCarrello', data=dataAcquista)
    print('Risposta Post: '+r.text)
    r = s.get('https://marcheroma.contram.it/home/MostraAcquisto')
    print('Risposta Mostra Acquisto: '+r.text)
    r = s.post('https://marcheroma.contram.it/home/ConfermaPagamentoBraintree')
    print('Completa Pagamento: '+r.text)
    #download biglietto
    r = s.get('https://marcheroma.contram.it/home/DownloadBiglietto')#, params=queryBiglietto)