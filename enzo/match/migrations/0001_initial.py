# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import match.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Foto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titolo', models.CharField(max_length=50)),
                ('vittoria', models.IntegerField(default=0)),
                ('sconfitta', models.IntegerField(default=0)),
                ('punteggio', models.DecimalField(default=match.models.punteggio_default, max_digits=10, decimal_places=3)),
                ('data_pub', models.DateField(default=datetime.date.today)),
            ],
        ),
        migrations.CreateModel(
            name='Giornata',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', models.DateField(default=datetime.date.today)),
                ('vincitore', models.ForeignKey(to='match.Foto')),
            ],
        ),
        migrations.CreateModel(
            name='Utente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=20)),
                ('cognome', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='foto',
            name='proprietario',
            field=models.ForeignKey(to='match.Utente'),
        ),
    ]
