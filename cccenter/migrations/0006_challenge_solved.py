# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cccenter', '0005_auto_20150409_1205'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='solved',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
