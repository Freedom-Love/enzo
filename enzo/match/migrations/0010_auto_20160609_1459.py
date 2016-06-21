# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import match.models


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0009_auto_20160608_1037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foto',
            name='punteggio',
            field=models.FloatField(default=match.models.punteggio_default),
        ),
    ]
