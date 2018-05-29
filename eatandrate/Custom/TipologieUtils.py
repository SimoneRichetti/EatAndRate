from django.shortcuts import get_object_or_404
from attivita.models import Tipologia


def add_tipe_object(obj, tip_form):
    """Aggiunge tipologie ad un'attività o ad una ricerca

    :param obj: oggetto a cui aggiungere tipologie
    :param tip_form: form contenente tipologie selezionate
    :return:
    """
    for t in obj.tipologie.all():
        obj.tipologie.remove(t)

    for nome_tip, is_selected in tip_form.cleaned_data.items():
        if is_selected:
            obj.tipologie.add(get_object_or_404(Tipologia, nome=nome_tip))
    obj.save()
