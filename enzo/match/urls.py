from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^myphoto/$', views.myphoto, name='myphoto'),
    url(r'^mystat/$', views.mystat, name='mystat'),
    url(r'^classifica/(?P<start>[0-9]+)/$', views.classifica, name='rank'),
    url(r'^classifica/inv/(?P<start>[0-9]+)/$', views.classifica, {'inv':True}, name='inv_rank'),
    url(r'^classifica/pers/(?P<start>[0-9]+)/$', views.classifica_pers, name='pers_rank'),
    url(r'^classifica/pers/inv/(?P<start>[0-9]+)/$', views.classifica_pers, {'inv':True}, name='pers_inv_rank'),
    url(r'^delete/$', views.delete, name='delete'),
    url(r'^foto/(?P<pk>[0-9]+)/$', views.foto_detail, name='foto_detail'),
    url(r'^insert/$', views.foto_insert, name='insert'),
    url(r'^giornata(/(?P<year>[0-9]{4}))?(/(?P<month>[0-9]{1,2}))?(/(?P<day>[0-9]{1,2}))?/$', views.giornata, name='giornata')
]