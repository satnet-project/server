# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PassiveMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('retrieved', models.BooleanField(default=False, verbose_name=b'Indicates whether the message has been retrieved by a remote user.')),
                ('doppler_shift', models.FloatField(verbose_name=b'Doppler shift during the reception of the message.')),
                ('groundstation_timestamp', models.BigIntegerField(verbose_name=b'Timestamp for when this message was received at the Ground Station')),
                ('reception_timestamp', models.BigIntegerField(verbose_name=b'Timestamp for when this message was received at the server')),
                ('message', models.CharField(max_length=4000, verbose_name=b'Message raw data in base64')),
                ('groundstation', models.ForeignKey(verbose_name=b'GroundStation that tx/rx this message', to='configuration.GroundStation')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
