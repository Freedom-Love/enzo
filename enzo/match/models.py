from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.dispatch import receiver
from datetime import date
from time import time
import os

# Create your models here.

def inserisci_utente(user):
    Utente.objects.create(user=user)


#per la portabilita' forniamo questa classe che collega le calassi di questa
#applicazione agli utenti del sito
class Utente(models.Model):

    user = models.OneToOneField(User)

    class Meta:
        verbose_name_plural = 'Utenti'

    def get_match_vinti(self):
        foto = Foto.objects.filter(proprietario=self)
        return sum(y.vittoria for y in foto)

    def get_tot_match(self):
        foto = Foto.objects.filter(proprietario=self)
        return sum(y.vittoria + y.sconfitta for y in foto)

    def get_rank_medio(self):
        foto = Foto.objects.filter(proprietario=self)
        if len(foto) == 0:
            return None
        return sum(y.get_rank() for y in foto) / float(len(foto))

    def get_classifica(self):
        return Foto.objects.filter(proprietario=self).order_by('-punteggio', 'pk')

    def get_max_rank(self):
        rank = self.get_classifica()
        if len(rank) == 0:
            return None
        return rank[0].get_rank()

    def get_min_rank(self):
        rank = self.get_classifica()
        if len(rank) == 0:
            return None
        return rank.last().get_rank()

    def __unicode__(self):
        return self.user.__unicode__()


#restituisce il punteggio necessario a piazzare
#a meta' classifica la nuova foto
def punteggio_default():
    lista = Foto.objects.order_by('-punteggio')
    if len(lista) == 0:
        return 0
    return lista[len(lista)/2].punteggio

#definisce il nome del file salvato
#ogni utente ha la sua directory
#per poterlo trovare facilmente mettiamo il titolo dell'immagine
#per renderlo univoco aggiungiamo _time
def get_file_name(instance, filename):
    ext = '.'+filename.split('.')[-1]
    titolo = instance.titolo.replace(" ", "_")
    return '/'.join(['match', instance.proprietario.user.username, titolo+'_'+str(int(time()))])+ext


class Foto(models.Model):
    titolo = models.CharField(max_length=50)
    vittoria = models.IntegerField(default=0)
    sconfitta = models.IntegerField(default=0)
    punteggio = models.FloatField(default=punteggio_default)
    img = models.ImageField(verbose_name="Immagine", upload_to=get_file_name)
    proprietario = models.ForeignKey(Utente)
    data_pub = models.DateField("Data Pubblicazione",default=date.today)

    class Meta:
        verbose_name_plural = "Foto"

    def win(self):
        self.vittoria += 1
        n = float(self.vittoria + self.sconfitta)
        self.punteggio += (1/n)
        self.save()
        gio = Giornata.objects.get_or_create(data=date.today())[0]
        gio.add_voto(self)

    def lose(self):
        self.sconfitta += 1
        n = float(self.vittoria + self.sconfitta)
        self.punteggio -= (1/n)
        self.save()

    def get_giornate_vinte(self):
        return len([x for x in Giornata.objects.all() if x.get_vincitore()[0] == self])

    #a parita' di punteggio hanno ranking migliore
    #le foto piu' vecchie cioe' pk piu' basso
    def get_rank(self):
        rank = Foto.objects.filter(punteggio__gte=self.punteggio).order_by('-punteggio', 'pk')
        for index, foto in enumerate(rank):
            if foto == self:
                return index + 1
        return 1

    get_rank.short_description = 'Rank'
    get_rank.admin_order_field = 'punteggio'

    def __unicode__(self):
        return self.titolo


class Giornata(models.Model):
    data = models.DateField(default=date.today)
    foto = models.ManyToManyField(Foto, through='VotiImgGiornata')

    class Meta:
        verbose_name_plural = "Giornate"

    def get_vincitore(self):
        #se la giornata e' oggi non vi e' ancora un vincitore
        if self.data == date.today():
            return None,

        g = VotiImgGiornata.objects.filter(giornata=self).order_by('-voti', 'pk')
        if len(g) == 0:
            return None,
        return g[0].foto, g[0].voti

    def add_voto(self, foto):
        v = VotiImgGiornata.objects.get_or_create(giornata=self, foto=foto)[0]
        v.voti += 1
        v.save()


#funzione che elimina il file dal filesystem
#automaticamente
@receiver(models.signals.pre_delete, sender=Foto)
def auto_delete_foto(sender, instance, **kwargs):
    os.remove(instance.img.path)


class VotiImgGiornata(models.Model):
    giornata = models.ForeignKey(Giornata)
    foto = models.ForeignKey(Foto)
    voti = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Voti Immagine Giornata"
        verbose_name_plural = "Voti Immagini Giornate"
