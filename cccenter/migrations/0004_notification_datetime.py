# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('cccenter', '0003_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 7, 4, 43, 49, 162591, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
