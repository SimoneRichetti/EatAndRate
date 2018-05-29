"""Contiene funzioni per l'aggiunta dell'attività:

Funzioni:
    update_coordinates_from_address(attivita)
    add_attivita(attivitaform, ownerprofile, tipologieform)
"""
import googlemaps
from Custom.TipologieUtils import add_tipe_object


def update_coordinates_from_address(attivita):
    """Ricava latitudine e longitudine da indirizzo e città

    Sfrutta l'API di geocoding di Google Maps. In caso di fallimento, setta a None

    :param attivita: attività di cui aggiornare le coordinate
    :return: attività modificata
    """
    try:
        gmaps = googlemaps.Client(key='AIzaSyCJYy7aDZolwKqUZS6WKEVYDPj36qtWlTI')
        geocode_result = gmaps.geocode(str(attivita.citta) + ', ' + str(attivita.indirizzo))
    except Exception:
        print('citta e indirizzo non riconosciuti')
        attivita.latitudine = None
        attivita.longitudine = None
    else:
        if len(geocode_result) > 0:
            attivita.latitudine = geocode_result[0]['geometry']['location']['lat']
            attivita.longitudine = geocode_result[0]['geometry']['location']['lng']
        else:
            attivita.latitudine = None
            attivita.longitudine = None

    attivita.save()
    return attivita


def add_attivita(attivitaform, ownerprofile, tipologieform):
    """Crea una nuova attività

    Dati i form contenenti informazioni necessarie su attività, relative tipologie
    e relativo proprietario, controlla che siano validi e nel caso aggiunge attività.

    :param attivitaform:
    :param ownerprofile:
    :param tipologieform:
    :return: nuova attività se i form sono validi, None altrimenti
    """
    if attivitaform.is_valid() and tipologieform.is_valid() and ownerprofile:
        attivita = attivitaform.save(commit=False)
        attivita.proprietario = ownerprofile
        attivita = update_coordinates_from_address(attivita)
        add_tipe_object(attivita, tipologieform)
        return attivita
    else:
        return None
