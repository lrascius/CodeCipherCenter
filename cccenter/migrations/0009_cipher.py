# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cccenter', '0008_auto_20150425_2254'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cipher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('ciphertype', models.CharField(max_length=200)),
                ('difficulty', models.CharField(max_length=50, choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
