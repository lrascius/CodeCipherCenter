# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cccenter', '0004_challenge_challenge_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='challenge',
            name='forum',
        ),
        migrations.AddField(
            model_name='comment',
            name='forum',
            field=models.ForeignKey(to='cccenter.Challenge', default=None),
            preserve_default=False,
        ),
    ]
