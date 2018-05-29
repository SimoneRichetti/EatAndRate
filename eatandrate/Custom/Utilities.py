from wordcloud import WordCloud
from Custom.stopwords import stopwords
import matplotlib.pyplot as plt
from string import punctuation


def create_tag_cloud(attivita):
    """Crea la tag cloud di un'attività

    Data un'attività, unisce il testo delle recensioni, rimuove le stopwords e
    genera la tag cloud

    :param attivita:
    :return:
    """
    text = ""
    for r in attivita.recensione_set.all():
        text += r.testo
        text += ' '

    for p in punctuation:
        text.replace(p, '')

    tokens = text.split()
    for sw in stopwords:
        for i in range(tokens.count(sw)):
            tokens.remove(sw)

    wc = WordCloud(background_color=(255, 255, 255), height=600, width=800).generate(' '.join(tokens))

    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    # print('Salvo tagcloud in', attivita.get_absolute_tagcloud_url())
    plt.savefig(attivita.get_absolute_tagcloud_url(), bbox_inches='tight')


def get_consigliati(request):
    """Data una richiesta HTTP, genera la lista dei consigliati per l'utente loggato

    Dato l'utente loggato, si considerano le sue ultime recensioni. Ricava gli
    utenti che hanno recensito con lo stesso voto e per ognuno di essi le attività
    meglio recensite. Ordina infine per reputazione e ritorna la lista ordinata.

    :param request: richiesta HTTP
    :return: lista dei consigliati
    """
    if not request.user.is_authenticated:
        return None

    # Considero le ultime 3 recensioni dell'utente loggato
    last_recs = request.user.user_profile.recensione_set.order_by('-data')[:3]

    # Dictionary che ad ognuna delle ultime 3 attività recensite associa una lista di consigiati
    cons_per_att = dict()
    for rec in last_recs:
        # Ogni recensione fatta mi genera dei consigliati
        consigliati = set()
        # Considero le recensioni della stess attività che hanno lo stesso voto
        # della recensione dell'utente
        same_vote_recs = rec.attivita.recensione_set.exclude(autore=rec.autore)\
            .filter(voto=rec.voto)  # .order_by('-data')
        # Considero gli autori delle recensioni
        authors = [r.autore for r in same_vote_recs]
        for a in authors:
            # Per ogni autore, prendo le 3 recensioni con voto più alto
            recs = a.recensione_set.\
                       exclude(attivita__recensione__autore_id=request.user.user_profile.id).\
                       order_by('-voto')[:3]
            att_cons = [r.attivita for r in recs]
            for att in att_cons:
                consigliati.add(att)

        cons_per_att[rec.attivita] = sorted(consigliati, key=lambda att: att.reputazione,
                                            reverse=True)
        #print('CONSIGLIATI PER', rec, ':', cons_per_att[rec.attivita])

    top_five = set()
    for cons in cons_per_att.values():
        for att in cons:
            if att.reputazione >= 3:
                top_five.add(att)

    return sorted(top_five, key=lambda att: att.reputazione, reverse=True)[:5]
