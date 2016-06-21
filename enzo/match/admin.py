from django.contrib import admin
from .models import *

# Register your models here.

#Collassiamo i campi meno importanti
class FotoAdmin(admin.ModelAdmin):
    list_display = ['titolo', 'proprietario', 'get_rank', 'punteggio', 'data_pub']
    list_filter = ['proprietario__user__username', 'data_pub']
    search_fields = ['titolo']
    fieldsets = [
        (None, {'fields': ['titolo', 'img', 'proprietario']}),
        ('Info Aggiuntive', {'fields': ['vittoria', 'sconfitta', 'punteggio', 'data_pub'], 'classes':['collapse']} )
    ]


class FotoInline(admin.StackedInline):
    model = Foto
    extra = 3
    fieldsets = FotoAdmin.fieldsets

class VotiInline(admin.StackedInline):
    model = VotiImgGiornata
    extra = 3


#diamo la possibilita' di inserire direttamente
#le immagini. Utile per la creazione del dataset
#iniziale
class UtenteAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_match_vinti', 'get_rank_medio']
    search_fields = ['user']
    inlines = [FotoInline]


class GiornataAdmin(admin.ModelAdmin):
    inlines = [VotiInline]


admin.site.register(Utente, UtenteAdmin)
admin.site.register(Foto, FotoAdmin)
admin.site.register(VotiImgGiornata)
admin.site.register(Giornata, GiornataAdmin)