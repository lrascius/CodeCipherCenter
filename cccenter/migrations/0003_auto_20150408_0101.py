# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('cccenter', '0002_auto_20150408_0035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='datetime_solved',
            field=models.DateTimeField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='challenge',
            name='forum',
            field=models.ForeignKey(null=True, to='cccenter.Comment', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='challenge',
            name='solved_by',
            field=models.OneToOneField(null=True, to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='challenge',
            name='users',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL, related_name='joined'),
            preserve_default=True,
        ),
    ]
