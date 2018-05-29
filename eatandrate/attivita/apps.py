from django.apps import AppConfig


class AttivitaConfig(AppConfig):
    name = 'attivita'

    def ready(self):
        """Crea le tipologie attribuibili alle attività"""
        super()
        from .models import Tipologia
        if Tipologia.objects.count() == 0:
            Tipologia.objects.create(nome='Pizzeria')
            Tipologia.objects.create(nome='Internazionale')
            Tipologia.objects.create(nome='Pesce')
            Tipologia.objects.create(nome='Vegano')
            Tipologia.objects.create(nome='FastFood')
            Tipologia.objects.create(nome='Birreria')
            Tipologia.objects.create(nome='Tradizionale')
            Tipologia.objects.create(nome='Sushi')
            Tipologia.objects.create(nome='Cinese')
            Tipologia.objects.create(nome='Barbecue')
            Tipologia.objects.create(nome='Bar')
