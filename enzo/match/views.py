from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from .models import Foto, Giornata
from .forms import FotoForm, GiornataForm
from datetime import date
from random import randint

#indica il numero di foto per match
numero_foto = 2

#numero massimo di foto per pagina in classifica
max_foto = 10


#costruisce il context in base a login e ai paremtri passati
def get_context(request, **kargs):
    if request.user.is_authenticated():
        kargs['logged'] = request.user

    kargs['gio_form'] = GiornataForm()
    return kargs


#ritorna l'elemento della query piu' vicino a punteggio
def get_vicino(query, punteggio):
    diff = abs(query.first().punteggio - punteggio)
    pk = query.first().pk
    for x in query:
        new_diff = abs(x.punteggio - punteggio)
        if new_diff > diff:
            return query.get(pk=pk)
        else:
            diff = new_diff
            pk = x.pk

    return query.last()


#funzione che decide che foto mostrare
def get_foto():
    if Foto.objects.all().count() < numero_foto:
        return None

    #prima foto casuale
    foto = []
    query = Foto.objects.order_by('?')
    foto.append(query.first())
    query = query.exclude(pk=foto[0].pk)
    punteggio = foto[0].punteggio

    #selezioniamo le altre foto con punteggio vicino
    #con una certa probabilita' anche la prossima sara' casuale
    while len(foto) < numero_foto:
        caso = randint(1,1000)
        if caso < 100:
            query = query.order_by('?')
            pross = query.first()
        else:
            query = query.order_by('-punteggio')
            pross = get_vicino(query, punteggio)

        foto.append(pross)
        query = query.exclude(pk=pross.pk)
    return foto


# Create your views here.
def index(request):
    if request.method == 'POST':
        try:
            vincitrice = request.POST['foto']
            Foto.objects.get(pk=vincitrice).win()
        except (KeyError, Foto.DoesNotExist):
            return HttpResponseRedirect(reverse('match:index'))

        for i in xrange(1,numero_foto+1):
            if request.POST['foto'+str(i)] != vincitrice:
                Foto.objects.get(pk=request.POST['foto'+str(i)]).lose()

    foto = get_foto()
    context = get_context(request, foto=foto, title='Home')

    return render(request, 'match/index.html', context)


@login_required()
def myphoto(request):
    foto = Foto.objects.filter(proprietario=request.user.utente)
    context = get_context(request, title='Le mie Foto', foto=foto)
    return render(request, 'match/myphoto.html', context)


@login_required()
def mystat(request):
    utente = request.user.utente
    if utente.get_tot_match() == 0:
        match = 0
    else:
        match = float(utente.get_match_vinti()) / utente.get_tot_match() * 100
    rank_medio = utente.get_rank_medio()
    rank_max = utente.get_max_rank()
    rank_min = utente.get_min_rank()
    dati = {'match':match, 'rank_medio':rank_medio, 'rank_max':rank_max, 'rank_min':rank_min}
    context = get_context(request, title='Statistiche Personali', **dati)
    return render(request, 'match/mystat.html', context)

#ritorna un subset di una lista
def subset(list, start, max):
    if start >= max:
        prev = start - max
    else:
        prev = None

    if start + max < len(list):
        foto = list[start:start+max_foto]
        next = start + max
    else:
        foto = list[start::]
        next = None

    return foto, next, prev


@login_required()
def classifica_pers(request, start, inv=False):
    utente = request.user.utente
    start = int(start)
    url = request.resolver_match.view_name

    if inv:
        foto = utente.get_classifica()[::-1]
        desc = 'Tue Foto Peggiori'
    else:
        foto = utente.get_classifica()
        desc = 'Tue Foto Migliori'

    foto, next, prev = subset(foto, start, max_foto)
    next = reverse(url, kwargs={'start': next}) if next != None else None
    prev = reverse(url, kwargs={'start': prev}) if prev != None else None

    context = get_context(request, title=desc, foto=foto, next=next, prev=prev)
    return render(request, 'match/classifica.html', context)


def classifica(request, start, inv=False):
    start = int(start)
    url = request.resolver_match.view_name

    if inv:
        foto = Foto.objects.order_by('punteggio', '-pk')
        desc = 'Foto Peggiori'
    else:
        foto = Foto.objects.order_by('-punteggio', 'pk')
        desc = 'Foto Migliori'

    foto, next, prev = subset(foto, start, max_foto)
    next = reverse(url, kwargs={'start': next}) if next != None else None
    prev = reverse(url, kwargs={'start': prev}) if prev != None else None

    context = get_context(request, title=desc, foto=foto, next=next, prev=prev)
    return render(request, 'match/classifica.html', context)



@login_required()
def delete(request):
    user = request.user.utente
    try:
        foto = request.POST.getlist('foto_sel[]')
        for f in foto:
            fo = Foto.objects.get(pk=f)
            if fo.proprietario == user:
                fo.delete()

    except (KeyError, Foto.DoesNotExist):
        pass

    return HttpResponseRedirect(reverse('match:myphoto'))


@login_required()
def foto_insert(request):
    error = False
    inserted = False
    if request.method == 'POST':
        form = FotoForm(request.POST, request.FILES)
        if form.is_valid():
            foto = form.save(commit=False)
            foto.proprietario = request.user.utente
            foto.save()
            inserted = True
        else:
            error = True

    form = FotoForm()
    context = get_context(request, title='Inserisci Immagine', form=form, inserted=inserted, error=error)
    return render(request, 'match/insert.html', context)


def foto_detail(request, pk):
    foto = get_object_or_404(Foto, pk=pk)
    prop = False
    perc_gio_vinte = None
    if request.user.is_authenticated() and foto.proprietario == request.user.utente:
        prop = True
        giorni = (date.today() - foto.data_pub).days + 1
        perc_gio_vinte = foto.get_giornate_vinte() * 100 / float(giorni)

    context = get_context(request, title=foto.titolo, foto=foto, proprietario=prop, perc_gio=perc_gio_vinte)
    return render(request, 'match/detail.html', context)


def giornata(request, year, month, day):
    if year == None or month == None or day == None:
        raise Http404

    data = date(int(year), int(month), int(day))

    try:
        giornata = Giornata.objects.get(data=data)
        vincitore, voti = giornata.get_vincitore()
    except:
        vincitore = None
        voti = None
        giornata = None

    context = get_context(request, title='Giornata', vincitore=vincitore, voti=voti, giornata=giornata)
    return render(request, 'match/giornata.html', context)