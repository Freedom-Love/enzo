# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0002_auto_20160603_1458'),
    ]

    operations = [
        migrations.AddField(
            model_name='foto',
            name='img',
            field=models.ImageField(default='', upload_to=b'', verbose_name=b'Immagine'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='foto',
            name='data_pub',
            field=models.DateField(default=datetime.date.today, verbose_name=b'Data Pubblicazione'),
        ),
        migrations.AlterField(
            model_name='utente',
            name='data_reg',
            field=models.DateField(default=datetime.date.today, verbose_name=b'Data Registrazione'),
        ),
    ]
