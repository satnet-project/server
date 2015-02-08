# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models, migrations
import django_countries.fields
from services.common import misc


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('sites', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('organization', models.CharField(max_length=100, verbose_name=b'Name of the organization that the user belongs to')),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('is_verified', models.BooleanField(default=False, verbose_name=b'Flag that sets this user profile as verified')),
                ('blocked', models.BooleanField(default=False, verbose_name=b'Flat that sets this user profile as blocked')),
                ('anonymous', models.BooleanField(default=False, verbose_name=b'Flag that sets this user as an anonymous user')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
        ),
        migrations.RunPython(misc.create_site),
    ]