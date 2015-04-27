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
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('ciphertext', models.TextField(default='')),
                ('plaintext', models.TextField(default='')),
                ('ciphertype', models.CharField(max_length=200)),
                ('cipherkey', models.TextField(default='')),
                ('datetime_created', models.DateTimeField()),
                ('datetime_solved', models.DateTimeField(blank=True, null=True)),
                ('challenge_type', models.CharField(choices=[('single', 'Single'), ('collaborative', 'Collaborative'), ('competitive', 'Competitive')], max_length=50)),
                ('solved', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Cipher',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('ciphertype', models.CharField(max_length=200)),
                ('difficulty', models.CharField(choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')], max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('text', models.TextField(default='')),
                ('datetime', models.DateTimeField()),
                ('forum', models.ForeignKey(to='cccenter.Challenge')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('profile_image', models.ImageField(upload_to='images/profile', default='images/profile/default.png')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='challenge',
            name='cipher',
            field=models.ManyToManyField(related_name='cipher_challenge_set', to='cccenter.Cipher'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='challenge',
            name='solved_by',
            field=models.ManyToManyField(blank=True, null=True, related_name='user_solved_challenge_set', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='challenge',
            name='users',
            field=models.ManyToManyField(blank=True, null=True, related_name='user_challenge_set', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
