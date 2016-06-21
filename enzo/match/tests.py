from django.test import TestCase
from .models import Foto, Giornata, Utente
from .views import max_foto
from datetime import date, timedelta
from django.core.urlresolvers import reverse

# Create your tests here.


#crea utente indipendentemente dalla classe user referenziata
def create_user(username='prova', password='prova'):
    user = Utente.user.field.rel.to.objects.create_user(username, 'prova@prova.pr', password)
    user = Utente.objects.create(user=user)
    return user


class FotoMethodTest(TestCase):

    #controlla il valori di default all'inserimento di una foto
    def test_nuova_foto(self):
        user = create_user()
        foto = Foto(titolo='test', proprietario=user, img='test.jpg')
        self.assertEqual(foto.vittoria, 0)
        self.assertEqual(foto.sconfitta, 0)
        self.assertEqual(foto.punteggio, 0)

    #controlla il valore dopo la vittoria
    def test_foto_win(self):
        user = create_user()
        foto = Foto(titolo='test', proprietario=user, img='test.jpg')
        foto.win()
        self.assertEqual(foto.sconfitta, 0)
        self.assertEqual(foto.vittoria, 1)
        self.assertEqual(foto.punteggio, 1)

    #controlla il valore dopo la sconfitta
    def test_foto_lose(self):
        user = create_user()
        foto = Foto(titolo='test', proprietario=user, img='test.jpg')
        foto.lose()
        self.assertEqual(foto.sconfitta, 1)
        self.assertEqual(foto.vittoria, 0)
        self.assertEqual(foto.punteggio, -1)

    #controlla che la classifica venga calcolata correttamente
    def test_foto_classifica(self):
        user = create_user()
        foto1 = Foto(titolo='test', proprietario=user, img='test.jpg', vittoria=100, sconfitta=10, punteggio=20)
        foto1.save()
        foto2 = Foto(titolo='test', proprietario=user, img='test.jpg', vittoria=2, sconfitta=30, punteggio=0.2)
        foto2.save()
        foto3 = Foto(titolo='test', proprietario=user, img='test.jpg', vittoria= 10, sconfitta=5, punteggio=13)
        foto3.save()
        foto4 = Foto(titolo='test', proprietario=user, img='test.jpg')
        foto4.save()
        self.assertEqual(foto4.punteggio, 13)
        self.assertEqual(foto1.get_rank(), 1)
        self.assertEqual(foto2.get_rank(), 4)
        self.assertEqual(foto3.get_rank(), 2)
        self.assertEqual(foto4.get_rank(), 3)

    #controlla che il valore delle giornate vinte
    def test_giornate_vinte(self):
        user = create_user()
        foto = Foto.objects.create(titolo='test', img='test.jpg', proprietario=user)
        foto.win()
        #vi deve essere il voto relativo alla giornata ma non la giornata vinta poiche' oggi si deve ancora concludere
        self.assertEqual(foto.get_giornate_vinte(), 0)
        gio = Giornata.objects.filter(foto=foto).count()
        self.assertEqual(gio, 1)

        #per la giornata di ieri deve risultare vincitore
        ieri = date.today() - timedelta(1)
        gio_ieri = Giornata.objects.create(data=ieri)
        gio_ieri.add_voto(foto)
        gio = Giornata.objects.filter(foto=foto).count()
        self.assertEqual(gio, 2)
        self.assertEqual(foto.get_giornate_vinte(), 1)

        #ora la vincitrice sara' foto2
        foto2 = Foto.objects.create(titolo='test', img='test.jpg', proprietario=user)
        gio_ieri.add_voto(foto2)
        gio_ieri.add_voto(foto2)
        self.assertEqual(foto2.get_giornate_vinte(),1)
        self.assertEqual(foto.get_giornate_vinte(),0)
        self.assertEqual(gio_ieri.get_vincitore()[0], foto2)


#testing della view relativa alle foto
class TestMyFotokView(TestCase):

    #se utente anonimo redirect al login
    def test_anon_user(self):
        response = self.client.get(reverse('match:myphoto'))
        self.assertEqual(response.status_code, 302)

    #utente loggato
    def test_user_foto(self):
        username = 'prova'
        password = 'prova'
        user = create_user(username=username, password=password)
        self.client.login(username=username, password=password)

        #nessuna foto
        response = self.client.get(reverse('match:pers_rank', kwargs={'start':0}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Non vi sono foto')
        self.assertQuerysetEqual(response.context['foto'], [])

        #inserimento foto, ora deve apparire la foto ma una sola pagina
        foto = Foto(titolo='test', proprietario=user, img='test.jpg')
        foto.save()
        response = self.client.get(reverse('match:pers_rank', kwargs={'start':0}))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Non vi sono foto')
        self.assertQuerysetEqual(response.context['foto'], ['<Foto: test>'])
        self.assertNotContains(response, 'Next')

        #inseriamo piu' foto per far apparire Next
        for i in xrange(max_foto):
            foto = Foto(titolo='test', proprietario=user, img='test.jpg')
            foto.save()

        response = self.client.get(reverse('match:pers_rank', kwargs={'start':0}))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Non vi sono foto')
        self.assertContains(response, 'Next')