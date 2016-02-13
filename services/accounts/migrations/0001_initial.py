# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, primary_key=True, parent_link=True, to=settings.AUTH_USER_MODEL, serialize=False)),
                ('organization', models.CharField(verbose_name='Name of the organization that the user belongs to', max_length=100)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('is_verified', models.BooleanField(verbose_name='Flag that sets this user profile as verified', default=False)),
                ('blocked', models.BooleanField(verbose_name='Flat that sets this user profile as blocked', default=False)),
                ('anonymous', models.BooleanField(verbose_name='Flag that sets this user as an anonymous user', default=False)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
        ),
    ]
