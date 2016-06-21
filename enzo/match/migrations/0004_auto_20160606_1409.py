# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0003_auto_20160603_1523'),
    ]

    operations = [
        migrations.CreateModel(
            name='VotiImgGiornata',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('voti', models.IntegerField(default=0)),
            ],
        ),
        migrations.AlterModelOptions(
            name='foto',
            options={'verbose_name_plural': 'Foto'},
        ),
        migrations.AlterModelOptions(
            name='giornata',
            options={'verbose_name_plural': 'Giornate'},
        ),
        migrations.RemoveField(
            model_name='giornata',
            name='vincitore',
        ),
        migrations.AlterField(
            model_name='foto',
            name='proprietario',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Utente',
        ),
        migrations.AddField(
            model_name='votiimggiornata',
            name='foto',
            field=models.ForeignKey(to='match.Foto'),
        ),
        migrations.AddField(
            model_name='votiimggiornata',
            name='giornata',
            field=models.ForeignKey(to='match.Giornata'),
        ),
        migrations.AddField(
            model_name='giornata',
            name='foto',
            field=models.ManyToManyField(to='match.Foto', through='match.VotiImgGiornata'),
        ),
    ]
