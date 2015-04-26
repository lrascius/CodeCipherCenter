# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cccenter', '0003_auto_20150408_0101'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='challenge_type',
            field=models.CharField(max_length=50, default='single', choices=[('single', 'single'), ('collaborative', 'collaborative'), ('competitive', 'competitive')]),
            preserve_default=False,
        ),
    ]
