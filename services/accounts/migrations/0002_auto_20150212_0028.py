# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='anonymous',
            field=models.BooleanField(default=False, verbose_name='Flag that sets this user as an anonymous user'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='blocked',
            field=models.BooleanField(default=False, verbose_name='Flat that sets this user profile as blocked'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='is_verified',
            field=models.BooleanField(default=False, verbose_name='Flag that sets this user profile as verified'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='organization',
            field=models.CharField(max_length=100, verbose_name='Name of the organization that the user belongs to'),
            preserve_default=True,
        ),
    ]
