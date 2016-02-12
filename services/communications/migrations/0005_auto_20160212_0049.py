# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('communications', '0004_auto_20160211_2358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='message',
            field=models.CharField(verbose_name='Message raw data in base64', max_length=4000),
            preserve_default=True,
        ),
    ]
