# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_auto_20150212_0028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='identifier',
            field=models.CharField(max_length=75, verbose_name='Identifier of the server as an element of the network', unique=True, validators=[django.core.validators.RegexValidator(regex='^[a-zA-Z0-9.\\-_]*$', code='invalid_leop_identifier', message="Alphanumeric or '.-_' required")]),
            preserve_default=True,
        ),
    ]
