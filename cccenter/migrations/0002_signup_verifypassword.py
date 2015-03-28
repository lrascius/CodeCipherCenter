# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cccenter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='signup',
            name='verifyPassword',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]
