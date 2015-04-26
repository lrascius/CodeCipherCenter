# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('cccenter', '0007_auto_20150420_2344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='users',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, related_name='user_challenge_set', null=True),
            preserve_default=True,
        ),
    ]
