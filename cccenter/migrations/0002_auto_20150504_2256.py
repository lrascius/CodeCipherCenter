# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('cccenter', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='forum',
            field=models.ForeignKey(to='cccenter.Challenge', related_name='challenge_comment_set'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='user_comment_set'),
            preserve_default=True,
        ),
    ]
