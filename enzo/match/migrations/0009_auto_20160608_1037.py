# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0008_auto_20160608_1030'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='foto',
            options={'verbose_name_plural': 'Foto'},
        ),
    ]
