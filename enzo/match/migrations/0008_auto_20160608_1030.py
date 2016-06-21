# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import match.models


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0007_auto_20160607_0754'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='foto',
            options={'verbose_name_plural': 'Foto', 'permissions': (('can_upload', 'Can Upload'),)},
        ),
        migrations.AlterModelOptions(
            name='utente',
            options={'verbose_name_plural': 'Utenti'},
        ),
        migrations.AlterField(
            model_name='foto',
            name='img',
            field=models.ImageField(upload_to=match.models.get_file_name, verbose_name=b'Immagine'),
        ),
    ]
