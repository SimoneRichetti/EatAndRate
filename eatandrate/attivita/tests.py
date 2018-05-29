"""Definisce i test legati al codice dell'app `attivita`"""
from django.template.response import TemplateResponse
from django.test import TestCase
from django.urls import reverse

import Custom.TestUtils as tutils
from recensioni.models import Recensione


# Create your tests here.
class TestRecensisci(TestCase):
    """Test legati alla view `recensisci()` per la creazione di una nuova recensione

    Tests:
        test_get_recensisci_attivita_inesistente
        test_get_recensisci_non_loggato
        test_get_loggato_gia_recensito
        test_get_loggato_non_ancora_recensito
        test_get_owner_loggato
        test_post_attivita_inesistente
        test_post_utente_non_loggato
        test_post_owner_loggato
        test_post_form_sbaliato
        test_post_utente_loggato_form_valido
    """
    def setUp(self):
        """Inizializza DB di test"""
        self.profilo_utente1 = tutils.create_user_profile('profilo1')
        self.profilo_utente2 = tutils.create_user_profile('profilo2')
        self.profilo_utente3 = tutils.create_user_profile('profilo3')
        self.owner1, self.attivita = tutils.create_owner_and_attivita('owner1', 'attivita')
        self.recensione = tutils.create_recensione(self.profilo_utente1, self.attivita)

    def test_get_recensisci_attivita_inesistente(self):
        """Controlla che la view ritorni una risposta 404 nel caso si
        richieda di recensire un'attività con id inesistente utilizzando una
        richiesta GET
        :return:
        """
        self.client.force_login(self.profilo_utente3.user)
        response = self.client.get(reverse('attivita:recensisci', args=(100,)))

        self.assertEqual(404, response.status_code, msg="Status code anomalo")

    def test_get_recensisci_non_loggato(self):
        """Controlla la redirezione alla pagina di login in caso un utente non loggato
        faccia una richiesta GET
        :return:
        """
        dest_url = reverse('attivita:recensisci', args=(self.attivita.id,))
        response = self.client.get(dest_url, follow=True)
        redirect_url = str(reverse('users:login')) + "?next=" + str(dest_url)

        # Controllo avvenuta redirezione
        self.assertGreater(len(response.redirect_chain), 0, msg="Nessuna redirezione")
        self.assertEqual(302, response.redirect_chain[0][1], msg="Status code anomalo")
        self.assertRedirects(response, redirect_url, msg_prefix="Redirezione avvenuta ma "
                                                                "non alla pagina di login")

        # Controllo corretta visualizzazione pagina di login
        self.assertEqual(200, response.status_code, msg="Status code anomalo")
        self.assertRegex(response.request['PATH_INFO'], "login",
                         msg="Non viene visualizzata la pagina di login")
        self.assertIsInstance(response, TemplateResponse, msg="La pagina visualizzata non contiene alcun"
                                                              "template")

    def test_get_loggato_gia_recensito(self):
        """Controlla il corretto funzionamento del sistema nel caso un utente che
        abbia già recensito l'attività tenti di aggiungere una nuova recensione
        mediante una richiesta GET
        :return:
        """
        self.client.force_login(self.profilo_utente1.user)
        response = self.client.get(reverse('attivita:recensisci', args=(self.attivita.id,)), follow=True)
        redirect_url = reverse('attivita:detail', args=(self.attivita.id,))

        # Controllo avvenuta redirezione
        self.assertGreater(len(response.redirect_chain), 0, msg="Nessuna redirezione")
        self.assertEqual(302, response.redirect_chain[0][1], msg="Status code anomalo")
        self.assertRedirects(response, redirect_url, msg_prefix="Redirezione avvenuta ma "
                                                                "non alla pagina di login")

        # Controllo corretta visualizzazione pagina e presenza messaggio di errore
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "Hai già recensito questa attività")

    def test_get_loggato_non_ancora_recensito(self):
        """Controlla il corretto funzionamento del sistema nel caso un utente
        che non abbia ancora recensito l'attività tenti di aggiungere una nuova
        recensione mediante richiesta GET
        :return:
        """
        self.client.force_login(self.profilo_utente3.user)
        response = self.client.get(reverse('attivita:recensisci', args=(self.attivita.id,)), follow=True)

        self.assertEqual(200, response.status_code, msg="Status code anomalo")
        self.assertEqual(0, len(response.redirect_chain), msg="Redirezione inaspettata")
        self.assertRegex(response.request['PATH_INFO'], "recensisci",
                         msg="Non viene visualizzata la pagina di recensione")

    def test_get_owner_loggato(self):
        """Controlla il corretto funzionamento del sistema nel caso l'utente
        loggato sia un proprietario di attività e non un normale utente e generi
        una richiesta GET
        :return:
        """
        dest_url = reverse('attivita:recensisci', args=(self.attivita.id,))
        self.client.force_login(self.owner1.user)
        response = self.client.get(dest_url, follow=True)
        redirect_url = str(reverse('users:login')) + "?next=" + str(dest_url)

        # Controllo avvenuta redirezione
        self.assertGreater(len(response.redirect_chain), 0, msg="Nessuna redirezione")
        self.assertEqual(302, response.redirect_chain[0][1], msg="Status code anomalo")
        self.assertRedirects(response, redirect_url, msg_prefix="Redirezione avvenuta ma "
                                                                "non alla pagina di login")

        # Controllo corretta visualizzazione pagina di login
        self.assertEqual(200, response.status_code, msg="Status code anomalo")
        self.assertRegex(response.request['PATH_INFO'], "login")
        self.assertIsInstance(response, TemplateResponse, msg="Non viene visualizzata "
                                                              "la pagina di login")

    def test_post_attivita_inesistente(self):
        """Controlla riposta 404 nel caso venga inviata una richiesta POST
        con id attività inesistente
        :return:
        """
        self.client.force_login(self.profilo_utente3.user)
        response = self.client.post(reverse('attivita:recensisci', args=(100,)), follow=True)

        self.assertEqual(404, response.status_code, msg="Status code anomalo")

    def test_post_utente_non_loggato(self):
        """Controlla redirezione a pagina di login nel caso venga inviata una
        richiesta POST da un utente non loggato
        :return:
        """
        dest_url = reverse('attivita:recensisci', args=(self.attivita.id,))
        response = self.client.post(dest_url, follow=True)
        redirect_url = str(reverse('users:login')) + "?next=" + str(dest_url)

        # Controllo avvenuta redirezione
        self.assertGreater(len(response.redirect_chain), 0, msg="Nessuna redirezione")
        self.assertEqual(302, response.redirect_chain[0][1], msg="Status code anomalo")
        self.assertRedirects(response, redirect_url, msg_prefix="Redirezione avvenuta ma "
                                                                "non alla pagina di login")

        # Controllo corretta visualizzazione pagina di login
        self.assertEqual(200, response.status_code, msg="Status code anomalo")
        self.assertRegex(response.request['PATH_INFO'], "login", msg="Non viene visualizzata pagina login")
        self.assertIsInstance(response, TemplateResponse, )

    def test_post_owner_loggato(self):
        """Controlla redirezione a pagina di login nel caso venga inviata una
        richiesta POST
        :return:
        """
        dest_url = reverse('attivita:recensisci', args=(self.attivita.id,))
        self.client.force_login(self.owner1.user)
        response = self.client.post(dest_url, follow=True)
        redirect_url = str(reverse('users:login')) + "?next=" + str(dest_url)

        # Controllo avvenuta redirezione
        self.assertGreater(len(response.redirect_chain), 0, msg="Nessuna redirezione")
        self.assertEqual(302, response.redirect_chain[0][1], msg="Status code anomalo")
        self.assertRedirects(response, redirect_url, msg_prefix="Redirezione avvenuta ma "
                                                                "non alla pagina di login")

        # Controllo corretta visualizzazione pagina di login
        self.assertEqual(200, response.status_code)
        self.assertRegex(response.request['PATH_INFO'], "login")
        self.assertIsInstance(response, TemplateResponse, msg="La pagina visualizzata non contiene alcun"
                                                              "template")

    def test_post_form_sbaliato(self):
        """
        Controlla ricarica pagina con notifica degli errori nel caso la view
        riceva una richiesta POST contenente un form con dati non validi
        :return:
        """
        dati_recensione = {
            'voto': 8,
            'testo': '',
        }
        self.client.force_login(self.profilo_utente2.user)
        response = self.client.post(reverse('attivita:recensisci',
                                            args=(self.attivita.id,)), dati_recensione)

        # Controllo ricarica pagina con notifica degli errori
        self.assertEqual(200, response.status_code, msg="Status code anomalo")
        self.assertEqual(response.request['PATH_INFO'],
                         reverse('attivita:recensisci', args=(self.attivita.id,)),
                         msg="Non viene visualizzata pagina di recensione")
        self.assertContains(response, "Errore nella compilazione del form",
                            msg_prefix="Non viene segnalato errore nel form")
        self.assertContains(response, "This field is required",
                            msg_prefix="Non viene segnalato errore nel form")

    def test_post_utente_loggato_form_valido(self):
        """Controlla che venga aggiunta la recensione e avvenga la redirezione
        alla pagina della relativa attività in caso senza errori, ovvero
        richiesta POST da utente loggato e form corretto.
        :return
        """
        num_recensioni_pre_request = Recensione.objects.count()
        dati_recensione = {
            'voto': 4,
            'testo': 'Wow',
        }
        self.client.force_login(self.profilo_utente2.user)
        response = self.client.post(reverse('attivita:recensisci', args=(self.attivita.id,)),
                                    dati_recensione, follow=True)
        redirect_url = reverse('attivita:detail', args=(self.attivita.id,))

        # Controllo redirezione
        self.assertGreater(len(response.redirect_chain), 0, msg="Non avviene redirezione")
        self.assertEqual(302, response.redirect_chain[0][1], msg="Status code anomalo")
        self.assertRedirects(response, redirect_url, msg_prefix="Redirezione avvenuta ma "
                                                                "non alla pagina di login")

        # Controllo caricamento corretto pagina
        self.assertEqual(200, response.status_code, msg="Status code anomalo")
        self.assertEqual(response.request['PATH_INFO'], reverse('attivita:detail', args=(self.attivita.id,)),
                         msg="Non viene visualizzata pagina dell'attività")
        self.assertIsInstance(response, TemplateResponse, msg="La pagina visualizzata non "
                                                              "contiene nessun template")

        # Controllo aggiunta recensione
        self.assertEqual(num_recensioni_pre_request + 1, Recensione.objects.count(),
                         msg="Nessuna nuova recensione")

    def tearDown(self):
        """Libera DB test"""
        del self.profilo_utente1
        del self.profilo_utente2
        del self.profilo_utente3
        del self.owner1
        del self.attivita
        del self.recensione
