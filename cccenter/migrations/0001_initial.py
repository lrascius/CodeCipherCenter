# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('ciphertext', models.TextField(default='')),
                ('plaintext', models.TextField(default='')),
                ('ciphertype', models.CharField(max_length=200)),
                ('cipherkey', models.TextField(default='')),
                ('datetime_created', models.DateTimeField()),
                ('datetime_solved', models.DateTimeField()),
                ('solved_by', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('username', models.CharField(max_length=50)),
                ('text', models.TextField(default='')),
                ('datetime', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('datetime_created', models.DateTimeField()),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='challenge',
            name='forum',
            field=models.ForeignKey(to='cccenter.Comment'),
        ),
        migrations.AddField(
            model_name='challenge',
            name='users',
            field=models.ManyToManyField(to='cccenter.UserProfile'),
        ),
    ]
