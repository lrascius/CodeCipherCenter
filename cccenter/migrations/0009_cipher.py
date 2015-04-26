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
<<<<<<< local
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
=======
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
>>>>>>> other
                ('ciphertype', models.CharField(max_length=200)),
<<<<<<< local
                ('difficulty', models.CharField(max_length=50, choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')])),
=======
                ('difficulty', models.CharField(choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')], max_length=50)),
>>>>>>> other
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
