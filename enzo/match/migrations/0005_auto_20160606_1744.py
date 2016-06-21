# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0004_auto_20160606_1409'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='votiimggiornata',
            options={'verbose_name': 'Voti Immagine Giornata', 'verbose_name_plural': 'Voti Immagini Giornate'},
        ),
        migrations.AlterField(
            model_name='giornata',
            name='foto',
            field=models.ManyToManyField(to='match.Foto', null=True, through='match.VotiImgGiornata'),
        ),
    ]
