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
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('ciphertext', models.TextField(default='')),
                ('plaintext', models.TextField(default='')),
                ('ciphertype', models.CharField(max_length=200)),
                ('cipherkey', models.TextField(default='')),
                ('datetime_created', models.DateTimeField()),
                ('datetime_solved', models.DateTimeField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('text', models.TextField(default='')),
                ('datetime', models.DateTimeField()),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('datetime_created', models.DateTimeField()),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='challenge',
            name='forum',
            field=models.ForeignKey(blank=True, to='cccenter.Comment'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='challenge',
            name='solved_by',
            field=models.OneToOneField(blank=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='challenge',
            name='users',
            field=models.ManyToManyField(related_name='joined', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
