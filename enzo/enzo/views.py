from django.shortcuts import HttpResponseRedirect, render
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.contrib.auth.views import login
from django.contrib.auth.forms import UserCreationForm
from match.views import get_context
from match.models import inserisci_utente

def redirect_index(request):
    return HttpResponseRedirect(reverse('match:index'))

def view_logout(request):
    logout(request)
    return redirect_index(request)

def registration(request, error=False):
    if request.user.is_authenticated():
       return redirect_index(request)

    if request.method == 'POST' and error == False:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            inserisci_utente(user)
            context = get_context(request, title='Registrazione Completata')
            return render(request, 'registration/reg_confirm.html', context)
        else:
            return registration(request, True)
    else:
        context = get_context(request, form=UserCreationForm(), title='Registrazione', error=error)
        return render(request, 'registration/registration.html', context)

def login_view(request):
    if request.user.is_authenticated():
       return redirect_index(request)

    context = get_context(request, title='Login')
    return login(request, extra_context=context)

