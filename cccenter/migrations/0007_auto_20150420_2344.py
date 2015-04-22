# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cccenter', '0006_challenge_solved'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='datetime_created',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='profile_image',
            field=models.ImageField(default='images/profile/default.png', upload_to='images/profile'),
            preserve_default=True,
        ),
    ]
