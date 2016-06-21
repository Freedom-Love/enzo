# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0005_auto_20160606_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='giornata',
            name='foto',
            field=models.ManyToManyField(to='match.Foto', through='match.VotiImgGiornata'),
        ),
    ]
