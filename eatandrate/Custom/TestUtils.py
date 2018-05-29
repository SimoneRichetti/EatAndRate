"""Metodi utilizzati per popolare il DB di test

Funzioni:
    create_user(username, **kwargs)
    create_recensione(autore, attivita, **kwargs)
    create_owner_and_attivita(username, nome_att, **kwargs)
    create_user_profile(username, **kwargs)
"""
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from attivita.models import Attivita
from recensioni.models import Recensione
from users.models import UserProfile, OwnerProfile


def create_user(username, **kwargs):
    """Crea un nuovo utente

    Richiede username. Se passate anche altre informazioni vengono salvate, se
    no vengono utilizzate informazioni di default

    :param username: username del nuovo utente
    :param kwargs: eventuali informazioni opzionali
    :return: nuovo utente aggiunto
    """
    if kwargs.get('first_name'):
        first_name = kwargs.get('first_name')
    else:
        first_name = ""

    if kwargs.get('last_name'):
        last_name = kwargs.get('last_name')
    else:
        last_name = ""

    if kwargs.get('password'):
        password = kwargs.get('password')
    else:
        password = 'progettold'
    if kwargs.get('email'):
        email = kwargs.get('email')
    else:
        email = str(username) + '@example.com'

    user = User.objects.create(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password
    )
    user.save()
    return user


def create_recensione(autore, attivita, **kwargs):
    """Crea una nuova recensione

    Richiede l'autore e l'attività relativa, se passate ulteriori informazioni
    vengono salvate, se no si utilizzano informazioni di default

    :param autore: autore recensione
    :param attivita: attività recensita
    :param kwargs: eventuali parametri opzionali
    :return: la nuova recensione creata
    """
    if kwargs.get('data'):
        data = kwargs.get('data')
    else:
        data = timezone.now().date()
    if kwargs.get('testo'):
        testo = kwargs.get('testo')
    else:
        testo = "Dummy review"
    if kwargs.get('voto'):
        voto = kwargs.get('voto')
    else:
        voto = 3
    rec = Recensione.objects.create(
        attivita=attivita,
        autore=autore,
        data=data,
        voto=voto,
        testo=testo
    )
    rec.save()
    return rec


def create_owner_and_attivita(username, nome_att, **kwargs):
    """Crea un nuovo profilo di proprietario e la relativa attività

    Richiede nome utente e nome attività, se passate ulteriori informazioni
    vengono aggiunte, se no utilizza informazioni di default

    :param username: username proprietario
    :param nome_att: nome attività
    :param kwargs: eventuali parametri opzionali
    :return: ritorna il profilo del proprietario e l'attività
    """
    user = create_user(username, **kwargs)
    owner_profile = OwnerProfile.objects.create(
        user=user
    )
    owner_profile.save()
    content_type = ContentType.objects.get(model='attivita')
    permission1 = Permission.objects.get(content_type=content_type,
                                         codename='add_attivita')
    permission2 = Permission.objects.get(content_type=content_type,
                                         codename='delete_attivita')
    permission3 = Permission.objects.get(content_type=content_type,
                                         codename='change_attivita')
    user.user_permissions.add(permission1, permission2, permission3)

    if kwargs.get('indirizzo'):
        indirizzo = kwargs.get('indirizzo')
    else:
        indirizzo = 'via Demo 1'
    if kwargs.get('citta'):
        citta = kwargs.get('citta')
    else:
        citta = 'Roma'
    if kwargs.get('descrizione'):
        descrizione = kwargs.get('descrizione')
    else:
        descrizione = "Dummy description"

    att = Attivita.objects.create(
        nome=nome_att,
        indirizzo=indirizzo,
        citta=citta,
        descrizione=descrizione,
        proprietario=owner_profile,
        latitudine=None,
        longitudine=None
    )
    att.save()
    return owner_profile, att


def create_user_profile(username, **kwargs):
    """Crea un nuovo profilo utente

    Richiede il nome dell'utente, se passate ulteriori informazioni vengono
    salvate, se no si utilizzano informazioni di default

    :param username: nome utente
    :param kwargs: eventuali parametri aggiuntivi
    :return: nuovo profilo utente
    """
    user = create_user(username, **kwargs)
    content_type = ContentType.objects.get(model='recensione')
    permission1 = Permission.objects.get(content_type=content_type,
                                         codename='add_recensione')
    permission2 = Permission.objects.get(content_type=content_type, codename='can_vote_review')
    permission3 = Permission.objects.get(content_type=content_type,
                                         codename='delete_recensione')
    permission4 = Permission.objects.get(content_type=content_type,
                                         codename='change_recensione')

    user.user_permissions.add(permission1, permission2, permission3, permission4)
    user_profile = UserProfile.objects.create(
        user=user,
        affidabilita=0
    )
    user_profile.save()
    return user_profile
