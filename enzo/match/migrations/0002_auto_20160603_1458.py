# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='utente',
            name='data_reg',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='utente',
            name='email',
            field=models.EmailField(default='prova@pr.pr', unique=True, max_length=254),
            preserve_default=False,
        ),
    ]
