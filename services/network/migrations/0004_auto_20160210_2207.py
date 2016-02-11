# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_auto_20150618_2142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='groundstations',
            field=models.ManyToManyField(to='configuration.GroundStation', verbose_name='Ground stations'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='server',
            name='identifier',
            field=models.CharField(validators=[django.core.validators.RegexValidator(regex='^[a-zA-Z0-9.\\-_]*$', code='invalid_server_identifier', message="Alphanumeric or '.-_' required")], max_length=75, unique=True, verbose_name='Identifier of the server as an element of the network'),
            preserve_default=True,
        ),
    ]
