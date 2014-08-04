"""
   Copyright 2013, 2014 Ricardo Tubio-Pardavila

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
__author__ = 'rtubiopa@calpoly.edu'

from django.db import models

from services.configuration.models import channels
from services.scheduling.models import operational


class Message(models.Model):
    """Message model class.

    This class includes all the information related with the relay of a
    message.
    """
    operational_slot = models.ForeignKey(
        operational.OperationalSlot,
        verbose_name='OperationalSlot during which the message was transmitted'
    )

    groundstation_channel = models.ForeignKey(
        channels.GroundStationChannel,
        verbose_name='GroundStation channel that tx/rx this message'
    )
    spacecraft_channel = models.ForeignKey(
        channels.SpacecraftChannel,
        verbose_name='Spacecraft channel that tx/rx this message'
    )

    upwards = models.BooleanField(
        'Message relay direction(upwards = GS-to-SC, downwards = SC-to-GS)'
    )
    forwarded = models.BooleanField(
        'Flag that indicates whether the message has already been forwarded '
        'to the receiver'
    )

    reception_timestamp = models.IntegerField(
        'Timestamp that indicates the moment when this message was received at'
        'the server.'
    )
    transmission_timestamp = models.IntegerField(
        'Timestamp that indicates the moment when this message was '
        'transmitted to the receiver'
    )

    message = models.BinaryField('Message raw data')