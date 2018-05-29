"""Definisce i test legati al codice dell'app `recensioni`"""
from django.test import TestCase
from django.utils import timezone

import Custom.TestUtils as tutils
from recensioni.models import Recensione


# Create your tests here.
class TestRecensione(TestCase):
    """Test legati al codice del model `Recensione` per valutare l'efficacia
    dei controlli su voto e data

    Tests:
    test_voto_out_of_range
    test_data_futura
    test_no_testo
    test_input_corretto
    """
    def setUp(self):
        """Inizializza DB di test"""
        self.profilo1 = tutils.create_user_profile('profilo1')
        self.owner, self.attivita = tutils.create_owner_and_attivita('owner1', 'attivita1')

    def test_voto_out_of_range(self):
        """Controlla che venga sollevata un'eccezione ValueError in caso di
        tentato salvataggio su DB di una recensione con voto non compreso tra
        1 e 5
        :return:
        """
        with self.assertRaises(ValueError, msg="Non viene segnalato voto non valido"):
            Recensione.objects.create(
                attivita=self.attivita,
                autore=self.profilo1,
                voto=6,
                testo='wow',
                data=timezone.now().date()
            )

    def test_data_futura(self):
        """Controlla che venga sollevata un'eccezione ValueError in caso di
        tentato salvataggio su DB di una recensione con data futura
        :return:
        """
        with self.assertRaises(ValueError, msg="Non viene segnalata data non valida"):
            Recensione.objects.create(
                attivita=self.attivita,
                autore=self.profilo1,
                voto=5,
                testo='wow',
                data=timezone.now().date() + timezone.timedelta(1)
            )

    def test_no_testo(self):
        """Controlla che venga sollevata un'eccezione ValueError in caso di
        tentato salvataggio su DB di una recensione senza testo
        :return:
        """
        with self.assertRaises(ValueError, msg="Non viene segnalato testo non inserito"):
            Recensione.objects.create(
                attivita=self.attivita,
                autore=self.profilo1,
                voto=1,
                testo='',
                data=timezone.now().date()
            )

    def test_input_corretto(self):
        """Controlla che il salvataggio vada a buon fine nel caso i campi della
        recensione siano corretti
        :return:
        """
        num_rec_init = Recensione.objects.count()
        Recensione.objects.create(
            attivita=self.attivita,
            autore=self.profilo1,
            voto=1,
            testo='Wow',
            data=timezone.now().date()
        )
        self.assertGreater(Recensione.objects.count(), num_rec_init,
                           msg="Non viene creata recensione")

    def tearDown(self):
        """Libera DB test"""
        del self.profilo1
        del self.attivita
        del self.owner
